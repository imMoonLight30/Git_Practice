# Instructions for AI Agents

Welcome. This repo (`automation-hub`) is a personal collection of automations. You — Claude, Copilot, Codex, Cursor, or any other coding agent — are expected to read this file before making changes.

## Mission

Help the owner build small, focused automations that solve real problems. Some will grow into products. Treat every automation as something that could one day be shipped.

## Ground rules

1. **One automation per folder** under `automations/<name>/`. Don't mix unrelated work.
2. **Every automation needs a `README.md`** with: purpose, how to run, dependencies, required env vars, example output.
3. **Pick the right language for the job.** Default to Python for scripting, Node/TypeScript for web/API work, Shell for glue, Java only when it genuinely fits. Document the choice.
4. **Keep automations self-contained.** Dependencies live inside the automation's folder (`requirements.txt`, `package.json`, `pom.xml`, etc.).
5. **No secrets in git.** Use `.env` files (gitignored) and document required variables.
6. **Update the Index** in [README.md](README.md) when you add a new automation.

## Workflow when adding a new automation

1. Confirm the goal with the owner if anything is ambiguous.
2. Create `automations/<kebab-case-name>/`.
3. Copy [docs/automation-template.md](docs/automation-template.md) → `automations/<name>/README.md` and fill it in.
4. Implement the smallest working version first. Iterate.
5. Add a usage example or sample output in the README.
6. Append the automation to the **Index** in the top-level README.

## Workflow when modifying an existing automation

1. Read that automation's `README.md` first.
2. Preserve its existing language/runtime unless asked to change it.
3. Update the README if behavior, inputs, or dependencies change.

## Code quality expectations

- Small, readable functions over clever one-liners.
- Validate inputs at the entry point. Don't over-engineer internal validation.
- Log what the automation is doing — these run unattended.
- Fail loudly with clear error messages.
- Add a brief comment block at the top of each script: what it does, how to run it.

## Things to avoid

- Don't refactor unrelated automations "while you're in there".
- Don't add frameworks/build systems unless the automation actually needs them.
- Don't generate placeholder/stub automations that don't do real work.
- Don't commit credentials, tokens, or personal data.

## Useful context

- The owner uses macOS.
- This repo is a learning + building space — clarity matters more than cleverness.
- If an automation could be useful to others later, structure it so it could be extracted into its own repo cleanly.
