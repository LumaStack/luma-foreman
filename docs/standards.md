# Standards

This is a temporary stop gap until we have a proper standards system + ecosystem.

## For distributed tooling, follow XDG standards

XDG is explicit about where config, data, and executables live:

- ~/.config/<org>/<project>/ — configuration: things the user edits
- ~/.local/share/<org>/<project>/ — data: things a program installs and manages
- ~/.local/bin/ — executables