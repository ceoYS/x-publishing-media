#!/usr/bin/env python3
# X-ready one-page editorial infographics. Generated solely from posts.json.
import json, hashlib, math, os, glob
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT=Path(__file__).resolve().parent
DATA=json.loads((ROOT/'posts.json').read_text(encoding='utf-8'))
OUT=ROOT/'images'
OUT.mkdir(parents=True,exist_ok=True)
W,H=1200,1500
PALETTES=[
('#132A38','#E6B86E','#F6F2E9'),('#272B39','#B9CECF','#F8F4EC'),
('#233530','#B9C68D','#F6F1E8'),('#3B3030','#E5BFA7','#F8F1E9'),
('#203043','#94C8D5','#F3F5F2'),('#333044','#C4B3D7','#F7F3F1')]
FONTPATHS=[
'/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',
'/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc',
'/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc',
'/usr/share/fonts/truetype/nanum/NanumGothic.ttf',
'/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf']
BOLDPATHS=[
'/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc',
'/usr/share/fonts/truetype/nanum/NanumGothicBold.ttf']
def font(size,bold=False):
    for x in ((BOLDPATHS+FONTPATHS) if bold else FONTPATHS):
        if os.path.isfile(x):return ImageFont.truetype(x,size)
    raise RuntimeError('Korean font missing. Install fonts-noto-cjk.')
def wrap(d,text,f,maxw,maxlines=4):
    # Unicode-safe visual wrapping; punctuation and Korean syllables remain intact
    out=[];line=''
    for ch in str(text).replace('\\n',' ').strip():
        t=line+ch
        if d.textlength(t,font=f)>maxw and line:
            out.append(line.strip());line=ch
        else:line=t
    if line:out.append(line.strip())
    if len(out)>maxlines:
        out=out[:maxlines]
        while d.textlength(out[-1]+'…',font=f)>maxw:out[-1]=out[-1][:-1]
        out[-1]+='…'
    return out
def tw(d,text,xy,f,fill,maxw,lines=4,leading=1.46):
    x,y=xy
    for ln in wrap(d,text,f,maxw,lines):
        d.text((x,y),ln,font=f,fill=fill)
        y+=int(f.size*leading)
    return y
def draw_one(item):
    i=item['number'];slug=item['slug']
    navy,accent,paper=PALETTES[(i-1)%len(PALETTES)]
    img=Image.new('RGB',(W,H),paper);d=ImageDraw.Draw(img)
    d.rectangle((0,0,W,288),fill=navy)
    # signature editorial motif: circles/lines, deliberately different by subject
    for k in range(6):
        rr=68+k*32
        d.ellipse((W-135-rr,103-rr,W-135+rr,103+rr),
                  outline=accent,width=3 if k%2 else 2)
    d.rounded_rectangle((64,53,282,102),radius=24,fill=accent)
    d.text((91,58),'SINA / NOTES',font=font(23,True),fill=navy)
    d.text((64,119),f"{slug}  /  30",font=font(26,True),fill=accent)
    tw(d,item['title'],(62,169),font(49,True),'#FFFFFF',925,2,1.27)
    # Sector and counter line
    d.line((64,329,W-64,329),fill='#DAD7D0',width=2)
    d.text((68,346),f"CASE  {item['subject']}",font=font(29,True),fill=navy)
    d.text((68,397),item['sector'],font=font(25),fill='#687178')
    cards=[
       ('01  관찰한 사실', item['fact']),
       ('02  내가 읽은 구조', item['insight']),
       ('03  보이지 않는 비용', item['risk']),
       ('04  확인하고 싶은 질문', item['test'])
    ]
    y=469
    for j,(lab,val) in enumerate(cards):
        h=205 if j!=1 else 214
        d.rounded_rectangle((63,y,W-63,y+h),radius=24,fill='#FFFFFF',outline='#E5E0D5',width=2)
        d.rounded_rectangle((63,y+22,72,y+h-22),radius=5,fill=accent)
        d.text((102,y+23),lab,font=font(27,True),fill=navy)
        tw(d,val,(102,y+77),font(31), '#353A3B',W-205,3,1.43)
        y+=h+19
    # footer
    d.line((64,1415,W-64,1415),fill='#D4CFC2',width=2)
    d.text((65,1432),f"Source  longblack.co/note/{item['note_id']}",font=font(24),fill='#5A6266')
    d.text((925,1432),"@SinaBroys",font=font(22,True),fill=navy)
    target=OUT/f'{slug}.png'
    img.save(target,optimize=True)
    return {'number':i,'subject':item['subject'],'filename':target.name,'sha256':hashlib.sha256(target.read_bytes()).hexdigest(),'bytes':target.stat().st_size}
manifest=[draw_one(x) for x in DATA['items']]
assert len(manifest)==30
(OUT/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
# Contact sheet for visual QA (not intended for X)
thumbs=[]
for p in sorted(OUT.glob('??.png')):
    im=Image.open(p);im.thumbnail((240,300));thumbs.append(im.copy())
sheet=Image.new('RGB',(240*6,300*5),'#E9E9E9')
for n,im in enumerate(thumbs):sheet.paste(im,((n%6)*240,(n//6)*300))
sheet.save(OUT/'contact_sheet.jpg',quality=85,optimize=True)
print(json.dumps({'generated':len(manifest),'bytes':sum(x['bytes'] for x in manifest)},ensure_ascii=False))
