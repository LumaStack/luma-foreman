"""What can be gated, what it accepts, and what it means.

One table drives the gate, the CLI's validation, its help, and `keys`. Adding a
gated command class means adding a Key here and a matcher in `match.py`.
"""

from __future__ import annotations

from dataclasses import dataclass, field

# Decision values, in the order they escalate.
ALLOW = "allow"    # no opinion; the normal Claude Code permission flow decides
ASK = "ask"        # prompt, but bypassPermissions and trust="full" silence it
ALWAYS = "always"  # prompt in every mode, bypass included
DENY = "deny"      # refuse outright, every mode
TRUSTED = "trusted"  # ssh only: allow a host on ssh_hosts, otherwise ask
SAFE = "safe"        # curl/wget only: allow a plain fetch, ask when it writes/uploads/pipes

TIERED = (ALWAYS, ASK, ALLOW, DENY)


@dataclass(frozen=True)
class Key:
    name: str
    values: tuple[str, ...]
    default: str
    gates: str
    note: str = ""

    @property
    def free_form(self) -> bool:
        """True when the value is data rather than a decision.

        ``ssh_hosts`` is the only one. The allow/ask/deny shorthands are
        meaningless for it, and offering them writes the string "allow" into a
        hostname list.
        """
        return not self.values


KEYS: tuple[Key, ...] = (
    Key("trust", ("normal", "full"), "normal",
        "Whether this project skips the ask tier entirely.",
        '"full" silences every ask-tier gate in this project without touching the\n'
        "always tier — recursive_rm still prompts. It is a per-project standing\n"
        "version of bypassPermissions, which is per-session and toggled with shift+tab."),
    Key("recursive_rm", TIERED, ALWAYS,
        "rm -r, -R, -rf, --recursive — including inside compounds and via /bin/rm."),
    Key("ssh", TIERED + (TRUSTED,), ASK,
        "Any ssh invocation.",
        '"trusted" allows a host named in ssh_hosts and prompts for anything else.\n'
        "Anything it cannot parse with confidence prompts: no host, an unrecognised\n"
        "flag form, or two ssh invocations in one compound. Set ssh_hosts as well,\n"
        'or "trusted" trusts nothing.'),
    Key("curl", TIERED + (SAFE,), ASK, "Any curl invocation."),
    Key("wget", TIERED + (SAFE,), ASK, "Any wget invocation."),
    Key("sudo", TIERED, ASK, "Any sudo invocation."),
    Key("git_push", TIERED, ASK,
        "git push. Force-pushes also hit a native ask rule that fires in every mode."),
    Key("downloads", TIERED, ALLOW,
        "Package managers that fetch and then run what they fetched: npm/pnpm/yarn/bun, "
        "pip/uv, go, cargo, gem, brew, apt-get.",
        "This lists the common front doors, and that is all it can do. Any script\n"
        "that opens a socket downloads too, so treat this as a speed bump on the\n"
        "obvious cases rather than a claim that nothing reaches the network."),
    Key("policy_write", TIERED, ALWAYS,
        "Writes to the policy files, and to the gate that reads them. Also covers the "
        "writing subcommands of this command.",
        "Keeps a session from editing the rules that govern it. Paired with\n"
        "Edit(~/.config/luma/**) in settings.json permissions.deny, which covers the\n"
        "file tools. Reads stay ungated on purpose — being able to see the policy is\n"
        "what makes a refusal legible. Lowering this below \"always\" means an agent\n"
        "can hand itself any permission it likes."),
    Key("ssh_hosts", (), "",
        "Comma- or space-separated hosts treated as trusted when ssh = trusted."),
)

BY_NAME: dict[str, Key] = {k.name: k for k in KEYS}

# Keys that classify a command. `trust` is a mode, `ssh_hosts` is data.
GATED: tuple[Key, ...] = tuple(
    k for k in KEYS if k.name not in ("trust", "ssh_hosts")
)

SAFE_NOTE = (
    '"safe" allows a plain fetch and prompts when the command writes to disk (-o,\n'
    "-O, --output), uploads a body (-T, -d, -F, --data), or pipes into an\n"
    "interpreter (| sh, bash <(...), $(curl ...)).\n\n"
    "It CANNOT tell you what a URL returns. The hook sees only the command string,\n"
    'so "safe" is a claim about the shape of the command, never about the bytes\n'
    "that come back. Ergonomics, not containment."
)


def note_for(key: Key) -> str:
    if key.name in ("curl", "wget"):
        return SAFE_NOTE
    return key.note


def defaults() -> dict[str, str]:
    return {k.name: k.default for k in KEYS}
