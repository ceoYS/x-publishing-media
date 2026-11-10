#!/usr/bin/env python3
"""Twenty individually illustrated editorial one-pagers: posts 11-30.

Uses existing 01-10 typography/layout helpers only (renders to temp).
No changes to approved source posts, original article references, or reservations.
"""
import os, runpy, tempfile, json, hashlib, math
from pathlib import Path
from PIL import Image, ImageDraw

os.environ["SINABROYS_OUT"] = tempfile.mkdtemp(prefix="sinabroys_helper_")
os.environ["SINABROYS_SKIP_CONTACT_SHEET"] = "1"
h = runpy.run_path(str(Path(__file__).with_name("sinabroys_01_10_v2_editorial.py")))
frame,box,txt,circ,ln,arr,tag,paragraph,icon,book,bottle = (h[k] for k in
    ("frame","box","txt","circ","ln","arr","tag","paragraph","icon","book","bottle"))
tint = h["tint"]
from PIL import ImageFont
W,H=1200,1500
DEST=Path("media/images/sinabroys/20261110")
DEST.mkdir(parents=True,exist_ok=True)
ROWS=[
("11","11_YiayiaAndFriends.png","이야이야앤프렌즈","처음 사는 이유와 다시 사는 이유","#996B58","디자인으로 시작한 관심이 실제 만족으로 이어질까?","1841"),
("12","12_Arena.png","아레나 Are.na","오래 머무는 앱보다 오래 쓰는 도구","#7771AE","사용 시간을 늘리지 않아도 지불할 이유가 있을까?","2057"),
("13","13_ThreeWheelBooks.png","세발서점","고객을 찾아가는 작은 서점","#397B8B","매장을 옮기는 자유는 어떤 제약과 맞바뀔까?","2049"),
("14","14_WeStayByulnae.png","위스테이별내","시설보다 함께 살아가는 규칙","#638A76","참여와 참여하지 않을 자유를 함께 설계할 수 있을까?","2046"),
("15","15_AITransformation.png","AI 전환 보고서","새 도구보다 달라지는 실제 업무","#5486A6","절약한 시간만큼 검수 비용도 확인하고 있을까?","2043"),
("16","16_TokyoRRealEstate.png","도쿄R부동산","누군가에게는 낡음도 선택 이유","#A0824D","평균 점수보다 취향과 제약을 먼저 볼 수 있을까?","2041"),
("17","17_GoodSamaritanRecipe.png","굿사마리안레시피","처음 찾아온 이유와 다시 오는 이유","#BD7162","스토리 다음에 고객이 기억하는 것은 무엇일까?","2039"),
("18","18_Levis.png","리바이스","새 상품도 브랜드의 신뢰를 지켜야 한다","#4573A5","확장은 기존 고객의 생활과 자연스럽게 연결되는가?","594"),
("19","19_PerfumeHeroes.png","조향사 오하니","향수의 이야기는 구매 이후에도 남을까","#8B6A97","첫 구매를 만든 이야기와 재구매 이유는 같은가?","593"),
("20","20_F45.png","F45","운동 습관을 만드는 그룹의 힘","#3D8D83","모임의 흥분보다 꾸준히 운동하는 이유는 무엇일까?","592"),
("21","21_BaskinRobbins.png","배스킨라빈스","브랜드 매출과 점주의 이익은 다르다","#A75E83","점포별 투자 회수기간을 함께 보고 있는가?","591"),
("22","22_GShock.png","지샥 G-SHOCK","포기하지 않는 것과 집착하는 것","#62697C","버티기보다 고객의 작은 신호를 읽고 있는가?","581"),
("23","23_MiddaySquares.png","미드데이스퀘어","창업자의 이야기가 제품 구매로 이어질까","#9E6755","조회수와 구매 전환은 얼마나 연결될까?","578"),
("24","24_SleepEconomy.png","슬리포노믹스","수면 시장에서 가장 어려운 약속","#788B9A","사용자가 느끼는 변화와 검증된 효과를 구분하는가?","577"),
("25","25_ScienceMuseum.png","이정모 과학관","설명보다 직접 해본 기억","#D08A43","즐거운 체험이 며칠 뒤 이해로 남았는가?","604"),
("26","26_BrandCollaboration.png","허재영 협업","로고 두 개보다 중요한 조합","#7C6C9A","이 파트너가 아니면 못 만들 결과는 무엇일까?","580"),
("27","27_Musinsa.png","무신사","커뮤니티의 취향이 구매 신뢰로","#445D81","사람들이 이곳의 추천을 믿고 실제로 사는가?","2045"),
("28","28_JasperMorrison.png","재스퍼 모리슨","첫인상보다 매일의 사용","#788476","사진에 멋진 물건과 오래 쓰기 좋은 물건은 같은가?","2054"),
("29","29_TENT.png","TENT의 도구 수업","새 도구보다 먼저 하지 않을 일","#8E794F","일을 줄일 권한 없이 도구만 늘고 있지는 않은가?","2048"),
("30","30_RossanoFerretti.png","로사노 페레티","프리미엄 서비스의 복제 가능성","#896C6A","한 사람의 판단을 팀이 배워 재현할 수 있을까?","585"),
]
def ellipse(d,xy,c,outline=None,width=3): d.ellipse(tuple(map(int,xy)),fill=c,outline=outline,width=width)
def flow(d,labels,xs,y,a):
    for i,(x,l) in enumerate(zip(xs,labels)):
        circ(d,x,y,66,"#FFFFFF",outline=a,width=4)
        txt(d,str(i+1).zfill(2),x,y-29,37,a,True,True)
        tag(d,l,x-108,y+95,216,a)
        if i<len(xs)-1:arr(d,x+75,y,xs[i+1]-75,y,a,5)
def heading(d,s,a):txt(d,s,91,444,30,a,True)
def note(d,s,a):txt(d,s,600,1079,26,a,True,True)
def column(d,x,y,w,h,title,body,a,fill):
    box(d,(x,y,x+w,y+h),fill,26)
    txt(d,title,x+26,y+30,31,a,True)
    if body: paragraph(d,body,x+26,y+99,w-52,h-128,28,23,"#323943")
def shop(d,x,y,a):
    box(d,(x-102,y-12,x+102,y+138),"#FFFFFF",15,outline=a,width=4)
    d.polygon([(x-118,y),(x-83,y-67),(x+83,y-67),(x+118,y)],fill=tint(a,.5))
    box(d,(x-32,y+57,x+32,y+136),tint(a,.65),5)
def person(d,x,y,a):
    circ(d,x,y-40,31,tint(a,.4),outline=a,width=4)
    box(d,(x-45,y-4,x+45,y+92),tint(a,.62),18)
def garment(d,x,y,a):
    d.polygon([(x-99,y),(x-47,y-39),(x+47,y-39),(x+99,y),(x+69,y+54),(x+49,y+46),(x+49,y+168),(x-49,y+168),(x-49,y+46),(x-69,y+54)],fill=tint(a,.45))
    ln(d,[(x-47,y-39),(x,y-7),(x+47,y-39)],a,5)
def diagram(d,row):
    no=int(row[0]);a=row[4]
    if no==11:
        heading(d,"FIRST PURCHASE  ≠  RETURN PURCHASE",a)
        column(d,85,511,495,478,"처음 구매","호기심 · 패키지 · 선물할 이유",a,tint(a,.90))
        column(d,619,511,497,478,"재구매","실제 맛과 품질 · 만족 · 쓰임",a,"#E5EDE6")
        bottle(d,325,763,.81,a)
        bottle(d,854,763,.81,"#62856D",True)
        arr(d,574,764,621,764,a)
        note(d,"브랜드의 이야기는 입구, 제품 만족은 반복 구매의 조건",a)
    elif no==12:
        heading(d,"조용한 수집과 연결을 설계하는 도구",a)
        box(d,(83,512,1120,1036),"#EBE9F4",29)
        txt(d,"소셜 피드",316,555,30,a,True,True)
        txt(d,"Are.na",889,555,34,a,True,True)
        for j in range(4):
            box(d,(137,625+j*82,500,674+j*82),tint(a,.78),12)
            txt(d,["추천","알림","반응","추가 스크롤"][j],320,633+j*82,22,a,True,True)
        pts=[(758,690),(927,642),(1019,819),(843,915)]
        for i,j in [(0,1),(1,2),(2,3),(3,0),(0,2)]:
            ln(d,[pts[i],pts[j]],a,4)
        for i,(x,y) in enumerate(pts):
            box(d,(x-63,y-44,x+63,y+44),"#FFFFFF",16,outline=a,width=3)
            txt(d,["기록","이미지","연결","생각"][i],x,y-17,25,a,True,True)
        note(d,"체류시간이 아니라 정리할 수 있는 사고의 가치",a)
    elif no==13:
        heading(d,"이동식 서점의 비용과 기회",a)
        box(d,(83,514,1116,1031),"#E3EFF0",30)
        # mobile bookcart, distinct three wheels
        for cx,r in [(279,851),(617,851),(933,851)]:
            circ(d,cx,851,r*0+53,"#56656C")
            circ(d,cx,851,29,"#F5F2E9")
        box(d,(164,622,1006,805),"#F9F3E9",15,outline=a,width=4)
        for i,c in enumerate(["#B7A1AC","#D6C08D","#88AAB2","#B08D81"]):
            book(d,247+i*148,660,108,131,c)
        txt(d,"책장이 움직이면 독자를 만나는 장소도 바뀐다",601,938,28,a,True,True)
        note(d,"공간의 자유와 날씨·계절의 제약을 함께 본다",a)
    elif no==14:
        heading(d,"주거 공동체는 시설보다 운영 규칙",a)
        box(d,(80,517,1120,1028),"#E6EEE6",34)
        flow(d,["주민","운영 규칙","함께 사는 공간"],[247,602,960],696,a)
        column(d,147,893,405,114,"참여의 기회","",a,"#FFFFFF")
        column(d,647,893,405,114,"참여하지 않을 자유","",a,"#FFFFFF")
        note(d,"시설을 늘리기보다 지속될 의사결정 구조가 중요하다",a)
    elif no==15:
        heading(d,"BEFORE  /  AFTER",a)
        box(d,(83,504,566,1036),"#EEEEEC",30)
        box(d,(630,504,1119,1036),"#E3EEF7",30)
        for x,title,labels in [(324,"기존 업무",["자료 정리","반복 입력","사람 검수"]),(875,"AI 활용",["반복 처리","예외 판단","사람 검수"])]:
            txt(d,title,x,543,32,a,True,True)
            for k,l in enumerate(labels):
                y=653+k*115
                box(d,(x-179,y,x+179,y+80),"#FFFFFF",18)
                txt(d,l,x,y+21,26,"#323943",True,True)
                if k<2:arr(d,x,y+85,x,y+105,a,3)
        note(d,"시간 절감뿐 아니라 결과 검수 부담도 함께 측정",a)
    elif no==16:
        heading(d,"매물의 평균 점수와 취향의 일치",a)
        box(d,(87,520,570,1010),"#EEEAE1",29)
        box(d,(625,520,1112,1010),"#E4EEE8",29)
        for x,title,old in [(324,"표준적인 매물",False),(864,"개성 있는 공간",True)]:
            d.polygon([(x-145,734),(x,618),(x+145,734)],fill="#9BB0B0" if not old else "#A48871")
            box(d,(x-110,735,x+110,897),"#FBF9F0",7,outline=a,width=3)
            for dx in [-60,27]:box(d,(x+dx,764,x+dx+49,819),"#D9DFDE" if not old else "#DDC9A3",6)
            txt(d,title,x,944,29,a,True,True)
        note(d,"단점도 솔직히 보여줘야 맞는 고객이 선택한다",a)
    elif no==17:
        heading(d,"첫 방문과 재방문을 분리해 본다",a)
        box(d,(86,510,564,1026),tint(a,.85),34)
        box(d,(640,510,1114,1026),"#E7EEE5",34)
        for x,title,sub in [(327,"첫 방문","창업자의 이야기"),(877,"재방문","음식 · 가격 · 경험")]:
            circ(d,x,744,133,"#FFFFFF")
            circ(d,x,744,102,"#F6E9D3",outline=a,width=5)
            for dx,dy in [(-38,-23),(45,-14),(-11,42)]:circ(d,x+dx,744+dy,19,tint(a,.3))
            txt(d,title,x,915,33,a,True,True)
            txt(d,sub,x,971,24,"#5F6264",False,True)
        arr(d,570,760,630,760,a,6)
        note(d,"좋은 스토리가 좋은 음식의 검증을 대신하지 않는다",a)
    elif no==18:
        heading(d,"브랜드 확장의 질문: 신뢰를 지키는가",a)
        box(d,(81,511,1117,1024),"#E6EDF5",34)
        garment(d,265,670,a);garment(d,885,670,"#8090A6")
        box(d,(448,678,744,879),"#FFFFFF",27)
        txt(d,"브랜드의",596,723,35,a,True,True)
        txt(d,"핵심 신뢰",596,785,36,a,True,True)
        arr(d,389,767,437,767,a);arr(d,752,767,793,767,a)
        txt(d,"상품 종류를 넓히는 것이 곧 브랜드를 키우는 건 아니다",600,992,24,a,True,True)
        note(d,"인기보다 고객의 생활과 기존 브랜드 신뢰",a)
    elif no==19:
        heading(d,"첫 구매의 서사  /  재구매의 취향",a)
        box(d,(86,518,1114,1028),"#ECE3EF",34)
        bottle(d,600,750,1.28,a,True)
        box(d,(121,700,368,867),"#FFFFFF",20)
        txt(d,"스토리",243,733,31,a,True,True)
        txt(d,"첫 관심",243,792,28,"#45454A",True,True)
        box(d,(824,700,1073,867),"#FFFFFF",20)
        txt(d,"향의 만족",949,732,30,a,True,True)
        txt(d,"반복 구매",949,793,28,"#45454A",True,True)
        arr(d,373,767,492,767,a);arr(d,706,767,811,767,a)
        note(d,"이야기를 산 사람이 향 자체를 또 선택하는가",a)
    elif no==20:
        heading(d,"개인의 의지보다 지속 가능한 그룹 경험",a)
        box(d,(86,516,1113,1029),"#E0EEE9",34)
        pts=[(600,635,"참여"),(931,789,"동료"),(600,937,"반복"),(266,789,"습관")]
        for i,(x,y,l) in enumerate(pts):
            circ(d,x,y,80,"#FFFFFF",outline=a,width=4)
            txt(d,l,x,y-24,31,a,True,True)
        for i,(x,y,l) in enumerate(pts):
            xx,yy,_=pts[(i+1)%4]
            arr(d,int(x*.65+xx*.35),int(y*.65+yy*.35),int(x*.36+xx*.64),int(y*.36+yy*.64),a,5)
        note(d,"한 번의 인증보다 다음주에도 오는 이유",a)
    elif no==21:
        heading(d,"프랜차이즈의 숫자는 주체별로 다르다",a)
        box(d,(81,510,1116,1037),"#F1E6EC",34)
        column(d,117,557,449,354,"브랜드·본사","가맹점 매출 합계와 본사 회계 매출은 같지 않을 수 있다",a,"#FFFFFF")
        column(d,638,557,444,354,"개별 점주","월세 · 인건비 · 폐기 · 초기 투자비용을 함께 고려",a,"#FFFFFF")
        arr(d,576,746,623,746,a)
        tag(d,"매장 수 ≠ 점주 수익성",338,956,528,a)
        note(d,"점포별 투자회수기간이 빠진 성장 숫자는 불완전하다",a)
    elif no==22:
        heading(d,"제품을 오래 지키는 것의 두 얼굴",a)
        box(d,(83,507,1114,1023),"#E8EBEF",34)
        circ(d,600,739,155,"#FFFFFF",outline=a,width=8)
        circ(d,600,739,108,tint(a,.83),outline=a,width=5)
        txt(d,"G",600,676,102,a,True,True)
        txt(d,"SHOCK",600,794,29,a,True,True)
        column(d,122,633,324,245,"버티기","철학을 유지하는 일",a,"#FFFFFF")
        column(d,751,633,324,245,"검증","고객 신호를 읽는 일",a,"#FFFFFF")
        note(d,"작은 구매 신호가 뚜렷해지는가를 봐야 한다",a)
    elif no==23:
        heading(d,"콘텐츠는 초콜릿 판매를 도와야 한다",a)
        box(d,(80,506,1118,1033),"#F0E6E0",34)
        flow(d,["창업 스토리","관심·신뢰","제품 구매"],[242,599,959],680,a)
        for i,x in enumerate([315,486,657,826]):
            box(d,(x,911,x+104,983),"#795B4B",10)
            txt(d,"CHOC",x+52,929,22,"#FFFFFF",True,True)
        note(d,"시청자 증가와 고객 전환을 별도로 측정한다",a)
    elif no==24:
        heading(d,"수면은 구매와 효과를 구분해야 한다",a)
        box(d,(83,520,1116,1029),"#E8EDF3",33)
        column(d,120,566,437,361,"구매 이유","불면 · 스트레스 · 생활 패턴 등 문제는 서로 다르다",a,"#FFFFFF")
        column(d,641,566,440,361,"효과 검증","편안한 경험과 실제 수면 변화는 같은 주장일 수 없다",a,"#FFFFFF")
        ln(d,[(593,583),(593,930)],a,4)
        tag(d,"감정적 기대  ≠  입증된 결과",338,957,524,a)
        note(d,"건강 관련 주장에는 더 높은 근거가 필요하다",a)
    elif no==25:
        heading(d,"설명보다 실험으로 이해하는 경험",a)
        box(d,(85,515,1115,1027),"#FAECD8",34)
        flow(d,["설명 듣기","직접 실험","며칠 뒤 기억"],[236,601,964],693,a)
        # test tube
        for x in [483,564,644,721]:
            box(d,(x,911,x+31,995),tint(a,.7),11,outline=a,width=3)
            circ(d,x+15,976,9,a)
        note(d,"재미는 입구이고 이해는 남겨야 할 결과물",a)
    elif no==26:
        heading(d,"서로 다른 역량이 만나는 지점",a)
        box(d,(83,510,1117,1028),"#ECE8F2",35)
        circ(d,427,735,211,tint(a,.6))
        circ(d,782,735,211,tint(a,.78))
        txt(d,"제품 제작",348,707,32,a,True,True)
        txt(d,"팬·경험",863,707,32,a,True,True)
        box(d,(514,664,700,843),"#FFFFFF",27)
        txt(d,"새 결과",605,724,31,a,True,True)
        tag(d,"로고만 묶는 협업과 능력을 더하는 협업은 다르다",206,983,790,a)
        note(d,"파트너가 아니면 불가능한 결과가 있는가",a)
    elif no==27:
        heading(d,"콘텐츠 커뮤니티에서 구매 신뢰로",a)
        box(d,(80,508,1115,1023),"#E5EBF3",32)
        flow(d,["취향 콘텐츠","정보 공유","추천 신뢰","구매 결정"],[204,473,744,1013],705,a)
        txt(d,"커뮤니티 규모만으로 매출을 설명할 수 없다",599,971,28,a,True,True)
        note(d,"사람들이 이곳에서 보고 사면 덜 실패한다고 느끼는가",a)
    elif no==28:
        heading(d,"사진에 좋은 제품  /  매일 쓰기 좋은 제품",a)
        box(d,(82,516,559,1030),"#EDEDE7",32)
        box(d,(629,516,1114,1030),"#E7ECE4",32)
        # chairs
        for x in [314,872]:
            box(d,(x-97,731,x+97,790),13,tint(a,.56),outline=a,width=4)
            box(d,(x-102,627,x-64,740),14,tint(a,.68),outline=a,width=4)
            ln(d,[(x-72,790),(x-96,922)],a,7)
            ln(d,[(x+73,790),(x+101,922)],a,7)
        txt(d,"첫인상",317,958,32,a,True,True)
        txt(d,"반복 사용",872,958,32,a,True,True)
        note(d,"눈길을 끄는 것과 손이 오래 가는 것의 균형",a)
    elif no==29:
        heading(d,"더 많은 도구보다 더 적은 우선순위",a)
        box(d,(80,516,560,1025),"#F2EDE1",30)
        box(d,(642,516,1117,1025),"#ECEEDC",30)
        txt(d,"할 일 추가",321,558,32,a,True,True)
        txt(d,"하지 않을 일",878,558,32,a,True,True)
        for i in range(4):
            box(d,(155,654+i*75,482,711+i*75),"#FFFFFF",12)
            txt(d,"□  새 작업 "+str(i+1),175,664+i*75,23,"#4B4D50")
        for i,s in enumerate(["이번 주 핵심","할 권한 확인","멈출 작업"]):
            box(d,(712,671+i*100,1040,739+i*100),"#FFFFFF",13)
            txt(d,"✓  "+s,734,686+i*100,24,a,True)
        note(d,"멈출 수 없는 일은 우선순위에서 사라지지 않는다",a)
    elif no==30:
        heading(d,"프리미엄 서비스가 커질 때의 숙제",a)
        box(d,(80,511,1118,1026),"#EEE6E4",33)
        flow(d,["상담","전문가의 판단","서비스","팀 전수"],[205,470,738,1011],708,a)
        txt(d,"한 사람의 재능만으로는 품질을 복제하기 어렵다",602,985,27,a,True,True)
        note(d,"상담과 판단을 팀 전체가 재현할 수 있는가",a)
    else:raise ValueError(no)

manifest=[]
for row in ROWS:
    im,d,a=frame(row)
    diagram(d,row)
    dst=DEST/row[1]
    im.save(dst,format="PNG",optimize=True)
    with Image.open(dst) as check:
        assert check.format=="PNG" and check.size==(1200,1500)
        check.verify()
    assert dst.stat().st_size>15000, dst
    manifest.append({"id":row[0],"file":row[1],"size":dst.stat().st_size,
        "sha256":hashlib.sha256(dst.read_bytes()).hexdigest(),"source":row[6]})
for lo,hi in [(11,20),(21,30)]:
    sheet=Image.new("RGB",(1600,1010),"#EDEBE8")
    for i,row in enumerate(ROWS[lo-11:hi-10]):
        im=Image.open(DEST/row[1])
        im.thumbnail((290,420))
        sheet.paste(im,(15+(i%5)*320+(290-im.width)//2,23+(i//5)*490))
    sheet.save(DEST/f"contact_sheet_{lo}_{hi}_editorial.jpg",quality=89)
(DEST/"manifest_11_30_editorial.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding="utf-8")
print("[RENDERED] 20 images at 1200×1500")
for it in manifest: print(it["id"],it["file"],it["size"],it["sha256"][:12])
