#!/usr/bin/env python3
"""SinaBroys 01–10: editorial infographic V2. Changes media images only.
Uses Pillow + Noto CJK; no AI claims, fabricated metrics, or auto scheduling.
"""
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import hashlib, json, math, os, re, sys

W,H=1200,1500
OUT=Path(os.environ.get("SINABROYS_OUT","media/images/sinabroys/20261110"))
OUT.mkdir(parents=True,exist_ok=True)
F="/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
B="/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
for f in (F,B):
    if not Path(f).exists(): raise RuntimeError(f"Missing font {f}. Refuse to change fonts silently")
D=[
("01","01_HARMAY.png","HARMAY","작은 샘플을 돈 받고 파는 이유","#83629B","샘플을 산 사람은 다음에 뭘 살까?","1773"),
("02","02_Dominos.png","도미노피자","피자가 도착하기 전부터 시작되는 경험","#307E97","맛만큼 주문에서 수령까지의 마찰은 어떤가?","1767"),
("03","03_UrbanOutfitters.png","어반 아웃피터스","상품이 아니라 발견의 기대를 판다","#9A7254","다음에도 발견할 게 있다는 믿음은 어떻게 유지할까?","1838"),
("04","04_Eventbrite.png","이벤트브라이트","티켓 구매 전에 필요한 것은 발견","#397E74","추천을 본 사람이 실제 참석하도록 만들 수 있을까?","1835"),
("05","05_Marna.png","마나","누구도 불평하지 않은 불편을 발견하다","#A75E72","고객이 말로 표현하지 못한 불편은 어디에 있을까?","1833"),
("06","06_CryCheeseBurger.png","크라이치즈버거","자동화할 일과 사람이 남길 일","#A25A45","고객이 알아차리는 차이인가, 직원만 바쁜가?","1831"),
("07","07_MunhakDongne.png","문학동네 정민호","오래된 책을 새롭게 만나는 방법","#7061AD","새 상품보다 새로운 만남이 먼저일 수 있을까?","1832"),
("08","08_Dears.png","디어즈","직원 이탈률도 서비스 품질의 지표","#307F86","고객 이탈과 직원 이탈을 함께 보고 있는가?","1828"),
("09","09_ConcinoConcrete.png","콩치노 콩크리트","음악보다 음악에 집중하는 조건","#997347","다시 찾는 이유는 사진인가, 음악인가?","1827"),
("10","10_Crayola.png","크레욜라","크레용이 아닌 창의적인 순간","#5A8863","우리는 어떤 물건보다 어떤 순간을 만들고 있을까?","1844"),
]
def color(s):return tuple(int(s[i:i+2],16) for i in (1,3,5))
def tint(hexcol,amt=.86):
    r,g,b=color(hexcol);return (int(255*amt+r*(1-amt)),int(255*amt+g*(1-amt)),int(255*amt+b*(1-amt)))
def font(n,b=False):return ImageFont.truetype(B if b else F,n,index=0)
def txt(d,s,x,y,n=30,fill="#22252A",bold=False,center=False):
    f=font(n,bold)
    if center:x-=f.getlength(s)/2
    d.text((int(x),int(y)),s,font=f,fill=fill)
def box(d,b,fill,rad=24,outline=None,width=2):
    d.rounded_rectangle(tuple(int(z) for z in b),radius=rad,fill=fill,outline=outline,width=width)
def circ(d,x,y,r,fill,outline=None,width=2):
    d.ellipse((x-r,y-r,x+r,y+r),fill=fill,outline=outline,width=width)
def ln(d,points,col,width=5):d.line(points,fill=col,width=width,joint="curve")
def arr(d,x1,y1,x2,y2,col,width=6):
    ln(d,[(x1,y1),(x2,y2)],col,width);a=math.atan2(y2-y1,x2-x1)
    for t in [-.55,.55]:
        ln(d,[(x2,y2),(x2-20*math.cos(a+t),y2-20*math.sin(a+t))],col,width)
def wrapped(s,size,maxwidth,bold=False):
    f=font(size,bold);result=[]
    for para in s.split("\n"):
        acc=""
        for ch in para:
            if acc and f.getlength(acc+ch)>maxwidth:
                result.append(acc);acc=ch
            else:acc+=ch
        result.append(acc)
    return result
def paragraph(d,s,x,y,maxwidth,height,size=33,minsize=23,col="#292B30",bold=False):
    for n in range(size,minsize-1,-1):
        lines=wrapped(s,n,maxwidth,bold)
        step=int(n*1.5)
        if len(lines)*step<=height:break
    if len(lines)*step>height:raise RuntimeError("Text overflow: "+s[:35])
    for line in lines:
        txt(d,line,x,y,n,col,bold);y+=step
def frame(row):
    no,fname,title,sub,a,q,note=row
    im=Image.new("RGB",(W,H),"#FAF8F3");d=ImageDraw.Draw(im)
    circ(d,1169,-20,210,tint(a,.92));circ(d,-90,1390,210,tint(a,.96))
    box(d,(60,55,362,112),tint(a,.88),26)
    txt(d,"YS  /  BUSINESS NOTES",82,68,23,a,True)
    txt(d,no+" / 30",1020,65,33,a,True)
    title_size=68 if len(title)<=8 else 58 if len(title)<=10 else 52
    txt(d,title,65,158,title_size,"#1B2226",True)
    paragraph(d,sub,69,254,1065,73,34,28,"#5E6367")
    d.rectangle((67,344,1134,350),fill=a)
    txt(d,"CASE  /  VISUAL ANALYSIS",68,373,22,a,True)
    box(d,(69,1138,1133,1359),tint(a,.91),34)
    txt(d,"남는 질문",105,1177,29,a,True)
    paragraph(d,q,105,1231,972,108,37,30,"#20242A",True)
    ln(d,[(67,1390),(1132,1390)],tint(a,.56),3)
    txt(d,"YS  /  INDEPENDENT INSIGHT",69,1410,19,a,True)
    txt(d,"longblack.co/note/"+note,794,1410,19,"#6E7274")
    return im,d,a
def tag(d,s,x,y,w,col):
    box(d,(x,y,x+w,y+59),tint(col,.85),20)
    txt(d,s,x+w/2,y+9,26,col,True,True)
def card(d,b,heading,body,a):
    box(d,b,"#FFFFFF",22)
    txt(d,heading,b[0]+28,b[1]+25,27,a,True)
    paragraph(d,body,b[0]+28,b[1]+77,b[2]-b[0]-56,b[3]-b[1]-92,25,23,"#282B31")
def bottle(d,x,y,s,a,full=False):
    w=int(115*s);h=int((220 if full else 165)*s)
    box(d,(x-w//2,y-h//2,x+w//2,y+h//2),tint(a,.74),17,outline=a,width=5)
    box(d,(x-int(26*s),y-h//2-int(33*s),x+int(26*s),y-h//2+int(6*s)),a,8)
    box(d,(x-w//2+16*s,y-h//2+h*.36,x+w//2-16*s,y-h//2+h*.71),"#FFFFFF",8)
    txt(d,"FULL" if full else "TRY",x,y-14*s,int(20*s),a,True,True)
def book(d,x,y,w,h,c):
    box(d,(x,y,x+w,y+h),c,4)
    ln(d,[(x+8,y+6),(x+8,y+h-7)],"#F6F1E9",3)
def icon(d,name,x,y,a):
    if name=="check":
        circ(d,x,y,43,tint(a,.8));ln(d,[(x-22,y),(x-3,y+18),(x+25,y-20)],a,8)
    elif name=="heart":
        txt(d,"♥",x,y-45,78,a,True,True)
    elif name=="person":
        circ(d,x,y-35,25,a);box(d,(x-41,y-4,x+41,y+63),tint(a,.65),16)
    elif name=="calendar":
        box(d,(x-55,y-55,x+55,y+59),tint(a,.7),15,outline=a,width=5)
        ln(d,[(x-55,y-17),(x+55,y-17)],a,4)
        for xx in [-24,15]:circ(d,x+xx,y+14,8,a)
    elif name=="listen":
        circ(d,x,y,49,tint(a,.75),outline=a,width=4);txt(d,"♫",x,y-41,68,a,True,True)
    elif name=="bag":
        box(d,(x-50,y-17,x+50,y+64),tint(a,.72),10,outline=a,width=4)
        d.arc((x-23,y-48,x+23,y+10),185,355,fill=a,width=5)
def draw(row,d,a):
    no=int(row[0])
    top=470
    if no==1:
        txt(d,"CUSTOMER JOURNEY",84,449,30,a,True)
        box(d,(80,512,1120,977),tint(a,.94),31)
        steps=[("샘플 구매","bottle"),("직접 사용","check"),("취향 발견","heart"),("정품 구매","full")]
        for i,(lab,k) in enumerate(steps):
            x=223+253*i
            circ(d,x,700,102,"#FFFFFF")
            if k=="bottle":bottle(d,x,704,.62,a)
            elif k=="full":bottle(d,x,695,.73,a,True)
            else:icon(d,k,x,702,a)
            txt(d,lab,x,835,29,"#1E272C",True,True)
            if i<3:arr(d,x+110,700,x+145,700,a,5)
        txt(d,"샘플이 정품 판매의 적인지, 입구인지 확인이 필요하다",600,1027,27,a,True,True)
    elif no==2:
        txt(d,"ORDER  →  EXPERIENCE",85,447,29,a,True)
        box(d,(82,501,1116,1030),"#E6F0F2",30)
        names=["주문","조리","배달","수령"]
        for i,lab in enumerate(names):
            x=205+i*260
            circ(d,x,695,86,"#FFFFFF",outline=a,width=4)
            if i==0: box(d,(x-38,644,x+38,741),tint(a,.7),8,outline=a,width=4);txt(d,"✓",x,665,42,a,True,True)
            if i==1:
                box(d,(x-57,666,x+57,731),tint(a,.75),24,outline=a,width=5)
                for j in range(4):circ(d,x-33+j*22,693,7,a)
            if i==2:
                circ(d,x-42,726,17,a);circ(d,x+40,726,17,a)
                ln(d,[(x-42,716),(x-3,678),(x+30,717),(x-42,717)],a,7)
            if i==3:icon(d,"bag",x,691,a)
            txt(d,lab,x,821,31,a,True,True)
            if i<3:arr(d,x+88,696,x+168,696,a)
        txt(d,"맛을 평가하기 전에 고객은 이미 여러 과정을 경험한다",599,957,27,a,True,True)
        tag(d,"마찰 지점 발견",420,1051,360,a)
    elif no==3:
        txt(d,"PRODUCT  vs  DISCOVERY",84,447,29,a,True)
        box(d,(79,514,563,1049),tint(a,.91),29)
        box(d,(632,514,1118,1049),"#E7EEE5",29)
        txt(d,"상품만 고르기",316,558,33,a,True,True)
        txt(d,"취향을 발견하기",873,558,33,"#54745C",True,True)
        for j,(lab,c) in enumerate([("의류","#B2A7A3"),("신발","#89969A"),("소품","#A9B49C")]):
            box(d,(152,661+j*92,470,719+j*92),tint(c,.55),15)
            txt(d,lab,316,666+j*92,25,"#45484A",True,True)
        for j,(lab,c) in enumerate([("패션","#789A7E"),("공간","#90A7B4"),("라이프스타일","#B5A28D")]):
            circ(d,759,687+j*93,28,tint(c,.4),outline=c,width=4)
            txt(d,lab,815,662+j*93,26,"#405E4B",True)
        txt(d,"편집의 기대는 재고·유행 리스크를 동반한다",601,1072,26,a,True,True)
    elif no==4:
        txt(d,"TWO-SIDED PLATFORM",84,447,29,a,True)
        box(d,(86,511,1114,1025),tint(a,.94),33)
        pts=[(253,"주최자"),(604,"플랫폼"),(955,"참가자")]
        for i,(x,lab) in enumerate(pts):
            circ(d,x,709,114,"#FFFFFF",outline=a if i==1 else tint(a,.52),width=5)
            icon(d,"person" if i!=1 else "calendar",x,693,a)
            txt(d,lab,x,854,32,a,True,True)
        arr(d,379,700,470,700,a);arr(d,730,700,821,700,a)
        tag(d,"행사 발견",149,937,237,a)
        arr(d,395,965,479,965,a)
        tag(d,"티켓 구매",482,937,237,a)
        arr(d,728,965,812,965,a)
        tag(d,"실제 참석",815,937,239,a)
        txt(d,"추천 클릭 ≠ 실제 참석",600,1066,29,a,True,True)
    elif no==5:
        txt(d,"UNSPOKEN FRICTION",84,447,29,a,True)
        labels=[("젖은 우산","자주 겪지만 익숙한 불편"),("장바구니","매번 반복하는 작은 동작"),("생활 속 습관","말로 설명하지 않는 문제")]
        for i,(lab,body) in enumerate(labels):
            x=80+i*349
            box(d,(x,531,x+328,978),tint(a,.91 if i==1 else .94),31)
            circ(d,x+164,682,94,"#FFFFFF")
            if i==0:
                d.arc((x+99,622,x+228,729),180,360,fill=a,width=9)
                ln(d,[(x+164,675),(x+164,754),(x+191,754)],a,8)
            elif i==1:icon(d,"bag",x+164,669,a)
            else:
                icon(d,"check",x+164,669,a)
            txt(d,lab,x+164,811,28,a,True,True)
            paragraph(d,body,x+28,875,270,81,24,22,"#464148")
        txt(d,"익숙한 불편을 해결해도 구매할 이유가 되는지 봐야 한다",600,1052,25,a,True,True)
    elif no==6:
        txt(d,"DECISION MATRIX",85,447,29,a,True)
        box(d,(84,516,1115,1021),tint(a,.95),35)
        x0,y0=220,915
        ln(d,[(x0,550),(x0,y0),(1060,y0)],"#5E5D5B",5)
        txt(d,"운영 부담 ↑",112,551,27,"#4B4B4B",True)
        txt(d,"고객이 알아차리는 차이  →",598,953,27,"#4B4B4B",True,True)
        box(d,(247,580,608,741),"#F2DDD3",26)
        txt(d,"자동화 검토",428,612,34,a,True,True)
        paragraph(d,"고객에게 의미가 작은\n반복 업무",280,674,310,58,24,22,"#47403F")
        box(d,(656,740,1046,893),"#F1E4CD",26)
        txt(d,"사람 손 유지",851,764,34,a,True,True)
        paragraph(d,"고객이 차이를 느끼는\n경험",697,827,320,58,24,22,"#47403F")
        txt(d,"판단 기준은 비용만이 아니라 경험과 지속 가능성",599,1068,25,a,True,True)
    elif no==7:
        txt(d,"REPOSITIONING AN EXISTING PRODUCT",85,447,27,a,True)
        box(d,(83,514,1117,1029),tint(a,.93),34)
        pts=[(232,"신간 코너"),(602,"다른 진열"),(974,"새 독자")]
        for i,(x,s) in enumerate(pts):
            circ(d,x,682,105,"#FFFFFF")
            if i<2:
                for j,c in enumerate(["#CDB48F","#9AA5B4","#9D87AF"]):book(d,x-52+j*35,622,34,113,c)
            else:icon(d,"person",x,681,a)
            txt(d,s,x,843,30,a,True,True)
            if i<2:arr(d,x+114,698,x+254,698,a)
        txt(d,"같은 제품도 만나는 맥락이 달라지면 다르게 보인다",601,981,27,a,True,True)
        tag(d,"고객 미도달  vs  고객 불필요",338,1054,523,a)
    elif no==8:
        txt(d,"EMPLOYEE → SERVICE FLYWHEEL",85,447,29,a,True)
        box(d,(83,515,1118,1026),"#E2F0EC",34)
        pts=[(598,600,"근무 조건"),(871,736,"직원 안정"),(598,882,"서비스 품질"),(321,736,"재방문")]
        for i,(x,y,s) in enumerate(pts):
            circ(d,x,y,106,"#FFFFFF",outline=tint(a,.6),width=5)
            txt(d,s,x,y-21,30,a,True,True)
        for i,(x,y,s) in enumerate(pts):
            x2,y2,_=pts[(i+1)%4]
            mx=(x+x2)/2;my=(y+y2)/2
            arr(d,int((x+mx)/2),int((y+my)/2),int((mx+x2)/2),int((my+y2)/2),a,5)
        txt(d,"직원 안정이 곧 고객 경험의 조건이 될 수 있다",597,1068,27,a,True,True)
    elif no==9:
        txt(d,"PLACE  /  FOCUSED LISTENING",85,447,28,a,True)
        box(d,(78,508,560,1034),"#EFE9DE",32)
        box(d,(637,508,1117,1034),"#E8DCC8",32)
        txt(d,"집에서 듣기",320,555,32,a,True,True)
        txt(d,"그곳에 가서 듣기",880,555,32,a,True,True)
        icon(d,"listen",319,731,a)
        icon(d,"listen",880,729,a)
        for i,(s,x) in enumerate([("알림",313),("업무",313),("방해",313)]):
            tag(d,s,x-113,851+i*58,226,a)
        # central focus lines right
        for j in range(3):
            ln(d,[(769,867+j*36),(993,867+j*36)],a,5)
        txt(d,"같은 음악, 다른 집중의 조건",602,1071,27,a,True,True)
    elif no==10:
        txt(d,"PRODUCT CATEGORY → USE MOMENT",84,447,27,a,True)
        box(d,(80,511,1117,1026),"#EDF2E7",34)
        circ(d,602,742,119,"#FFF8EE",outline=a,width=6)
        txt(d,"크레욜라",602,710,34,a,True,True)
        for x,y,s in [(244,644,"아이의 놀이"),(966,645,"어른의 휴식"),(607,973,"창의적 시간")]:
            circ(d,x,y,92,"#FFFFFF")
            txt(d,s,x,y-20,27,a,True,True)
        arr(d,485,705,355,666,a);arr(d,722,705,846,665,a)
        arr(d,602,864,602,876,a)
        txt(d,"물건보다 고객이 꺼내는 순간을 다시 정의한다",600,1074,27,a,True,True)
    else: raise RuntimeError(no)
manifest=[]
for row in D:
    im,d,a=frame(row)
    draw(row,d,a)
    path=OUT/row[1]
    im.save(path,format="PNG",optimize=True)
    if path.stat().st_size<15000:raise RuntimeError("Suspiciously small PNG: "+str(path))
    if Image.open(path).size!=(1200,1500):raise RuntimeError("Wrong dimensions")
    manifest.append({"id":row[0],"file":row[1],"sha256":hashlib.sha256(path.read_bytes()).hexdigest(),
       "size":path.stat().st_size,"note":row[6]})
if os.environ.get("SINABROYS_SKIP_CONTACT_SHEET")!="1":
    sheet=Image.new("RGB",(1600,1020),"#EFEEEA")
    for i,item in enumerate(manifest):
        im=Image.open(OUT/item["file"])
        im.thumbnail((290,420))
        sheet.paste(im,(12+i%5*320+(290-im.width)//2,28+i//5*490))
    sheet.save(OUT/"contact_sheet_01_10_v2.jpg",quality=88)
(OUT/"manifest_01_10_v2.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding="utf-8")
print("[RENDERED]",len(manifest), "images at 1200x1500")
for it in manifest: print(it["id"],it["file"],it["size"],it["sha256"][:12])
