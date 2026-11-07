#!/usr/bin/env python3
"""Make a word-level transcript JSON from a video with local whisper.cpp (free, offline).

Usage: python3 whisper_words.py <video> [--model ~/whisper-models/ggml-medium.bin] [--lang auto]
Writes <video-stem>.json next to the video: {"words": [{"text","start","end","type"}], "audio_duration_secs"}
That is the shape cut-silences and cut-mistakes expect.
"""
import json, os, subprocess, sys, tempfile

def main():
    args = sys.argv[1:]
    if not args:
        sys.exit(__doc__)
    video = os.path.abspath(args[0])
    model = os.path.expanduser("~/whisper-models/ggml-base.en.bin")
    lang = "en"
    if "--model" in args:
        model = os.path.expanduser(args[args.index("--model") + 1])
    if "--lang" in args:
        lang = args[args.index("--lang") + 1]
    tmp = tempfile.mkdtemp()
    wav = os.path.join(tmp, "a.wav")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", video, "-ar", "16000", "-ac", "1", wav], check=True)
    base = os.path.join(tmp, "out")
    # -ml 1 + -sow: one word per segment, split on words not tokens
    subprocess.run(["whisper-cli", "-m", model, "-l", lang, "-ml", "1", "-sow", "-oj", "-of", base, "-f", wav],
                   check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    data = json.load(open(base + ".json"))
    words = []
    for seg in data.get("transcription", []):
        t = seg.get("text", "").strip()
        if not t:
            continue
        words.append({"text": t, "start": seg["offsets"]["from"] / 1000, "end": seg["offsets"]["to"] / 1000, "type": "word"})
    dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of",
                                "default=nw=1:nk=1", video], capture_output=True, text=True).stdout.strip() or 0)
    out = os.path.splitext(video)[0] + ".json"
    json.dump({"words": words, "audio_duration_secs": dur}, open(out, "w"), indent=1)
    print(json.dumps({"transcript": out, "words": len(words), "duration": dur}))

if __name__ == "__main__":
    main()
