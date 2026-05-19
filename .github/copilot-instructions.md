# GitHub Copilot Instructions

This repo (`automation-hub`) is a personal collection of automations. Follow [AGENTS.md](../AGENTS.md) for the full guide. Key points:

- **Structure**: each automation lives in its own folder under `automations/<kebab-case-name>/` with its own `README.md`.
- **Language**: pick what fits the task (Python, Node/TS, Shell, Java). Default to Python for scripts.
- **Self-contained**: each automation pins its own dependencies. No shared lockfile at the repo root unless multiple automations share runtime.
- **Secrets**: never commit. Use `.env` (gitignored) and document required variables in the automation's README.
- **Index**: when adding a new automation, append it to the Index in the top-level [README.md](../README.md).
- **Quality**: small readable functions, clear logging, fail loudly. Don't over-engineer.
- **Scope discipline**: do not refactor unrelated automations. Don't add stubs/placeholders.

When in doubt, mirror the structure of an existing automation in `automations/`.
