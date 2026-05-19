# <Automation Name>

> One-sentence description of what this automation does and who it's for.

## Why

What problem does it solve? What did life look like before this existed?

## How it works

A short explanation — 3–6 sentences or a bullet list. Mention the key components, external services, and data flow.

## Requirements

- Language / runtime (e.g. Python 3.11, Node 20, Java 17)
- External tools or accounts (e.g. a Google account, a Kite API key)
- Dependencies (link to `requirements.txt` / `package.json` / `pom.xml`)

## Setup

```bash
# from the repo root
cd automations/<name>
# install deps — example for Python
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

Copy `.env.example` to `.env` and fill in:

| Variable        | Purpose                          |
| --------------- | -------------------------------- |
| `EXAMPLE_KEY`   | What this is used for            |

## Run

```bash
python main.py            # or: node index.js, ./run.sh, etc.
```

## Example output

```
Sample of what success looks like.
```

## Notes / TODO

- Known limitations
- Ideas for the next iteration
