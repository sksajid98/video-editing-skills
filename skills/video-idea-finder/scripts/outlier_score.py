#!/usr/bin/env python3
"""Rank outlier videos: views divided by the channel's median views, so a small channel's breakout
beats a big channel's normal video.

Usage: python3 outlier_score.py videos.csv [--days 30] [--top 10] [--min-multiple 2]
CSV columns: channel,title,url,views,published (YYYY-MM-DD),channel_median_views
  channel_median_views may be blank: it is then the median of that channel's rows in the CSV
  (needs 5+ rows for that channel, otherwise the row is skipped and reported).
Prints a Markdown table, best outliers first.
"""
import csv, statistics, sys
from datetime import date, timedelta

def num(s):
    s = (s or "").strip().lower().replace(",", "")
    mult = 1
    for suf, m in (("k", 1e3), ("m", 1e6), ("b", 1e9)):
        if s.endswith(suf):
            s, mult = s[:-1], m
    return float(s) * mult if s else None

def main():
    a = sys.argv[1:]
    if not a:
        sys.exit(__doc__)
    opt = lambda k, d: float(a[a.index(k) + 1]) if k in a else d
    days, top, min_mult = opt("--days", 30), int(opt("--top", 10)), opt("--min-multiple", 2)
    rows = list(csv.DictReader(open(a[0], newline="", encoding="utf-8")))
    by_ch = {}
    for r in rows:
        v = num(r.get("views"))
        if v is not None:
            by_ch.setdefault(r["channel"].strip(), []).append(v)
    cutoff = date.today() - timedelta(days=days)
    out, skipped = [], []
    for r in rows:
        v = num(r.get("views"))
        try:
            pub = date.fromisoformat(r["published"].strip())
        except Exception:
            skipped.append((r.get("title", "?"), "bad or missing date")); continue
        if v is None or pub < cutoff:
            continue
        med = num(r.get("channel_median_views"))
        if med is None:
            ch = by_ch.get(r["channel"].strip(), [])
            if len(ch) < 5:
                skipped.append((r["title"], "no channel median and under 5 videos for it")); continue
            med = statistics.median(ch)
        if med <= 0:
            continue
        m = v / med
        if m >= min_mult:
            out.append((m, r, v, med, pub))
    out.sort(key=lambda x: -x[0])
    print("| # | Multiple | Views | Channel median | Published | Channel | Title |")
    print("|---|---|---|---|---|---|---|")
    for i, (m, r, v, med, pub) in enumerate(out[:top], 1):
        print(f"| {i} | {m:.1f}x | {v:,.0f} | {med:,.0f} | {pub} | {r['channel']} | [{r['title']}]({r.get('url','')}) |")
    if len(out) < top:
        print(f"\nOnly {len(out)} video(s) at {min_mult:g}x or more in the last {days:g} days.")
    for t, why in skipped:
        print(f"skipped: {t} ({why})")

if __name__ == "__main__":
    main()
