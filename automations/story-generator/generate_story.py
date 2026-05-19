"""
generate_story.py
-----------------
Generate a short story, a narrator-style transcript, and a character sheet
from a one-line prompt (or a YAML config).

Run:
    python generate_story.py --prompt "your idea here"
    python generate_story.py --config example.yaml
"""

from __future__ import annotations

import argparse
import json
import logging
import os
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

import yaml
from dotenv import load_dotenv
from openai import OpenAI

LENGTH_PRESETS = {
    "short": "600-900 words",
    "medium": "1500-2200 words",
    "long": "3500-5000 words",
}

SYSTEM_PROMPT = """You are a professional short-fiction writer and audio-drama scriptwriter.

You will be given a story brief. Produce a complete story in JSON with this exact schema:

{
  "title": str,
  "logline": str,                     // one-sentence pitch
  "characters": [
    {
      "name": str,
      "role": str,                    // protagonist / antagonist / mentor / etc.
      "description": str,             // 2-3 sentences
      "voice_hint": str               // how a single narrator should voice this character (pitch, pace, accent, mood)
    }
  ],
  "story": str,                       // the narrative prose, in the requested length
  "transcript": str                   // a narrator-friendly script of the SAME story
}

Rules for `transcript`:
- It will be read aloud by ONE narrator who voices every character.
- Wrap dialogue in standard quotes with attribution tags, e.g. Mira whispered, "I won't go."
- Insert short stage cues in italics like *(a long pause)* or *(thunder rolls)* sparingly.
- No speaker labels like "MIRA:" — keep it prose so a single TTS voice flows naturally.
- Keep paragraphs short (2-4 sentences) so TTS chunking sounds clean.

Return ONLY valid JSON. No markdown fences, no commentary.
"""


def slugify(text: str, max_len: int = 50) -> str:
    text = re.sub(r"[^a-zA-Z0-9\s-]", "", text).strip().lower()
    text = re.sub(r"[\s_-]+", "-", text)
    return text[:max_len].strip("-") or "story"


def build_user_prompt(cfg: dict[str, Any]) -> str:
    parts = [f"Prompt / premise: {cfg['prompt']}"]
    if cfg.get("genre"):
        parts.append(f"Genre: {cfg['genre']}")
    length_key = cfg.get("length", "short")
    parts.append(f"Target length: {LENGTH_PRESETS.get(length_key, length_key)}")
    if cfg.get("tone"):
        parts.append(f"Tone: {cfg['tone']}")
    if cfg.get("audience"):
        parts.append(f"Audience: {cfg['audience']}")
    if cfg.get("language"):
        parts.append(f"Language: {cfg['language']}")
    if cfg.get("characters"):
        seeded = "\n".join(
            f"  - {c.get('name', '?')}: {c.get('role', '')}".rstrip(": ")
            for c in cfg["characters"]
        )
        parts.append(f"Seeded characters (expand as needed):\n{seeded}")
    return "\n".join(parts)


def call_llm(client: OpenAI, model: str, user_prompt: str) -> dict[str, Any]:
    logging.info("Calling %s ...", model)
    resp = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        response_format={"type": "json_object"},
        temperature=0.9,
    )
    content = resp.choices[0].message.content or ""
    try:
        return json.loads(content)
    except json.JSONDecodeError as e:
        raise RuntimeError(f"LLM did not return valid JSON: {e}\n---\n{content[:500]}") from e


def render_characters_md(characters: list[dict[str, Any]]) -> str:
    lines = ["# Characters\n"]
    for c in characters:
        lines.append(f"## {c.get('name', 'Unknown')}")
        if c.get("role"):
            lines.append(f"**Role:** {c['role']}")
        if c.get("description"):
            lines.append(f"\n{c['description']}")
        if c.get("voice_hint"):
            lines.append(f"\n**Voice hint:** {c['voice_hint']}")
        lines.append("")
    return "\n".join(lines)


def write_outputs(out_dir: Path, data: dict[str, Any]) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)

    title = data.get("title", "Untitled")
    logline = data.get("logline", "")

    story_md = f"# {title}\n\n> {logline}\n\n{data.get('story', '').strip()}\n"
    transcript_md = f"# {title} — Narrator transcript\n\n{data.get('transcript', '').strip()}\n"
    characters_md = render_characters_md(data.get("characters", []))

    (out_dir / "story.md").write_text(story_md, encoding="utf-8")
    (out_dir / "transcript.md").write_text(transcript_md, encoding="utf-8")
    (out_dir / "characters.md").write_text(characters_md, encoding="utf-8")
    (out_dir / "story.json").write_text(
        json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    logging.info("Wrote outputs to %s", out_dir)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Generate a story + transcript + characters.")
    p.add_argument("--prompt", help="One-line story idea.")
    p.add_argument("--config", help="Path to a YAML config file.")
    p.add_argument("--genre", help="Genre (e.g. 'sci-fi thriller').")
    p.add_argument("--length", choices=list(LENGTH_PRESETS.keys()), help="Target story length.")
    p.add_argument("--tone", help="Tone (e.g. 'warm, witty').")
    p.add_argument("--audience", help="Target audience.")
    p.add_argument("--language", help="Language code or name. Default: en.")
    p.add_argument("--out", default="outputs", help="Output root directory.")
    p.add_argument("--model", help="Override the LLM model.")
    return p.parse_args()


def load_config(args: argparse.Namespace) -> dict[str, Any]:
    cfg: dict[str, Any] = {}
    if args.config:
        with open(args.config, encoding="utf-8") as f:
            cfg = yaml.safe_load(f) or {}
    # CLI flags override config
    for key in ("prompt", "genre", "length", "tone", "audience", "language"):
        val = getattr(args, key, None)
        if val:
            cfg[key] = val
    cfg.setdefault("length", "short")
    cfg.setdefault("language", "en")
    if not cfg.get("prompt"):
        sys.exit("Error: --prompt (or 'prompt' in --config) is required.")
    return cfg


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    load_dotenv()

    if not os.getenv("OPENAI_API_KEY"):
        sys.exit("Error: OPENAI_API_KEY not set (see .env.example).")

    args = parse_args()
    cfg = load_config(args)
    model = args.model or os.getenv("STORY_MODEL", "gpt-4o-mini")

    client = OpenAI()
    user_prompt = build_user_prompt(cfg)
    data = call_llm(client, model, user_prompt)

    # Preserve the brief alongside the story for reproducibility
    data["_brief"] = cfg

    title = data.get("title") or cfg["prompt"]
    timestamp = datetime.now().strftime("%Y%m%d-%H%M")
    out_dir = Path(args.out) / f"{slugify(title)}-{timestamp}"
    write_outputs(out_dir, data)

    print(f"\nDone. Story folder: {out_dir}")
    print("Next: python generate_audio.py --story-dir", out_dir)


if __name__ == "__main__":
    main()
