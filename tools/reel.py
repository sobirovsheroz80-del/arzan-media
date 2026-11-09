#!/usr/bin/env python3
"""Reel generator for arzantarifkz: text-card reels 1080x1920 with optional Piper voice.

Usage: python3 reel.py spec.json out.mp4 [--cover cover.jpg]
Spec: {"voice": "path.onnx" | null, "scenes": [{"lines": [...], "say": "...", "min": 3.0}]}
Each line: {"t": "text", "size": 120, "color": "#fff", "weight": "black", "gap": 30, "pill": "#F5C400"}
"""
import json, math, os, subprocess, sys, tempfile, wave
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H, FPS = 1080, 1920, 30
BG = (14, 14, 14)
YELLOW = (245, 196, 0)
WHITE = (255, 255, 255)
GREY = (170, 170, 170)
FONTS = {"black": "/usr/share/fonts/opentype/inter/Inter-Black.otf",
         "extrabold": "/usr/share/fonts/opentype/inter/Inter-ExtraBold.otf",
         "bold": "/usr/share/fonts/opentype/inter/Inter-Bold.otf",
         "semibold": "/usr/share/fonts/opentype/inter/Inter-SemiBold.otf",
         "medium": "/usr/share/fonts/opentype/inter/Inter-Medium.otf"}
_fc = {}
def font(weight, size):
    k = (weight, size)
    if k not in _fc: _fc[k] = ImageFont.truetype(FONTS[weight], size)
    return _fc[k]

def hexc(s):
    s = s.lstrip("#"); return tuple(int(s[i:i+2], 16) for i in (0, 2, 4))

def ease(t):  # ease-out cubic
    t = max(0.0, min(1.0, t)); return 1 - (1 - t) ** 3

def wrap(draw, text, f, maxw):
    words, lines, cur = text.split(), [], ""
    for w in words:
        test = (cur + " " + w).strip()
        if draw.textlength(test, font=f) <= maxw or not cur: cur = test
        else: lines.append(cur); cur = w
    if cur: lines.append(cur)
    return lines

def layout(scene):
    """Pre-measure lines: returns list of (line, font, wrapped_lines, height)."""
    d = ImageDraw.Draw(Image.new("RGB", (W, H)))
    items, total = [], 0
    for ln in scene["lines"]:
        f = font(ln.get("weight", "black"), ln.get("size", 110))
        maxw = W - 2 * ln.get("margin", 90)
        if "l" in ln:
            ln = dict(ln); ln["t"] = ln["l"]; rows = [ln["l"]]
        else:
            rows = wrap(d, ln["t"], f, maxw)
        lh = int(ln.get("size", 110) * 1.12)
        h = lh * len(rows) + (ln.get("pad", 0) * 2 if ln.get("pill") else 0)
        items.append((ln, f, rows, h, lh)); total += h + ln.get("gap", 36)
    return items, total - (scene["lines"][-1].get("gap", 36) if scene["lines"] else 0)

def draw_scene(scene, t_in, brand=True):
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    # soft yellow glow top-left for depth
    glow = Image.new("RGB", (W, H), BG)
    gd = ImageDraw.Draw(glow); gd.ellipse((-500, -600, 700, 500), fill=(60, 50, 10))
    glow = glow.filter(ImageFilter.GaussianBlur(220)); img = Image.blend(img, glow, 0.9); d = ImageDraw.Draw(img)
    if brand:
        f = font("bold", 40); txt = "ARZAN TARIF"
        tw = d.textlength(txt, font=f); x0 = (W - tw) / 2 - 34; y0 = 150
        d.rounded_rectangle((x0, y0, x0 + tw + 68, y0 + 74), radius=37, fill=YELLOW)
        d.text((x0 + 34, y0 + 14), txt, font=f, fill=(20, 20, 20))
    items, total = layout(scene)
    y = (H - total) / 2 + scene.get("yshift", 0)
    for i, (ln, f, rows, h, lh) in enumerate(items):
        delay = i * 0.14; p = ease((t_in - delay) / 0.38)
        if p <= 0: y += h + ln.get("gap", 36); continue
        dy = (1 - p) * 70; col = hexc(ln["color"]) if "color" in ln else WHITE
        alpha = p
        layer = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ld = ImageDraw.Draw(layer)
        yy = y + dy
        if ln.get("pill"):
            pad = ln.get("pad", 26); tw = max(ld.textlength(r, font=f) for r in rows)
            ld.rounded_rectangle(((W - tw) / 2 - 44, yy, (W + tw) / 2 + 44, yy + h), radius=ln.get("radius", 40), fill=hexc(ln["pill"]))
            yy += pad
        if "l" in ln:                                   # two-column price row
            tw = ln.get("width", 820); x0 = (W - tw) / 2
            ld.text((x0, yy), ln["l"], font=f, fill=col + (255,))
            rf = font(ln.get("rweight", "black"), ln.get("rsize", ln.get("size", 110)))
            rw = ld.textlength(ln["r"], font=rf); rcol = hexc(ln["rcolor"]) if "rcolor" in ln else YELLOW
            ld.text((x0 + tw - rw, yy - (rf.size - f.size) * 0.55), ln["r"], font=rf, fill=rcol + (255,))
            yy += lh
        else:
          for r in rows:
            tw = ld.textlength(r, font=f)
            x = (W - tw) / 2 if ln.get("align", "center") == "center" else ln.get("margin", 90)
            ld.text((x, yy), r, font=f, fill=col + (255,)); yy += lh
        if alpha < 1:
            a = layer.split()[3].point(lambda v: int(v * alpha)); layer.putalpha(a)
        img.paste(layer, (0, 0), layer)
        y += h + ln.get("gap", 36)
    return img

def tts(text, model, out):
    subprocess.run([sys.executable, "-m", "piper", "-m", model, "-f", out, "--length-scale", "0.88", "--sentence-silence", "0.25"], input=text.encode(), check=True, capture_output=True)
    with wave.open(out) as w: return w.getnframes() / w.getframerate()

def main():
    spec = json.load(open(sys.argv[1], encoding="utf-8")); out = sys.argv[2]
    cover = sys.argv[sys.argv.index("--cover") + 1] if "--cover" in sys.argv else None
    td = tempfile.mkdtemp(); durs, wavs = [], []
    for i, sc in enumerate(spec["scenes"]):
        if spec.get("voice") and sc.get("say"):
            w = os.path.join(td, f"s{i}.wav"); a = tts(sc["say"], spec["voice"], w)
            durs.append(max(sc.get("min", 2.5), a + sc.get("tail", 0.5))); wavs.append((w, a))
        else:
            durs.append(sc.get("min", 3.0)); wavs.append(None)
    total_frames = int(sum(durs) * FPS)
    # audio track: each scene's voice starts at scene start, silence otherwise
    if any(wavs):
        sr = 22050
        with wave.open(wavs[[i for i, w in enumerate(wavs) if w][0]][0]) as w0: sr = w0.getframerate()
        mix = bytearray(b"\x00\x00" * int(sum(durs) * sr)); pos = 0
        for d, w in zip(durs, wavs):
            if w:
                with wave.open(w[0]) as wf: data = wf.readframes(wf.getnframes())
                start = int(pos * sr) * 2; mix[start:start + len(data)] = data
            pos += d
        apath = os.path.join(td, "voice.wav")
        with wave.open(apath, "wb") as wf: wf.setnchannels(1); wf.setsampwidth(2); wf.setframerate(sr); wf.writeframes(bytes(mix))
    else:
        apath = None
    cmd = ["ffmpeg", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-"]
    if apath: cmd += ["-i", apath]
    else: cmd += ["-f", "lavfi", "-i", "anullsrc=r=44100:cl=mono"]
    cmd += ["-shortest", "-c:v", "libx264", "-preset", "veryfast", "-crf", "21", "-pix_fmt", "yuv420p", "-r", str(FPS),
            "-c:a", "aac", "-b:a", "96k", "-ar", "44100", "-movflags", "+faststart", "-t", f"{sum(durs):.3f}", out]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE, stderr=subprocess.DEVNULL)
    t = 0.0; cover_img = None
    for sc, d in zip(spec["scenes"], durs):
        n = int(round(d * FPS))
        for k in range(n):
            img = draw_scene(sc, k / FPS)
            if cover_img is None and k / FPS >= 1.2: cover_img = img
            p.stdin.write(img.tobytes())
    p.stdin.close(); p.wait()
    if cover and cover_img: cover_img.save(cover, quality=92)
    print(json.dumps({"out": out, "seconds": round(sum(durs), 2), "scenes": [round(x, 2) for x in durs]}))

if __name__ == "__main__":
    main()
