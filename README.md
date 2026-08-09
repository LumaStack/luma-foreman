# luma-foreman

Runs the site. It walks into a project repository, sets it up to succeed, and comes back periodically to check the work still holds.

> **Status:** seed. Nothing here yet but the shape of the job.

## The four jobs

- **Bootstrap.** Stand a new project up with the structure it should have had from the first commit.
- **Outfit.** Install the tooling every project is expected to carry — linting, tests, continuous integration, independent review, a backlog.
- **Inspect.** Check a project against the baseline and report where it falls short. Findings, exit codes, runnable in continuous integration.
- **Refit.** Return over time and confirm the latest learnings have actually been applied, not just published.

It also carries **meta-skills**: skills whose job is to generate a project's own best-practice skills, so each repository ends up with tooling suited to it rather than a copied template.

The goal is projects that are homogeneous where homogeneity pays and optimal where it does not.

## The constraint that defines this repository

**Foreman must run standalone, inside any repository, with no organization context available.**

No checkout of [luma-hq](https://github.com/LumaStack/luma-hq). No network call to fetch standards. No privileged path. A check that needs to know what the organization learned last quarter in order to run is a broken check — the learning must be baked in as an executable rule before it ships here.

This is what makes foreman usable in continuous integration, in a fresh clone, and in a repository belonging to someone with no access to the rest of the organization.

## Relationship to luma-hq

luma-hq is where a standard is argued, decided, and justified. luma-foreman is where it becomes executable and gets enforced. Changes flow one way: hq settles, foreman ships.
