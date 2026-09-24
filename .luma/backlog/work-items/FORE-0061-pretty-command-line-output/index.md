---
type: work-item
key: FORE-0061
title: Pretty command line output
workflow_status: captured
rank: 010.0600.000
kind: idea
stage: draft
created: {by: 'agent:claude-opus-5/luma-backlog', at: '2026-09-24T19:43:51Z'}
description: '% luma-foreman Reliable governance and predictable intelligence — for every project. USAGE luma-foreman <command> <subcommand> [args] CORE COMMANDS get Fetch a bundle for this repository apply Adopt bundles into agent harnesses inspect Check health bundle Manage bundles catalog Manage catalogs - where bundles come from publish Publish to a catalog remove Drop a bundle'
modified: {by: 'agent:claude-opus-5/luma-backlog', at: '2026-09-24T19:43:51Z'}
---

# Pretty command line output

% luma-foreman
Reliable governance and predictable intelligence — for every project.

USAGE
  luma-foreman <command> <subcommand> [args]

CORE COMMANDS
  get                 Fetch a bundle for this repository
  apply               Adopt bundles into agent harnesses
  inspect             Check health
  bundle              Manage bundles
  catalog             Manage catalogs - where bundles come from
  publish             Publish to a catalog
  remove              Drop a bundle

RESTRICT
  agent-permissions   Restrict agents in this repository

GETTING STARTED
  init                Setup this repository, safely
  help

FLAGS
  --help              Show help for command
  --version           Show version

EXAMPLES
  $ luma-foreman init
  $ luma-foreman catalog add https://github.com/LumaStack/luma-catalog
  $ luma-foreman get lumastack/luma-catalog/git-workflow
  $ luma-foreman apply
  $ luma-foreman bundle list

LEARN MORE
  Use `luma-foreman <command> <subcommand> --help` for a command's own options.
  Find more at https://github.com/LumaStack/luma-foreman

## Related work

- Born from the idea it replaces: [`pretty-command-line-output`](../../ideas/pretty-command-line-output.md)
