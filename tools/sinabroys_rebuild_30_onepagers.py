#!/usr/bin/env python3
"""Rebuild 30 ONEPAGER images from ChatGPT's already-published post texts.

This is a FALLBACK when the original chat ZIP cannot reach the PC.
It regenerates new images (not byte-identical to the original PNGs).
Never edits post copy and never schedules X/Buffer.
Requires Python 3, Pillow, Korean font and the user's existing gh login.
"""
import argparse, hashlib, re, subprocess, tempfile, time, urllib.request
from pathlib import Path

REPO = "ceoYS/x-publishing-media"
DATE = "20261110"
SOURCE = f"https://raw.githubusercontent.com/{REPO}/main/content/sinabroys/{DATE}/GROKBOT_FULL_30_POSTS_AND_IMAGES.md"
TARGET_DIR = f"media/images/sinabroys/{DATE}"
COLORS = ["#6954B7", "#387F9B", "#9B6C32", "#3D8271", "#A0506C", "#636C9C"]

def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "SinaBroys-Onepager/1.0"})
    with urllib.request.urlopen(req, timeout=45) as res:
        return res.read()

def cmd(*args, cwd=None):
    subprocess.run(args, cwd=cwd, check=True)

def font_path(bold=False):
    names = (
        ["/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc",
         "/usr/share/fonts/truetype/noto/NotoSansCJK-Bold.ttc",
         "/mnt/c/Windows/Fonts/malgunbd.ttf",
         "C:/Windows/Fonts/malgunbd.ttf"]
        if bold else
        ["/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
         "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc",
         "/mnt/c/Windows/Fonts/malgun.ttf",
         "C:/Windows/Fonts/malgun.ttf"]
    )
    return next((p for p in names if Path(p).exists()), None)

def parse(markdown):
    tags = list(re.finditer(r"(?m)^### (\d{2})\. ([^\n]+)\n", markdown))
    if len(tags) != 30:
        raise RuntimeError(f"Expected 30 entries, found {len(tags)}")
    items = []
    for i, tag in enumerate(tags):
        section = markdown[tag.end() : tags[i+1].start() if i+1 < len(tags) else len(markdown)]
        image = re.search(r"https://raw\.githubusercontent\.com/[^\s]+\.png", section)
        body = re.search(r"\*\*그대로 예약할 본문 전문 \(시작\):\*\*\s*(.*?)\s*\*\*본문 끝\.\*\*", section, re.S)
        if not image or not body:
            raise RuntimeError(f"Entry {tag.group(1)} missing original filename or post body")
        paragraphs = [x.strip().replace("\n", " ") for x in re.split(r"\n\s*\n", body.group(1)) if x.strip()]
        paragraphs = [x for x in paragraphs if not x.startswith("참고:") and not x.startswith("http")]
        if len(paragraphs) < 3:
            raise RuntimeError(f"Entry {tag.group(1)} appears incomplete")
        tension = next((x for x in paragraphs[2:] if any(word in x for word in
                     ("다만", "그런데", "물론", "문제", "어렵", "비용", "하지만"))),
                     paragraphs[len(paragraphs)//2])
        question = next((x for x in reversed(paragraphs) if "?" in x), paragraphs[-1])
        source = re.search(r"https://longblack\.co/note/\d+", body.group(1))
        items.append(dict(number=tag.group(1), title=tag.group(2),
            filename=Path(image.group()).name, intro=paragraphs[0],
            fact=paragraphs[1], tension=tension, question=question,
            source=source.group() if source else ""))
    if [p["number"] for p in items] != [f"{i:02d}" for i in range(1,31)]:
        raise RuntimeError("IDs are not consecutive 01 through 30")
    return items

def render(items, folder):
    try:
        from PIL import Image, ImageDraw, ImageFont
    except ImportError as ex:
        raise RuntimeError("Pillow is not installed. Report this; do not auto-install.") from ex
    regular = font_path()
    bold = font_path(True) or regular
    if regular is None:
        raise RuntimeError("No Korean font available. Report this; do not change fonts silently.")
    def font(sz, strong=False):
        return ImageFont.truetype(bold if strong else regular, sz, index=0)
    def wrap(txt, f, width):
        lines = []
        for paragraph in txt.split("\n"):
            line = ""
            for ch in paragraph:
                if line and f.getlength(line + ch) > width:
                    lines.append(line)
                    line = ch
                else:
                    line += ch
            if line:
                lines.append(line)
        return lines
    def fit(draw, txt, x, y, w, h, size, minimum, color, strong=False):
        for n in range(size, minimum - 1, -1):
            f = font(n, strong)
            lines = wrap(txt, f, w)
            leading = n + 12
            if len(lines) * leading <= h:
                break
        for line in lines[:int(h//leading)]:
            draw.text((x,y), line, font=f, fill=color)
            y += leading
    folder.mkdir(parents=True, exist_ok=True)
    output = []
    for idx, item in enumerate(items):
        accent = COLORS[idx % len(COLORS)]
        im = Image.new("RGB", (1200,1500), "#FAF8F6")
        d = ImageDraw.Draw(im)
        d.rounded_rectangle((55,55,1145,1445), radius=42, fill="#FFFFFF",
                            outline="#E8E2DF", width=3)
        d.rounded_rectangle((103,105,365,157), radius=23, fill="#F1EDFA")
        d.text((123,116), "LONG BLACK  /  NOTE", font=font(21, True), fill=accent)
        d.text((1012,100), item["number"], font=font(55, True), fill=accent)
        fit(d,item["title"],104,215,984,160,55,39,"#151720",True)
        d.rounded_rectangle((102,403,1098,409),radius=3,fill=accent)
        d.text((103,463),"01  이 사례에서 눈에 띄는 점",
               font=font(28,True),fill="#3B3942")
        d.rounded_rectangle((98,515,1102,737),radius=24,fill="#F7F5FA")
        fit(d,item["intro"]+" "+item["fact"],132,552,933,158,33,25,"#282A36")
        d.text((103,791),"02  쉽게 놓칠 수 있는 조건",
               font=font(28,True),fill="#3B3942")
        fit(d,item["tension"],113,850,980,180,32,25,"#323543")
        d.rounded_rectangle((98,1070,1102,1349),radius=27,fill="#F5F0FD")
        d.text((133,1112),"03  결국 남는 질문",
               font=font(28,True),fill=accent)
        fit(d,item["question"],134,1170,918,143,33,25,"#242537",True)
        d.text((103,1393),"YS  /  INDEPENDENT INSIGHT",
               font=font(19,True),fill=accent)
        note = item["source"].split("/")[-1] if item["source"] else "—"
        d.text((788,1392),"longblack.co/note/"+note,
               font=font(19),fill="#666778")
        path = folder/item["filename"]
        im.save(path,format="PNG",optimize=True)
        output.append((path,hashlib.sha256(path.read_bytes()).hexdigest()))
    print("[RENDERED]",len(output),"PNG images at 1200x1500")
    return output

def publish(files):
    cmd("gh","auth","status")
    cmd("gh","auth","setup-git")
    with tempfile.TemporaryDirectory(prefix="sinabroys_30_") as root:
        clone = Path(root)/"repo"
        cmd("git","clone","--quiet","--branch","main",
            f"https://github.com/{REPO}.git",str(clone))
        target = clone/TARGET_DIR
        target.mkdir(parents=True,exist_ok=True)
        for original,sha in files:
            final = target/original.name
            if final.exists():
                if hashlib.sha256(final.read_bytes()).hexdigest()!=sha:
                    raise RuntimeError("Existing image differs, will not overwrite: "+final.name)
            else:
                final.write_bytes(original.read_bytes())
        cmd("git","add","--",TARGET_DIR,cwd=clone)
        changed = subprocess.run(["git","diff","--cached","--quiet"],cwd=clone).returncode
        if changed:
            cmd("git","-c","user.name=SinaBroys Publisher",
                "-c","user.email=ceoYS@users.noreply.github.com",
                "commit","-m","media: regenerate 30 onepagers from approved copy",cwd=clone)
            cmd("git","push","origin","HEAD:main",cwd=clone)
        for path,sha in files:
            url = f"https://raw.githubusercontent.com/{REPO}/main/{TARGET_DIR}/{path.name}"
            verified = False
            for _ in range(6):
                try:
                    if hashlib.sha256(get(url)).hexdigest()==sha:
                        verified=True
                        break
                except Exception:
                    pass
                time.sleep(2)
            if not verified:
                raise RuntimeError("Public PNG verification failed: "+path.name)
            print("[VERIFIED]",url)
    print("[DONE] 30/30 GitHub URLs returned byte-identical PNGs")

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--out",default="SinaBroys_30_Onepagers")
    ap.add_argument("--source",help="Optional local markdown file for dry-run")
    ap.add_argument("--publish",action="store_true",help="Upload verified PNGs to GitHub")
    args=ap.parse_args()
    md=(Path(args.source).read_text(encoding="utf-8") if args.source
        else get(SOURCE).decode("utf-8"))
    files=render(parse(md),Path(args.out))
    print("[NOTICE] Newly rendered onepagers are not the old ZIP's original PNG bytes.")
    if args.publish:
        publish(files)
    else:
        print("[DRY RUN] Only local images generated; inspect before --publish")
if __name__=="__main__":
    main()
