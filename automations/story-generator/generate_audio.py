"""
generate_audio.py
-----------------
Take a story folder produced by generate_story.py and render an MP3
narrated by a single TTS voice.

Run:
    python generate_audio.py --story-dir outputs/<slug>-<timestamp>
    python generate_audio.py --story-dir outputs/... --voice nova
"""

from __future__ import annotations

import argparse
import logging
import os
import re
import sys
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

# Keep each TTS request well under the API limit (~4096 chars).
MAX_CHUNK_CHARS = 3500


def load_transcript(story_dir: Path) -> str:
    """Prefer story.json (cleaner text); fall back to transcript.md."""
    story_json = story_dir / "story.json"
    if story_json.exists():
        import json

        data = json.loads(story_json.read_text(encoding="utf-8"))
        text = data.get("transcript") or data.get("story") or ""
        if text:
            return text.strip()

    transcript_md = story_dir / "transcript.md"
    if transcript_md.exists():
        text = transcript_md.read_text(encoding="utf-8")
        # Strip the leading markdown title (first line starting with #)
        text = re.sub(r"^#.*\n", "", text, count=1).strip()
        return text

    sys.exit(f"Error: no transcript found in {story_dir}")


def chunk_text(text: str, max_chars: int = MAX_CHUNK_CHARS) -> list[str]:
    """Split on paragraph boundaries so the narration flows naturally."""
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    chunks: list[str] = []
    buf = ""
    for p in paragraphs:
        if len(buf) + len(p) + 2 <= max_chars:
            buf = f"{buf}\n\n{p}" if buf else p
        else:
            if buf:
                chunks.append(buf)
            # If a single paragraph is too long, hard-split it on sentence ends.
            if len(p) > max_chars:
                sentences = re.split(r"(?<=[.!?])\s+", p)
                buf = ""
                for s in sentences:
                    if len(buf) + len(s) + 1 <= max_chars:
                        buf = f"{buf} {s}".strip()
                    else:
                        if buf:
                            chunks.append(buf)
                        buf = s
            else:
                buf = p
    if buf:
        chunks.append(buf)
    return chunks


def synthesize(client: OpenAI, model: str, voice: str, text: str, out_path: Path) -> None:
    logging.info("Synthesizing %s chars -> %s", len(text), out_path.name)
    # Streaming response is the recommended pattern for the OpenAI TTS endpoint.
    with client.audio.speech.with_streaming_response.create(
        model=model,
        voice=voice,
        input=text,
        response_format="mp3",
    ) as response:
        response.stream_to_file(str(out_path))


def concat_mp3s(parts: list[Path], out_path: Path) -> None:
    """Naive byte-level concatenation. Works for MP3 because frames are independent;
    quality is fine for narration. Use ffmpeg if you need gapless mastering."""
    with open(out_path, "wb") as out:
        for p in parts:
            out.write(p.read_bytes())
    logging.info("Combined %d chunks -> %s", len(parts), out_path)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Render a story folder to MP3.")
    p.add_argument("--story-dir", required=True, help="Folder produced by generate_story.py")
    p.add_argument("--voice", help="OpenAI TTS voice (alloy, echo, fable, onyx, nova, shimmer, ...).")
    p.add_argument("--model", help="Override the TTS model.")
    p.add_argument("--keep-parts", action="store_true", help="Keep per-chunk MP3 files for debugging.")
    return p.parse_args()


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    load_dotenv()

    if not os.getenv("OPENAI_API_KEY"):
        sys.exit("Error: OPENAI_API_KEY not set (see .env.example).")

    args = parse_args()
    story_dir = Path(args.story_dir)
    if not story_dir.is_dir():
        sys.exit(f"Error: {story_dir} is not a directory.")

    model = args.model or os.getenv("TTS_MODEL", "gpt-4o-mini-tts")
    voice = args.voice or os.getenv("TTS_VOICE", "alloy")

    text = load_transcript(story_dir)
    chunks = chunk_text(text)
    logging.info("Transcript: %d chars, %d chunk(s)", len(text), len(chunks))

    client = OpenAI()
    parts_dir = story_dir / "_audio_parts"
    parts_dir.mkdir(exist_ok=True)
    part_paths: list[Path] = []
    for i, chunk in enumerate(chunks, 1):
        part = parts_dir / f"part-{i:03d}.mp3"
        synthesize(client, model, voice, chunk, part)
        part_paths.append(part)

    final = story_dir / "narration.mp3"
    if len(part_paths) == 1:
        final.write_bytes(part_paths[0].read_bytes())
    else:
        concat_mp3s(part_paths, final)

    if not args.keep_parts:
        for p in part_paths:
            p.unlink(missing_ok=True)
        parts_dir.rmdir()

    print(f"\nDone. Narration: {final}")


if __name__ == "__main__":
    main()
