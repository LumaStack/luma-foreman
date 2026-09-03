---
type: luma/idea
title: Improve command-line output UX
description: The command line output for v0.1.0 could use some pretty-ing up.
stage: draft
created: { by: human:benlinton, at: 2026-09-03T00:00:00Z }
---

# Improve command-line output UX

## Output from real world use for prototype v0.1.0

test@test:~/Workspace/code/lumastack/luma-backlog% luma-foreman
usage: luma-foreman <command> [args]

Commands:
  init                stand `.luma/` up in a repository that has none
  get                 adopt a bundle from a catalog into this project
  apply               write what this project adopted into what a harness reads
  inspect             check a project against the baseline and report shortfalls

  bundle              bundles this project holds — list, show, outdated
  catalog             where bundles come from — list, show
  agent-permissions   what an agent is allowed to do in this repository

Run `luma-foreman <command> --help` for a command's own options.
test@test:~/Workspace/code/lumastack/luma-backlog% luma-foreman init
luma-foreman init:
  .luma/PROJECT.md                created — every TODO in it is yours to answer
  .luma/config/luma-foreman.toml  created

  Nothing to gitignore — .luma/ is committed in full. Anything here
  that should not be is machine-local and belongs in ~/.config/luma/.

Next steps:
  luma-foreman catalog show <catalog>              what a catalog publishes
  luma-foreman get luma/<bundle> --from <catalog>  take one
test@test:~/Workspace/code/lumastack/luma-backlog% luma-foreman catalog
no catalogs — nothing registered, and nothing adopted.

  luma-foreman catalog add <url>              register one
  luma-foreman get <bundle> --from <catalog>  or take without registering
test@test:~/Workspace/code/lumastack/luma-backlog% luma-foreman catalog list
no catalogs — nothing registered, and nothing adopted.

  luma-foreman catalog add <url>              register one
  luma-foreman get <bundle> --from <catalog>  or take without registering
test@test:~/Workspace/code/lumastack/luma-backlog% luma-foreman catalog add https://github.com/LumaStack/luma-catalog
lumastack/luma-catalog: registered
  source  https://github.com/LumaStack/luma-catalog
  in      .luma/config/luma-foreman.toml

  Commit the config — the registry is how a teammate's `get` resolves too.
  Then: luma-foreman get lumastack/luma-catalog/<bundle>
test@test:~/Workspace/code/lumastack/luma-backlog% luma-foreman catalog list                                         
  lumastack/luma-catalog   (registered)
    0 of 24 bundles taken
    https://github.com/LumaStack/luma-catalog

1 catalog — registered in .luma/config/luma-foreman.toml, or remembered by receipts.

  luma-foreman catalog show <name>    what one publishes
test@test:~/Workspace/code/lumastack/luma-backlog% 

test@test:~/Workspace/code/lumastack/luma-backlog% luma-foreman catalog add https://github.com/LumaStack/luma-catalog
lumastack/luma-catalog is already registered — nothing to do
test@test:~/Workspace/code/lumastack/luma-backlog% luma-foreman get LumaStack/luma-catalog/luma-types                
luma-foreman get: no catalog — luma-foreman catalog add <url> to register one, or pass --from <path-or-url>
test@test:~/Workspace/code/lumastack/luma-backlog% luma-foreman get lumastack/luma-catalog/luma-types
lumastack/luma-catalog/luma-types: adopted 0.15.1
  from     lumastack/luma-catalog — https://github.com/LumaStack/luma-catalog
  commit   ce13c21e65900542c1570a6afdf903d8ac4fbf73
  into     .luma/bundles/lumastack/luma-catalog/luma-types/  (7 files)
  checksum sha256:b95583c57b3cf0c88b00bc034a668ed5f1a7e9811553cf7eeda8f87e72dfa281

  Commit the copy — an adopted bundle lives in the repository.
  Then: luma-foreman apply
test@test:~/Workspace/code/lumastack/luma-backlog% 