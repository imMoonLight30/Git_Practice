# Claude Code — Project Guide

See [AGENTS.md](AGENTS.md) for the full set of conventions. This file mirrors the key points for Claude Code's auto-loaded context.

## Quick rules

- This repo (`automation-hub`) holds personal automations, one per folder under `automations/`.
- Every automation has its own `README.md` (use [docs/automation-template.md](docs/automation-template.md)).
- Pick the simplest language that fits — Python, Node, Shell, Java when needed.
- Self-contained dependencies per automation. No secrets in git — use `.env`.
- Update the Index in the top-level [README.md](README.md) when adding an automation.

## Before you start work

1. Read [AGENTS.md](AGENTS.md).
2. If modifying an existing automation, read its `README.md` first.
3. Ask the owner to clarify ambiguous requirements rather than guessing.
