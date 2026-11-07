#!/usr/bin/env bash
# finish_audio.sh <in.mp4> <out.mp4>
# Two-pass loudnorm of the final mix to -14 LUFS integrated, -1 dBTP, LRA 7; video stream copied untouched.
set -euo pipefail
IN="$1"; OUT="$2"
J=$(ffmpeg -hide_banner -i "$IN" -af loudnorm=I=-14:TP=-1:LRA=7:print_format=json -f null - 2>&1 | sed -n '/^{/,/^}/p')
g(){ echo "$J" | python3 -c "import json,sys;print(json.load(sys.stdin)['$1'])"; }
ffmpeg -v error -y -i "$IN" -c:v copy -af "loudnorm=I=-14:TP=-1:LRA=7:measured_I=$(g input_i):measured_TP=$(g input_tp):measured_LRA=$(g input_lra):measured_thresh=$(g input_thresh):offset=$(g target_offset):linear=true,aresample=48000" -c:a aac -b:a 320k "$OUT"
echo "done: $OUT"
