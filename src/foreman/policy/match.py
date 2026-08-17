"""Deciding whether a command string invokes a gated class of command.

This matches TEXT. It cannot tell an argument from a command, so it over-prompts
on string literals like ``echo "rm -rf /"``. That is intentional and it fails
safe toward prompting.

What it is not: a security boundary. ``$(echo curl)``, a renamed binary, or a
Python script using urllib all walk straight past it. It guards against your own
slips and an agent's carelessness. For an actual boundary, use Claude Code's
sandboxing and put this on top for ergonomics.
"""

from __future__ import annotations

import re

# A command word, optionally reached by path: `curl`, `/usr/bin/curl`,
# `foo && curl`. Not `mycurl`, not `curl.sh`.
def _word(name: str) -> re.Pattern[str]:
    return re.compile(rf"(?:^|[^\w.\-])(?:[\w./\-]*/)?{name}(?:\s|$)")


WORD = {n: _word(n) for n in ("ssh", "curl", "wget", "sudo")}

# `rm` as a command word, then within its own argument list — not crossing a
# |, & or ; separator — a flag cluster containing r/R, or --recursive. The
# recursive flag is what matters; -f is not required.
RECURSIVE_RM = re.compile(
    r"(?:^|[^\w])rm\s+(?:[^|&;]*\s)?(?:-[a-zA-Z]*[rR][a-zA-Z]*|--recursive)(?:\s|$)"
)

GIT_PUSH = re.compile(r"(?:^|[^\w.\-])git(?:\s+-\S+)*\s+push(?:\s|$)")

# Package managers that fetch and then execute what they fetched. A convenience
# gate, not a boundary: these are the common front doors and nothing more.
DOWNLOADS = re.compile(
    r"(?:^|[^\w.\-])(?:"
    r"(?:npm|pnpm|yarn|bun)\s+(?:i|install|add|ci)"
    r"|(?:pip|pip3|uv)\s+(?:install|add)"
    r"|go\s+(?:get|install)"
    r"|cargo\s+(?:add|install|fetch)"
    r"|gem\s+install|brew\s+install|apt-get\s+install"
    r")(?:\s|$)"
)

# The CLI's own writing subcommands, and shell-level writes aimed at the policy
# directory or the gate. Reads stay ungated on purpose.
CLI_WRITE = re.compile(
    r"(?:^|[^\w.\-])luma-foreman\s+policy\s+(?:-\S+\s+)*"
    r"(?:set|unset|reset|edit|allow|ask|deny|install)(?:\s|$)"
)
POLICY_PATH = re.compile(
    r"config/luma-foreman|share/luma-foreman|\.config/luma/|share/luma/"
    r"|LUMA_FOREMAN_HOME|LUMA_FOREMAN_DATA|permission-gate"
)
WRITE_OP = re.compile(r">|>>|tee|sed\s+-i|\bcp\b|\bmv\b|\brm\b|install|truncate|chmod|chown|\bln\b")

# A lone `luma-foreman policy ...` invocation, anchored, with no shell
# separator anywhere. Deliberately narrow: matching the CLI *anywhere* would let
# `echo luma-foreman policy && curl evil` disarm every rule by naming it.
#
# The optional path prefix is not cosmetic. Without it `./bin/luma-foreman
# policy reset curl` — how you run it from a checkout — was not exempt, so with
# curl=deny the gate refused the command that would lift the deny. Same lockout
# as before, reached by a different route.
CLI_INVOCATION = re.compile(r"^\s*(?:[\w./\-]*/)?luma-foreman\s+policy(?:\s|$)")
SEPARATORS = (";", "&", "|", "`", "$(", "<(")

# curl/wget = "safe": a plain fetch is fine; writing to disk, uploading a body,
# or piping into an interpreter is not.
PIPE_TO_SHELL = re.compile(r"\|\s*(?:sudo\s+)?(?:sh|bash|zsh|ksh|dash|python[\d.]*|perl|ruby|node)(?:\s|$)")
SUBSTITUTION = re.compile(r"<\(\s*(?:curl|wget)|\$\(\s*(?:curl|wget)|`\s*(?:curl|wget)")
WRITES_OR_UPLOADS = re.compile(
    r"(?:^|\s)(?:-[oOT]|--output|--output-document|--remote-name|--upload-file"
    r"|-d|--data|--data-binary|--data-raw|-F|--form)(?:[\s=]|$)"
)


def is_cli_invocation(cmd: str) -> bool:
    """True when the command IS a `luma-foreman policy` call, not merely one that mentions it."""
    if any(sep in cmd for sep in SEPARATORS):
        return False
    return bool(CLI_INVOCATION.search(cmd))


def matches(key: str, cmd: str) -> bool:
    """Does *cmd* invoke the class of command that *key* gates?"""
    # `luma-foreman policy ...` talks ABOUT gated commands; it does not run them.
    # Without this, naming a key locks you out of changing it: with curl=deny,
    # the "curl" inside `policy reset curl` matches the curl rule and refuses
    # the one command that would lift the deny.
    if key != "policy_write" and is_cli_invocation(cmd):
        return False

    if key == "recursive_rm":
        return "rm" in cmd and bool(RECURSIVE_RM.search(cmd))
    if key in WORD:
        return key in cmd and bool(WORD[key].search(cmd))
    if key == "git_push":
        return "push" in cmd and bool(GIT_PUSH.search(cmd))
    if key == "downloads":
        return bool(DOWNLOADS.search(cmd))
    if key == "policy_write":
        if "luma" not in cmd and "foreman" not in cmd and "permission-gate" not in cmd:
            return False
        if CLI_WRITE.search(cmd):
            return True
        return bool(POLICY_PATH.search(cmd)) and bool(WRITE_OP.search(cmd))
    return False


def fetch_unsafe(cmd: str) -> bool:
    """For curl/wget = "safe": does this command do more than fetch to stdout?"""
    return bool(PIPE_TO_SHELL.search(cmd) or SUBSTITUTION.search(cmd) or WRITES_OR_UPLOADS.search(cmd))


_FLAG_WITH_VALUE = re.compile(r"^-[bcDEeFIiJLlmOoPpQRSWw]$")


def ssh_host(cmd: str) -> str | None:
    """The host of a single ssh invocation, or None when it cannot be read confidently.

    More than one ssh in a compound means we do not guess. Neither does an
    unparseable argument list. Both fall through to a prompt.
    """
    if len(WORD["ssh"].findall(cmd)) != 1 and len(re.findall(r"(?:^|[^\w.\-])(?:[\w./\-]*/)?ssh(?:\s|$)", cmd)) != 1:
        return None
    parts = cmd.split()
    for i, tok in enumerate(parts):
        if tok == "ssh" or tok.endswith("/ssh"):
            j = i + 1
            while j < len(parts):
                if parts[j].startswith("-"):
                    if _FLAG_WITH_VALUE.match(parts[j]):
                        j += 1
                    j += 1
                    continue
                return parts[j].split("@")[-1]
            return None
    return None


def ssh_trusted(cmd: str, hosts: str) -> bool:
    if not hosts:
        return False
    if len(re.findall(r"(?:^|[^\w.\-])(?:[\w./\-]*/)?ssh(?:\s|$)", cmd)) != 1:
        return False
    host = ssh_host(cmd)
    if not host:
        return False
    return host in {h for h in re.split(r"[,\s]+", hosts) if h}
