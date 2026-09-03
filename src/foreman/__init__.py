"""luma-foreman — the package root.

`__version__` is the single place the version is written. The tag carries the
`v` prefix and this does not: `git tag v0.1.0` against `__version__ = "0.1.0"`,
so a comparison between a tag and this string is one `lstrip` rather than a
guess about which end the prefix is on.
"""

__version__ = "0.1.0"
