#!/usr/bin/env bash
# intake.sh <video> [<video> ...] --project "<Project name>"
# Creates the project folder, copies sources, probes them, extracts 16 kHz audio, transcribes (Hindi + English gloss),
# detects scene cuts and makes a 1 fps contact sheet per source. Prints a JSON summary.
set -euo pipefail
PROJ=""; FILES=()
while [ $# -gt 0 ]; do case "$1" in --project) PROJ="$2"; shift 2;; *) FILES+=("$1"); shift;; esac; done
[ -z "$PROJ" ] && PROJ="$(basename "${FILES[0]%.*}")"
ROOT="${VAE_ROOT:-/Users/sajid.ali/Documents/Claude}/$PROJ"
mkdir -p "$ROOT"/{source,analysis,storyboard,graphics,broll,audio,renders,exports}
MODEL=~/whisper-models/ggml-medium.bin; [ -f "$MODEL" ] || MODEL=~/whisper-models/ggml-base.bin
echo "{\"project\":\"$ROOT\",\"sources\":["
first=1
for f in "${FILES[@]}"; do
  b="$(basename "$f")"; n="${b%.*}"; cp -n "$f" "$ROOT/source/" 2>/dev/null || true
  A="$ROOT/analysis/$n"; mkdir -p "$A"
  ffmpeg -v error -y -i "$f" -vn -ac 1 -ar 16000 "$A/a.wav"
  whisper-cli -m "$MODEL" -l hi -f "$A/a.wav" -osrt -ml 42 -of "$A/tr_hi" >/dev/null 2>&1 || true
  whisper-cli -m "$MODEL" -l en -f "$A/a.wav" -osrt -of "$A/tr_en" >/dev/null 2>&1 || true
  ffmpeg -v error -i "$f" -vf "select='gt(scene,0.22)',showinfo" -f null - 2>&1 | grep -o 'pts_time:[0-9.]*' | cut -d: -f2 > "$A/cuts.txt" || true
  ffmpeg -v error -y -i "$f" -vf "fps=1,scale=180:-2,tile=10x8" -frames:v 1 "$A/sheet.png" || true
  probe=$(ffprobe -v error -select_streams v:0 -show_entries stream=width,height,r_frame_rate:format=duration -of json "$f" | tr -d '\n ')
  [ $first -eq 0 ] && echo ","; first=0
  echo "{\"file\":\"$ROOT/source/$b\",\"analysis\":\"$A\",\"probe\":$probe}"
done
echo "]}"
