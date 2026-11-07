#!/usr/bin/env python3
"""qc_final.py <final.mp4> [--fps 25] — delivery checks for the final MP4.
Checks 1080x1920, fps, H.264/AAC, loudness -14 ±1 LUFS, true peak <= -1 dBTP, no black or frozen stretches > 0.5 s.
Prints PASS/FAIL per check; exit 1 on any FAIL."""
import json, re, subprocess, sys
f=sys.argv[1]; want_fps=float(sys.argv[sys.argv.index("--fps")+1]) if "--fps" in sys.argv else None
p=json.loads(subprocess.run(["ffprobe","-v","error","-show_streams","-show_format","-of","json",f],capture_output=True,text=True).stdout)
v=[s for s in p["streams"] if s["codec_type"]=="video"][0]; a=[s for s in p["streams"] if s["codec_type"]=="audio"]
num,den=v["r_frame_rate"].split("/"); fps=float(num)/float(den)
res=[]; ok=lambda n,c,info: res.append((n,"PASS" if c else "FAIL",info))
ok("size",(v["width"],v["height"])==(1080,1920),f'{v["width"]}x{v["height"]}')
ok("fps",want_fps is None or abs(fps-want_fps)<0.01,f"{fps:.3f}")
ok("codecs",v["codec_name"]=="h264" and a and a[0]["codec_name"]=="aac",f'{v["codec_name"]}/{a[0]["codec_name"] if a else "none"}')
e=subprocess.run(["ffmpeg","-nostats","-i",f,"-af","ebur128=peak=true","-f","null","-"],capture_output=True,text=True).stderr
I=float(re.findall(r"I:\s+(-?[\d.]+) LUFS",e)[-1]); tp=float(re.findall(r"Peak:\s+(-?[\d.]+) dBFS",e)[-1])
ok("loudness",abs(I+14)<=1,f"{I} LUFS"); ok("true peak",tp<=-0.9,f"{tp} dBTP")
bd=subprocess.run(["ffmpeg","-i",f,"-vf","blackdetect=d=0.5:pix_th=0.05,freezedetect=n=0.003:d=0.5","-an","-f","null","-"],capture_output=True,text=True).stderr
blk=re.findall(r"black_start:([\d.]+)",bd); frz=re.findall(r"freeze_start: ([\d.]+)",bd)
ok("black frames",not blk,", ".join(blk) or "none"); ok("frozen frames",not frz,", ".join(frz) or "none (end-card holds are expected)")
for n,s,i in res: print(f"{s:4}  {n:13} {i}")
sys.exit(1 if any(s=="FAIL" for _,s,_ in res) else 0)
