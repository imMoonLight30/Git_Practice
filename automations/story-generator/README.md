# story-generator

> Turn a one-line idea into a full short story + a narrator-style transcript + a character sheet. Optionally render it to an MP3 narrated by a single voice.

## Why

To produce shareable audio stories where a single narrator speaks on behalf of every character — ready to upload to YouTube, Spotify for Podcasters, Instagram, etc.

## How it works

Two scripts, run independently:

1. **`generate_story.py`** — calls an LLM to produce a structured story.
   - Input: a short prompt (and optional YAML config for genre/length/tone/characters).
   - Output (into `outputs/<slug>-<timestamp>/`):
     - `story.md` — the narrative prose
     - `transcript.md` — narrator-style script (single-voice friendly: dialogue is wrapped in tags like `Mira said softly, "I won't go."`)
     - `characters.md` — character bios + voice hints
     - `story.json` — machine-readable copy of all of the above (consumed by the audio step)

2. **`generate_audio.py`** — reads `story.json` (or `transcript.md`) and renders an MP3 using OpenAI's TTS (single narrator voice).

## Requirements

- Python 3.10+
- An OpenAI API key (`OPENAI_API_KEY`)
- Dependencies in [requirements.txt](requirements.txt)

## Setup

```bash
cd automations/story-generator
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # then edit and add your OPENAI_API_KEY
```

| Variable             | Purpose                                              |
| -------------------- | ---------------------------------------------------- |
| `OPENAI_API_KEY`     | Auth for both story generation and TTS               |
| `STORY_MODEL`        | (optional) default `gpt-4o-mini`                     |
| `TTS_MODEL`          | (optional) default `gpt-4o-mini-tts`                 |
| `TTS_VOICE`          | (optional) default `alloy` (one of OpenAI's voices)  |

## Run

### Phase 1 — generate the story

```bash
# Simplest: just give it a prompt
python generate_story.py --prompt "A lonely lighthouse keeper befriends a talking seagull during a storm"

# With more control
python generate_story.py \
  --prompt "A heist on a Mars colony" \
  --genre "sci-fi thriller" \
  --length short \
  --tone "tense, witty" \
  --audience "adults" \
  --language en
```

Or use a YAML config:

```bash
python generate_story.py --config example.yaml
```

### Phase 2 — render audio

```bash
# Point it at the folder produced by phase 1
python generate_audio.py --story-dir outputs/a-heist-on-mars-20260519-1830

# Override voice
python generate_audio.py --story-dir outputs/... --voice nova
```

The MP3 lands in the same folder as `narration.mp3`.

## Example output (truncated)

```
outputs/lighthouse-keeper-20260519-1845/
├── story.md
├── transcript.md
├── characters.md
├── story.json
└── narration.mp3     # after running generate_audio.py
```

## Notes / TODO

- Currently uses one narrator voice for the whole story (matches the "one person tells it all" brief).
- Could be extended later: per-character voices, background music, chapter splits, automatic upload to YouTube/Spotify.
- Long stories will need chunking for TTS (>4096 chars per request). The audio script already handles this by splitting on paragraph boundaries.
