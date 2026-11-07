# Make a native Premiere text graphic (.mogrt, Premiere-built) from Premiere's stock "Basic Title":
# sets the text, font, size, fill colour, tracking and drop shadow in the title's own text style. No After Effects.
# Usage (module): make(out_path, text, font, size, rgb_hex, tracking=0, shadow=True, name=None)
import zipfile, io, gzip, re, base64, json, uuid, os
BASIC = "/Applications/Adobe Premiere Pro 2026/Adobe Premiere Pro 2026.app/Contents/Essential Graphics/Basic Title.mogrt"
BLOB = re.compile(r'(<StartKeyframeValue[^>]*>)([A-Za-z0-9+/=\s]+)(</StartKeyframeValue>)')

def _objset(xml, oid, val):
    def f(m):
        return re.sub(r"<StartKeyframe>(-91445760000000000),[^,]*,", lambda k: "<StartKeyframe>%s,%s," % (k.group(1), val), m.group(0), count=1)
    return re.sub(r'<(VideoComponentParam|PointComponentParam) ObjectID="%d".*?</\1>' % oid, f, xml, flags=re.S)
def _rehash(xml):
    """give every StartKeyframeValue a fresh BinaryHash whose last field is len(blob)+12, as Premiere writes it"""
    def f(m):
        raw = base64.b64decode(re.sub(r"\s", "", m.group(2)))
        u = uuid.uuid4().hex
        h = "%s-%s-%s-%s-%s%08x" % (u[:8], u[8:12], u[12:16], u[16:20], u[20:24], len(raw) + 12)
        return '<StartKeyframeValue Encoding="base64" BinaryHash="%s">' % h + m.group(2) + "</StartKeyframeValue>"
    return re.sub(r'<StartKeyframeValue Encoding="base64" BinaryHash="[^"]*">([^<]*)</StartKeyframeValue>'.replace("([^<]*)", "()([^<]*)"), f, xml)
def color_int(hexs, order="rgb"):
    r, g, b = int(hexs[1:3], 16), int(hexs[3:5], 16), int(hexs[5:7], 16)
    return (r << 16 | g << 8 | b) if order == "rgb" else (b << 16 | g << 8 | r)
def make(out, text, font, size, rgb, tracking=0, shadow=True, name=None, order="rgb", sh_op=45, sh_off=6, sh_blur=6):
    z = zipfile.ZipFile(BASIC); files = {n: z.read(n) for n in z.namelist()}
    pgz = zipfile.ZipFile(io.BytesIO(files["project.prgraphic"])); pgf = {n: pgz.read(n) for n in pgz.namelist()}
    pn = [n for n in pgf if n.endswith(".prproj")][0]; xml = gzip.decompress(pgf[pn]).decode("utf-8")
    def repl(m):
        raw = base64.b64decode(re.sub(r"\s", "", m.group(2)))
        if b"m\x00T\x00e\x00x\x00t" not in raw: return m.group(0)
        n = int.from_bytes(raw[:4], "little"); j = json.loads(raw[8:8 + n].decode("utf-16le"))
        tp = j["mTextParam"]; ss = tp["mStyleSheet"]
        ss["mText"] = text
        ss["mFontName"]["mParamValues"] = [[0, font]]
        ss["mFontSize"]["mParamValues"] = [[0, size]]
        ss["mFillColor"]["mParamValues"] = [[0, color_int(rgb, order)]]
        ss["mTracking"]["mParamValues"] = [[0, tracking]]
        tp["mAlignment"] = 2
        tp.update(mShadowVisible=bool(shadow), mShadowAngle=135, mShadowOffset=sh_off, mShadowBlur=sh_blur, mShadowOpacity=sh_op, mShadowColor=0, mShadowSize=0)
        body = json.dumps(j, separators=(",", ":")).encode("utf-16le")
        return m.group(1) + base64.b64encode(len(body).to_bytes(4, "little") + b"\0\0\0\0" + body).decode() + m.group(3)
    xml2 = _rehash(BLOB.sub(repl, xml))
    pgf[pn] = gzip.compress(xml2.encode("utf-8"))
    bio = io.BytesIO(); zo = zipfile.ZipFile(bio, "w", zipfile.ZIP_DEFLATED)
    for n, d in pgf.items(): zo.writestr(n, d)
    zo.close(); files["project.prgraphic"] = bio.getvalue()
    d = json.loads(files["definition.json"].decode("utf-8-sig"))
    d["capsuleID"] = str(uuid.uuid4())
    label = name or text
    d["capsuleName"] = label
    if isinstance(d.get("capsuleNameLocalized"), dict):
        for e in d["capsuleNameLocalized"].get("strDB", []): e["str"] = label
    for c in d.get("clientControls", []):
        if c.get("type") == 6 and isinstance(c.get("value"), dict):
            for e in c["value"].get("strDB", []): e["str"] = text
    files["definition.json"] = json.dumps(d).encode("utf-8")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    zo = zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED)
    for n, data in files.items():
        if re.match(r"project_[A-Za-z]{2}_[A-Za-z]{2}\.prgraphic$", n): continue
        zo.writestr(n, data)
    zo.close(); return out
if __name__ == "__main__":
    import sys
    D = "/Users/sajid.ali/Documents/PROJECTS/2026/November/SJ 0022 BPXJ 0 2026-11-05 Sonia 0 IN/6. VFX + AE/Hook 1 v1 Premiere build/pr_text/"
    print(make(D + "TEST WARM WATER.mogrt", "WARM WATER", "InterTight-Black", 84, "#FFFFFF", -10))
    print(make(D + "TEST RED.mogrt", "RED TEST", "InterTight-Black", 84, "#E8262C", 0, order="rgb"))

# ---------- text + box (from Premiere's stock "Simple Web Caption": one text layer + one box pinned to it) ----------
CAPTION = "/Applications/Adobe Premiere Pro 2026/Adobe Premiere Pro 2026.app/Contents/Essential Graphics/Captions and Subtitles/Simple Web Caption.mogrt"
def make_box(out, text, font, size, text_rgb, box_rgb, tracking=0, text_shadow=False, box_shadow=True, name=None, stroke_rgb=None, stroke_w=0, box_op=100, box_dy=0.0, box_vs=100.0):
    z = zipfile.ZipFile(CAPTION); files = {n: z.read(n) for n in z.namelist()}
    pgz = zipfile.ZipFile(io.BytesIO(files["project.prgraphic"])); pgf = {n: pgz.read(n) for n in pgz.namelist()}
    pn = [n for n in pgf if n.endswith(".prproj")][0]; xml = gzip.decompress(pgf[pn]).decode("utf-8")
    def enc(j):
        body = json.dumps(j, separators=(",", ":")).encode("utf-16le")
        return base64.b64encode(len(body).to_bytes(4, "little") + b"\0\0\0\0" + body).decode()
    def repl(m):
        raw = base64.b64decode(re.sub(r"\s", "", m.group(2)))
        if len(raw) < 8: return m.group(0)
        n = int.from_bytes(raw[:4], "little")
        try: j = json.loads(raw[8:8 + n].decode("utf-16le"))
        except Exception: return m.group(0)
        if "mTextParam" in j:
            tp = j["mTextParam"]; ss = tp["mStyleSheet"]
            ss["mText"] = text; ss["mFontName"]["mParamValues"] = [[0, font]]; ss["mFontSize"]["mParamValues"] = [[0, size]]
            ss["mFillColor"]["mParamValues"] = [[0, color_int(text_rgb)]]; ss["mTracking"]["mParamValues"] = [[0, tracking]]
            tp.update(mShadowVisible=bool(text_shadow), mShadowAngle=135, mShadowOffset=6, mShadowBlur=6, mShadowOpacity=45, mShadowColor=0)
        elif "mStyle" in j:
            st = j["mStyle"]; st["mFillColor"] = color_int(box_rgb); st["mFillVisible"] = True
            st.update(mShadowVisible=bool(box_shadow), mShadowAngle=135, mShadowOffset=10, mShadowBlur=24, mShadowOpacity=30, mShadowColor=0)
            if stroke_rgb: st.update(mStrokeVisible=True, mStrokeColor=color_int(stroke_rgb), mStrokeWidth=stroke_w)
        else: return m.group(0)
        return m.group(1) + enc(j) + m.group(3)
    xml2 = BLOB.sub(repl, xml)
    # static: drop the template's fade-in/out and bounce keyframes (house rule: no fades), keep the rest pose
    def unanim(m):
        b = m.group(0)
        if "<Keyframes>" not in b: return b
        nm = re.search(r"<Name>([^<]*)</Name>", b).group(1)
        rest = "-91445760000000000,100.,0,0,0,0,0,0" if nm == "Opacity" else "-91445760000000000,0.49895831942558289,-0.081451416015625,0,0"
        b = re.sub(r"<Keyframes>[^<]*</Keyframes>\s*", "", b)
        b = re.sub(r"<StartKeyframe>[^<]*</StartKeyframe>", "<StartKeyframe>" + rest + "</StartKeyframe>", b)
        b = b.replace("<IsTimeVarying>true</IsTimeVarying>", "<IsTimeVarying>false</IsTimeVarying>")
        return b
    xml2 = re.sub(r"<(VideoComponentParam|PointComponentParam)\b[^>]*>.*?</\1>", unanim, xml2, flags=re.S)
    xml2 = xml2.replace("<StartKeyframe>-91445760000000000,29.692832946777,0,0,0,0,0,0</StartKeyframe>", "<StartKeyframe>-91445760000000000,%s,0,0,0,0,0,0</StartKeyframe>" % repr(float(box_op)))
    if box_vs != 100.0: xml2 = _objset(xml2, 114, repr(float(box_vs)))
    if box_dy: xml2 = xml2.replace("-91445760000000000,-0.011120617389678955,-0.095372498035430908,", "-91445760000000000,-0.011120617389678955,%r," % (-0.095372498035430908 + box_dy))
    xml2 = _rehash(xml2)
    pgf[pn] = gzip.compress(xml2.encode("utf-8"))
    bio = io.BytesIO(); zo = zipfile.ZipFile(bio, "w", zipfile.ZIP_DEFLATED)
    for n, d in pgf.items(): zo.writestr(n, d)
    zo.close(); files["project.prgraphic"] = bio.getvalue()
    d = json.loads(files["definition.json"].decode("utf-8-sig")); d["capsuleID"] = str(uuid.uuid4()); label = name or text; d["capsuleName"] = label
    if isinstance(d.get("capsuleNameLocalized"), dict):
        for e in d["capsuleNameLocalized"].get("strDB", []): e["str"] = label
    for c in d.get("clientControls", []):
        if c.get("type") == 6 and isinstance(c.get("value"), dict):
            for e in c["value"].get("strDB", []): e["str"] = text
    files["definition.json"] = json.dumps(d).encode("utf-8")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    zo = zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED)
    for n, data in files.items():
        if re.match(r"project_[A-Za-z]{2}_[A-Za-z]{2}\.prgraphic$", n): continue
        zo.writestr(n, data)
    zo.close(); return out

# ---------- box / shape only (Simple Web Caption with its text hidden and the box un-pinned, drawn to an exact size) ----------
import struct, math
def _path(w, h, r=0, skew_deg=0, cx=723.0, cy=94.0):
    """closed path centred on (cx, cy) in template px; rounded corners via bezier handles; skewX like CSS."""
    k = 0.5523 * r; x0, x1, y0, y1 = cx - w / 2, cx + w / 2, cy - h / 2, cy + h / 2
    if r <= 0: V = [(x0, y0, x0, y0, x0, y0), (x1, y0, x1, y0, x1, y0), (x1, y1, x1, y1, x1, y1), (x0, y1, x0, y1, x0, y1)]
    else:
        V = [(x0 + r, y0, x0 + r - k, y0, x0 + r, y0), (x1 - r, y0, x1 - r, y0, x1 - r + k, y0),
             (x1, y0 + r, x1, y0 + r - k, x1, y0 + r), (x1, y1 - r, x1, y1 - r, x1, y1 - r + k),
             (x1 - r, y1, x1 - r + k, y1, x1 - r, y1), (x0 + r, y1, x0 + r, y1, x0 + r - k, y1),
             (x0, y1 - r, x0, y1 - r + k, x0, y1 - r), (x0, y0 + r, x0, y0 + r, x0, y0 + r - k)]
    t = math.tan(math.radians(-skew_deg)) if skew_deg else 0
    sk = lambda x, y: x + (y - cy) * t * -1
    out = struct.pack("<II", 2, len(V))
    for (x, y, ix, iy, ox, oy) in V: out += struct.pack("<7f", 0, sk(x, y), y, sk(ix, iy), iy, sk(ox, oy), oy)
    return out + b"\x01"
def make_shape(out, w, h, fill_rgb, r=0, op=100, stroke_rgb=None, stroke_w=0, skew_deg=0, shadow=True, name="Box", sh_op=30, sh_off=10, sh_blur=24, sh_col="#000000"):
    """w, h, r, stroke_w in frame px (1080x1920); converted to the template's 1920x1080 space."""
    S = 1920 / 1080; w, h, r, stroke_w = w * S, h * S, r * S, stroke_w * S
    z = zipfile.ZipFile(CAPTION); files = {n: z.read(n) for n in z.namelist()}
    pgz = zipfile.ZipFile(io.BytesIO(files["project.prgraphic"])); pgf = {n: pgz.read(n) for n in pgz.namelist()}
    pn = [n for n in pgf if n.endswith(".prproj")][0]; xml = gzip.decompress(pgf[pn]).decode("utf-8")
    def enc(j):
        body = json.dumps(j, separators=(",", ":")).encode("utf-16le")
        return base64.b64encode(len(body).to_bytes(4, "little") + b"\0\0\0\0" + body).decode()
    def repl(m):
        raw = base64.b64decode(re.sub(r"\s", "", m.group(2)))
        if raw[:8] == struct.pack("<II", 2, 4) and len(raw) == 121: return m.group(1) + base64.b64encode(_path(w, h, r, skew_deg)).decode() + m.group(3)
        if len(raw) < 8: return m.group(0)
        n = int.from_bytes(raw[:4], "little")
        try: j = json.loads(raw[8:8 + n].decode("utf-16le"))
        except Exception: return m.group(0)
        if "mTextParam" in j:
            j["mTextParam"]["mStyleSheet"]["mText"] = " "; j["mTextParam"]["mShadowVisible"] = False
        elif "mStyle" in j:
            st = j["mStyle"]; st["mFillColor"] = color_int(fill_rgb); st["mFillVisible"] = True
            st.update(mShadowVisible=bool(shadow), mShadowAngle=90, mShadowOffset=sh_off, mShadowBlur=sh_blur, mShadowOpacity=sh_op, mShadowColor=color_int(sh_col))
            st.update(mStrokeVisible=bool(stroke_rgb), mStrokeColor=color_int(stroke_rgb or "#FFFFFF"), mStrokeWidth=stroke_w or 1)
        else: return m.group(0)
        return m.group(1) + enc(j) + m.group(3)
    xml2 = BLOB.sub(repl, xml)
    def unanim(m):
        b = m.group(0)
        if "<Keyframes>" not in b: return b
        nm = re.search(r"<Name>([^<]*)</Name>", b).group(1)
        rest = "-91445760000000000,100.,0,0,0,0,0,0" if nm == "Opacity" else "-91445760000000000,0.49895831942558289,-0.081451416015625,0,0"
        b = re.sub(r"<Keyframes>[^<]*</Keyframes>\s*", "", b); b = re.sub(r"<StartKeyframe>[^<]*</StartKeyframe>", "<StartKeyframe>" + rest + "</StartKeyframe>", b)
        return b.replace("<IsTimeVarying>true</IsTimeVarying>", "<IsTimeVarying>false</IsTimeVarying>")
    xml2 = re.sub(r"<(VideoComponentParam|PointComponentParam)\b[^>]*>.*?</\1>", unanim, xml2, flags=re.S)
    xml2 = xml2.replace("<StartKeyframe>-91445760000000000,29.692832946777,0,0,0,0,0,0</StartKeyframe>", "<StartKeyframe>-91445760000000000,%s,0,0,0,0,0,0</StartKeyframe>" % repr(float(op)))
    xml2 = re.sub(r"\s*<ComponentPinMap ObjectRef=\"\d+\"/>", "", xml2)          # un-pin: the box keeps the drawn size
    pgf[pn] = gzip.compress(xml2.encode("utf-8"))
    bio = io.BytesIO(); zo = zipfile.ZipFile(bio, "w", zipfile.ZIP_DEFLATED)
    for n, d in pgf.items(): zo.writestr(n, d)
    zo.close(); files["project.prgraphic"] = bio.getvalue()
    d = json.loads(files["definition.json"].decode("utf-8-sig")); d["capsuleID"] = str(uuid.uuid4()); d["capsuleName"] = name
    if isinstance(d.get("capsuleNameLocalized"), dict):
        for e in d["capsuleNameLocalized"].get("strDB", []): e["str"] = name
    for c in d.get("clientControls", []):
        if c.get("type") == 6 and isinstance(c.get("value"), dict):
            for e in c["value"].get("strDB", []): e["str"] = " "
    files["definition.json"] = json.dumps(d).encode("utf-8")
    zo = zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED)
    for n, data in files.items():
        if re.match(r"project_[A-Za-z]{2}_[A-Za-z]{2}\.prgraphic$", n): continue
        zo.writestr(n, data)
    zo.close(); return out
