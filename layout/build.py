"""우니 상세페이지를 모듈형 기본 레이아웃으로 나누고, 제품별 내용을 끼워 미리보기 HTML을 만든다.

사용: python3 layout/build.py  (저장소 루트에서 실행)
- 운영 페이지(루트 index.html)의 CSS·스크립트를 그대로 가져온다.
- 가격, 푸터, 전체 상품·구매 안내, 전화 문의, 분석 태그는 넣지 않는다.
- 모듈은 PRODUCTS의 키가 있을 때만 출력된다(필수 모듈: hero, facts, menu, product, storage, info).
"""
import html
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = (ROOT / "index.html").read_text(encoding="utf-8")
OUT = ROOT / "layout"
E = html.escape

# ---------- 운영 페이지에서 머리(CSS)와 꼬리(스크립트) 가져오기 ----------
head = SRC[: SRC.index('<main id="top">')]
head = re.sub(r"\s*<!-- Google Tag Manager -->.*?<!-- End Google Tag Manager -->", "", head, flags=re.S)
head = re.sub(r"\s*<!-- Google tag \(gtag\.js\) -->\s*<script.*?</script>\s*<script>.*?</script>", "", head, flags=re.S)
head = re.sub(r"\s*<!-- Google Tag Manager \(noscript\) -->.*?<!-- End Google Tag Manager \(noscript\) -->", "", head, flags=re.S)
head = re.sub(r'\s*<script type="application/ld\+json">.*?</script>', "", head, flags=re.S)
head = re.sub(r'\s*<link rel="canonical"[^>]*>|\s*<meta (?:property="og:|name="twitter:)[^>]*>', "", head)
head = re.sub(r'\s*<a class="nav-site nav-primary-cta"[^\n]*</a>|\s*<a class="nav-phone nav-secondary-cta"[^\n]*</a>', "", head)
head = re.sub(r'\s*<meta name="description"[^>]*>', "", head)
head = head.replace('<meta charset="utf-8">', '<meta charset="utf-8">\n    <meta name="robots" content="noindex">', 1)

tail = SRC[SRC.index('<div class="floating-tools"'):]
tail = re.sub(r'\s*<div class="floating-conversion".*?</div>', "", tail, count=1, flags=re.S)
tail = re.sub(r'\s*<div class="mobile-cta-bar".*?</div>', "", tail, count=1, flags=re.S)

head = re.sub(r'(href|src)="assets/', r'\1="../assets/', head)
head = re.sub(r"url\((['\"]?)assets/", r"url(\1../assets/", head)
tail = re.sub(r'(href|src)="assets/', r'\1="../assets/', tail)

EXTRA_CSS = """
      body{padding-bottom:0!important}
      .ph{display:flex;align-items:center;justify-content:center;width:100%;height:100%;min-height:180px;background:repeating-linear-gradient(45deg,#eef3f6 0 12px,#e5ecf1 12px 24px);color:#5f7684;font-size:13px;font-weight:800;text-align:center;padding:12px}
      .mod{position:relative}
      .mod-tag{position:absolute;top:10px;left:10px;z-index:30;background:#0f1d2b;color:#fff;font-size:11px;font-weight:800;padding:4px 9px;border-radius:999px;letter-spacing:0;pointer-events:none}
      .mod-tag.opt{background:#7a4b00}
      body.no-tags .mod-tag,body.no-tags .todo-mark{display:none}
      .todo{outline:2px dashed #f2b100;outline-offset:2px}
      body.no-tags .todo{outline:0}
      .preview-bar{position:sticky;top:0;z-index:80;display:flex;flex-wrap:wrap;gap:8px;align-items:center;padding:9px 14px;background:#0f1d2b;color:#cfe0ee;font-size:12px}
      .preview-bar b{color:#fff}.preview-bar button{border:1px solid #5d7387;background:transparent;color:#fff;border-radius:999px;padding:4px 10px;font-size:12px;cursor:pointer}
      .lineup{display:grid;gap:14px;grid-template-columns:repeat(var(--n),1fr);margin-top:22px}
      .lineup-card{border:1px solid var(--line);border-radius:20px;overflow:hidden;background:#fff;box-shadow:0 14px 40px rgba(7,59,99,.08)}
      .lineup-card .lc-photo{aspect-ratio:1/1;overflow:hidden;background:#edf2f4}.lineup-card .lc-photo img{width:100%;height:100%;object-fit:cover}
      .lineup-card .lc-body{padding:16px}.lineup-card h3{font-size:17px;font-weight:900;color:var(--navy)}
      .lineup-card p{font-size:13px;color:var(--muted);margin-top:3px}
      .lineup-card .lc-store{display:inline-block;margin-top:8px;font-size:11px;font-weight:800;padding:3px 9px;border-radius:999px;background:#e6f0fa;color:var(--navy)}
      @media(min-width:921px){.menu-grid.n1{grid-template-columns:1fr}.menu-grid.n2{grid-template-columns:1fr 1fr}.process-grid.n2{grid-template-columns:1fr 1fr}.process-grid.n3{grid-template-columns:repeat(3,1fr)}}
      @media(max-width:640px){.lineup{grid-template-columns:1fr 1fr}.lineup.n3 .lineup-card:first-child{grid-column:1/-1}}
"""
head = re.sub(r"[ \t]+\n", "\n", head)
head = head.replace("</style>", EXTRA_CSS + "    </style>", 1)


def t(s):
    """'?'로 시작하는 값은 확인이 필요한 문구로 표시한다."""
    s = s or ""
    if s.startswith("?"):
        return f'<span class="todo">{E(s[1:])}</span>'
    return s  # 일반 문구는 <br>, <strong> 등 간단한 태그를 허용


def img(src, alt, extra=""):
    if not src:
        return f'<div class="ph">사진 자리 · {E(alt)}</div>'
    return f'<img src="{src}" alt="{E(alt)}" loading="lazy" decoding="async"{extra}>'


def tag(label, optional=False):
    return f'<span class="mod-tag{" opt" if optional else ""}">{E(label)}</span>'


def head_block(label, title, desc):
    return (f'<div class="section-head reveal"><p class="section-label">{E(label)}</p>'
            f'<h2 class="section-title">{t(title)}</h2>' + (f'<p class="section-desc">{t(desc)}</p>' if desc else "") + "</div>")


# ---------- 모듈 ----------
def m_hero(d):
    h = d["hero"]
    dist = f'<p class="distance"><strong>{E(h["num"])}</strong><span>{E(h["unit"])}</span></p>' if h.get("num") else ""
    route = ""
    if h.get("route"):
        parts = []
        for i, (small, name) in enumerate(h["route"]):
            if i:
                parts.append(f'<span class="route-line{" air" if i == 1 else ""}" aria-hidden="true"></span>')
            parts.append(f'<span class="route-point">{f"<small>{E(small)}</small>" if small else ""}{E(name)}</span>')
        route = f'<div class="route">{"".join(parts)}</div>'
    rails = h.get("rail") or [None]
    cards = "".join(f'<figure class="rail-card">{img(s, d["name"] + " 대표 이미지")}</figure>' for s in rails)
    dup = "".join(f'<figure class="rail-card" aria-hidden="true">{img(s, "")}</figure>' for s in rails) if len(rails) > 1 else ""
    pack = ""
    if h.get("pack") is not None:
        pack = (f'<aside class="pack-spot"><div class="pack-photo">{img(h["pack"], d["name"] + " 완제품")}</div>'
                f'<div class="pack-caption"><small>PACK CONFIGURATION</small><strong>{t(h["packCaption"])}</strong></div></aside>')
    links = '<div class="hero-support-links"><a href="#product">제품 정보 확인</a>' + (
        '<span aria-hidden="true">·</span><a href="#process">공정 확인</a>' if "process" in d else "") + "</div>"
    return (f'<section class="hero mod">{tag("① 히어로 · 필수")}<div class="hero-copy"><p class="eyebrow">{t(h["eyebrow"])}</p>{dist}'
            f'<h1>{t(h["title"])}<br><em>{t(h["em"])}</em></h1><p>{t(h["desc"])}</p>{route}{links}</div>'
            f'<div class="hero-media"><div class="hero-rail-stage"><div class="hero-rail"><div class="rail-track"{"" if dup else " style=\"animation:none\""}>{cards}{dup}</div></div>{pack}</div></div></section>')


def m_facts(d):
    out = "".join(f'<div class="fact"><b>{t(b)}{f"<span>{E(u)}</span>" if u else ""}</b><div><small>{E(s)}</small><strong>{t(st)}</strong></div></div>'
                  for b, u, s, st in d["facts"])
    return f'<div class="facts mod">{tag("② 핵심 3칸 · 필수")}{out}</div>'


def m_gallery(d):
    g = d["gallery"]
    n = len(g["slides"])
    slides = "".join(
        f'<figure class="grade-slide{" is-active" if i == 0 else ""}" id="grade-slide-{i}" role="tabpanel" aria-hidden="{"false" if i == 0 else "true"}">'
        f'{img(s["img"], s["title"])}<figcaption class="grade-slide-caption"><strong>{t(s["title"])}</strong><span>{t(s["sub"])}</span></figcaption></figure>'
        for i, s in enumerate(g["slides"]))
    thumbs = "".join(
        f'<button class="grade-thumb{" is-active" if i == 0 else ""}" type="button" data-grade-thumb="{i}" role="tab" aria-selected="{"true" if i == 0 else "false"}" aria-controls="grade-slide-{i}">'
        f'{img(s["img"], "")}<span>{E(s["thumb"])}</span></button>' for i, s in enumerate(g["slides"]))
    dots = "".join(f'<button class="grade-dot{" is-active" if i == 0 else ""}" type="button" data-grade-dot="{i}" aria-label="{i + 1}번 사진"></button>' for i in range(n))
    proofs = "".join(f'<div class="grade-proof"><b>{i + 1:02d}</b><div><strong>{t(h)}</strong><span>{t(p)}</span></div></div>' for i, (h, p) in enumerate(g["proofs"]))
    return (f'<section class="grade-price mod" id="gallery">{tag("③ 사진 확인 · 선택", True)}{head_block(g["label"], g["title"], g["desc"])}'
            f'<div class="grade-price-grid reveal"><div class="grade-gallery" data-grade-gallery><div class="grade-slider" aria-live="polite">{slides}'
            f'<span class="grade-swipe-hint" aria-hidden="true"><i>‹</i> 밀어서 넘기기 <i>›</i></span><div class="grade-gallery-nav">'
            f'<button class="grade-gallery-btn" type="button" data-grade-prev aria-label="이전 사진">‹</button><button class="grade-gallery-btn" type="button" data-grade-next aria-label="다음 사진">›</button></div></div>'
            f'<div class="grade-thumbs" role="tablist">{thumbs}</div><div class="grade-dots" aria-hidden="true">{dots}</div></div>'
            f'<article class="grade-copy-card"><small>{E(g["cardLabel"])}</small><h2>{t(g["cardTitle"])}</h2><p>{t(g["cardDesc"])}</p>'
            f'<div class="grade-proof-list">{proofs}</div></article></div></section>')


def m_menu(d):
    m = d["menu"]
    cards = "".join(f'<article class="menu-card"><div class="menu-photo">{img(c["img"], c["title"])}</div><div class="menu-body"><small>{E(c["en"])}</small><h3>{t(c["title"])}</h3>'
                    + (f'<p>{t(c["desc"])}</p>' if c.get("desc") else "") + "</div></article>" for c in m["cards"])
    return f'<section class="menu mod" id="menu">{tag("④ 활용 · 필수 (1~3장)")}{head_block("MENU APPLICATION", m["title"], m.get("desc"))}<div class="menu-grid n{len(m["cards"])} reveal">{cards}</div></section>'


def m_product(d):
    p = d["product"]
    items = p.get("items")
    if items and len(items) > 1:  # 여러 상품: 라인업 카드
        cards = "".join(f'<article class="lineup-card"><div class="lc-photo">{img(i.get("img"), i["name"])}</div><div class="lc-body"><h3>{E(i["name"])}</h3>'
                        f'<p>{t(i["spec"])}</p><span class="lc-store">{E(i["storage"])}</span></div></article>' for i in items)
        body = f'<div class="lineup n{len(items)} reveal" style="--n:{len(items)}">{cards}</div>'
        note = f'<div class="product-note" style="margin-top:18px">{t(p["note"])}</div>' if p.get("note") else ""
        return f'<section class="product mod" id="product">{tag(f"⑤ 구성·규격 · 필수 (상품 {len(items)}개 → 카드)")}{head_block("PRODUCT DETAIL", p["title"], p.get("desc"))}{body}{note}</section>'
    specs = "".join(f"<li><span>{E(k)}</span><strong>{t(v)}</strong></li>" for k, v in p["specs"])
    mini = ""
    if p.get("mini"):
        mini = '<div class="mini-gallery reveal">' + "".join(f'<figure class="mini-card">{img(s, c)}<span>{E(c)}</span></figure>' for s, c in p["mini"]) + "</div>"
    return (f'<section class="product mod" id="product">{tag("⑤ 구성·규격 · 필수 (상품 1개 → 규격표)")}{head_block("PRODUCT DETAIL", p["title"], p.get("desc"))}'
            f'<div class="product-grid reveal"><div class="product-main">{img(p.get("img"), d["name"] + " 제품 사진")}</div>'
            f'<div class="product-side"><h3 class="spec-title">한눈에 보는 제품 규격</h3><ul class="spec-list">{specs}</ul>'
            + (f'<div class="product-note">{t(p["note"])}</div>' if p.get("note") else "") + f"</div></div>{mini}</section>")


def m_process(d):
    p = d["process"]
    cards = "".join(f'<article class="process-card"><div class="process-photo">{img(s["img"], s["title"])}</div><div class="process-body"><p class="process-no">PROCESS {i + 1:02d}</p>'
                    f'<h3>{t(s["title"])}</h3>' + (f'<p>{t(s["desc"])}</p>' if s.get("desc") else "") + "</div></article>" for i, s in enumerate(p["steps"]))
    foot = f'<p class="process-foot reveal">{t(p["foot"])}</p>' if p.get("foot") else ""
    return f'<section class="process mod" id="process">{tag("⑥ 공정 · 선택 (2~4단계)", True)}{head_block("FROM SEA TO TRAY", p["title"], p.get("desc"))}<div class="process-grid n{len(p["steps"])} reveal">{cards}</div>{foot}</section>'


def m_direct(d):
    x = d["direct"]
    pts = "".join(f'<div class="direct-point"><b>{i + 1:02d}</b><div><strong>{t(h)}</strong><span>{t(s)}</span></div></div>' for i, (h, s) in enumerate(x["points"]))
    strip = "<i>→</i>".join(f"<span>{E(s)}</span>" for s in x["strip"])
    return (f'<section class="direct mod" id="direct">{tag("⑦ 유통 구조 · 선택 (직수입 제품만)", True)}<div class="direct-inner reveal"><div class="direct-copy"><p class="section-label">WHY DIRECT MATTERS</p>'
            f'<blockquote>{t(x["quote"])}</blockquote><p>{t(x["desc"])}</p><div class="direct-points">{pts}</div><div class="direct-route-strip">{strip}</div></div></div></section>')


def m_storage(d):
    s = d["storage"]
    temps = "".join(f'<span class="temp">{t(x)}</span>' for x in s["temps"])
    card = ""
    if s.get("manual"):
        card = (f'<div class="manual-card"><strong>{E(s["manual"])}</strong><p>제품 상태에 맞는 보관 온도와 권장 해동 방법, 피해야 할 해동법을 한 페이지에서 확인하세요.</p>'
                f'<a class="manual-link" href="https://manual.oceanperu.co.kr/" target="_blank" rel="noopener noreferrer">메뉴얼 자세히 보기 →</a></div>')
    elif s.get("tips"):
        card = '<div class="manual-card"><strong>보관 · 사용 안내</strong>' + "".join(f"<p>{t(x)}</p>" for x in s["tips"]) + "</div>"
    return (f'<section class="manual mod" id="manual">{tag("⑧ 보관·해동 · 필수")}<div class="manual-inner reveal"><div><p class="section-label">STORAGE &amp; THAWING</p>'
            f'<h2 class="section-title">{t(s["title"])}</h2><p class="section-desc">{t(s["desc"])}</p><div class="temps">{temps}</div></div>{card}</div></section>')


def m_info(d):
    rows = "".join(f'<tr><th scope="row">{E(k)}</th><td style="white-space:pre-line">{t(v)}</td></tr>' for k, v in d["info"])
    return (f'<section class="info mod" id="info">{tag("⑨ 정보 고시 · 필수")}{head_block("PRODUCT INFORMATION", "제품 정보 고시", "상품별 최종 표기는 실제 제품 라벨과 별도 고시 내용을 기준으로 확인해 주세요.")}'
            f'<table class="info-table reveal"><tbody>{rows}</tbody></table></section>')


ORDER = [("hero", m_hero, None), ("facts", m_facts, None), ("gallery", m_gallery, ("#gallery", "PHOTO")), ("menu", m_menu, ("#menu", "MENU")),
         ("product", m_product, ("#product", "PRODUCT")), ("process", m_process, ("#process", "PROCESS")), ("direct", m_direct, ("#direct", "DIRECT")),
         ("storage", m_storage, ("#manual", "STORAGE")), ("info", m_info, ("#info", "INFO"))]


def page(d):
    body, nav = [], []
    for key, fn, link in ORDER:
        if key in d:
            body.append(fn(d))
            if link:
                nav.append(f'<a href="{link[0]}" data-floating-link>{link[1]}</a>')
    h = re.sub(r"<title>.*?</title>", f"<title>{E(d['title'])} | 오션페루 상세 미리보기</title>", head, count=1, flags=re.S)
    h = re.sub(r'(<nav class="nav"[^>]*>).*?(</nav>)', lambda m: m.group(1) + "".join(x.replace(" data-floating-link", "") for x in nav[:5]) + m.group(2), h, count=1, flags=re.S)
    h = h.replace("<body", "<body", 1)
    bar = (f'<div class="preview-bar"><b>{E(d["title"])}</b><span>검토용 표시: 번호표(검정 필수·갈색 선택), 노란 점선(확인 필요 문구), 빗금(사진 자리)</span>'
           '<button type="button" onclick="document.body.classList.toggle(\'no-tags\')">표시 켜기/끄기</button></div>')
    h = h.replace('<div class="page">', bar + '<div class="page">', 1)
    tl = re.sub(r'(<nav class="floating-menu-list"[^>]*>).*?(</nav>)', lambda m: m.group(1) + "".join(nav) + m.group(2), tail, count=1, flags=re.S)
    return h + '<main id="top">' + "\n".join(body) + "</main>\n</div>\n" + tl


A = "../assets/web/"
T = "img/"  # 참다랑어 이미지 (Figma v1에서 내려받은 것)
PRODUCTS = {
    # 1) 우니: 운영 페이지 내용 전체. 가격·푸터만 뺐다.
    "index": {
        "title": "페루산 우니 (전체형)", "name": "페루산 우니",
        "hero": {"eyebrow": "PERU OWN FACTORY · AIR FREIGHT · DIRECT DELIVERY", "num": "16,400", "unit": "km",
                 "title": "멀리 왔지만,", "em": "돌아서 오진 않았습니다.",
                 "desc": "오션페루는 <strong>페루 현지의 자체 공장에서 원물을 엄선하고 손질·가공한 우니</strong>를 항공편으로 한국까지 빠르게 운송합니다.<br>통관 후에는 <strong>오션페루가 직접 받아, 중간 유통망 없이 고객에게 전달</strong>하며, 산지의 공정부터 국내 전달까지 불필요한 지연을 줄이는 것이 오션페루가 신선도를 지키는 방식입니다.",
                 "route": [("자체 공장", "페루 현지"), ("통관", "오션 페루"), ("", "고객")],
                 "rail": [A + f"rail-product-0{i}.webp" for i in range(1, 5)], "pack": A + "uni-pack-front-no-text.webp", "packCaption": "100g · 20g × 5칸"},
        "facts": [("0단계", "", "MIDDLE DISTRIBUTION", "중간 유통 없는 직납 구조"), ("100", "g", "ONE PACK", "한 팩 정량 구성"), ("3", "WAYS", "MENU APPLICATION", "초밥 · 덮밥 · 곁들임")],
        "gallery": {"label": "GRADE A · PHOTO PROOF", "title": "판단 기준은<br>실제 제품의 상태입니다",
                    "desc": "사진을 좌우로 밀거나 버튼·썸네일을 눌러 제품의 정면, 사선, 포장 상태를 차례로 확인해 주세요.",
                    "slides": [{"img": A + "uni-pack-front.webp", "title": "FRONT · 정면 구성", "sub": "100g · 20g × 5칸 구성을 한눈에 확인", "thumb": "정면"},
                               {"img": A + "uni-pack-angle-no-text.webp", "title": "ANGLE · 결감과 입체감", "sub": "색, 결, 담김 상태를 다른 각도에서 확인", "thumb": "사선"},
                               {"img": A + "uni-pack-label.webp", "title": "PACKAGE · 실제 포장", "sub": "납품과 보관을 고려한 패키지 상태 확인", "thumb": "패키지"}],
                    "cardLabel": "PERU UNI · GRADE A", "cardTitle": "먼저 보여드려야 할 것은<br>제품의 상태입니다",
                    "cardDesc": "정면, 사선, 포장 사진을 먼저 보여드리는 이유는 원물과 담김 상태를 보고 판단할 수 있어야 하기 때문입니다.",
                    "proofs": [("정면 구성", "100g 한 팩을 20g × 5칸으로 나눈 구성을 확인합니다."), ("결감과 입체감", "색, 결, 담김 상태를 다른 각도에서 확인합니다."), ("실제 포장", "납품과 보관을 고려한 패키지 상태를 확인합니다.")]},
        "menu": {"title": "매장 메뉴에 바로 적용 가능한<br>3가지 활용 방식", "desc": "초밥·덮밥·곁들임 세 가지 방식으로 매장 메뉴 구성에 바로 적용할 수 있습니다. 트레이 단위로 소분되어 있어 손질 없이 바로 사용 가능합니다.",
                 "cards": [{"img": A + "menu-sushi.webp", "en": "SUSHI", "title": "초밥 · 군함", "desc": "우니의 색과 형태를 한 점에 집중해 보여주는 대표적인 활용 방식입니다."},
                           {"img": A + "menu-dong.webp", "en": "RICE BOWL", "title": "우니동 · 카이센동", "desc": "밥과 해산물 위에 더해 한 그릇의 양감과 색감을 풍성하게 구성할 수 있습니다."},
                           {"img": A + "menu-sasimi.webp", "en": "PAIRING", "title": "사시미 · 곁들임", "desc": "감태, 크래커, 육회, 단새우 등 다양한 재료와 조합해 메뉴의 폭을 넓힐 수 있습니다."}]},
        "product": {"title": "매장 사용 기준으로 확인하는<br>페루산 우니의 구성", "desc": "100g 한 팩을 20g씩 5칸으로 소분해, 매장 메뉴 구성과 사용량 관리에 바로 적용할 수 있도록 구성했습니다.",
                    "img": A + "uni-pack-front.webp",
                    "specs": [("제품명", "페루산 성게알(우니)"), ("원산지", "페루"), ("내용량", "100g / 팩"), ("트레이 구성", "20g × 5칸"), ("대표 활용", "초밥 · 덮밥 · 사시미"), ("보관", "냉장 또는 냉동")],
                    "note": "수산물의 특성상 제품마다 색상, 크기와 형태에는 자연스러운 차이가 있을 수 있습니다.",
                    "mini": [(A + "uni-pack-label.webp", "납품용 포장 상태"), (A + "uni-pack-angle-no-text.webp", "20g × 5칸 소분 구성"), (A + "uni-plated.webp", "플레이팅 활용 예시")]},
        "process": {"title": "바다에서 트레이까지,<br>과정을 숨기지 않습니다", "desc": "원물의 상태를 확인하고, 작업장에서 선별과 손질을 거쳐 사용하기 편한 트레이에 담기까지. 제품이 만들어지는 흐름을 순서대로 보여드립니다.",
                    "steps": [{"img": A + "process-origin.webp", "title": "원물 확인", "desc": "제품의 출발점인 성게 원물의 상태를 먼저 확인합니다."},
                              {"img": A + "process-check.webp", "title": "상태 선별", "desc": "원물의 상태를 살피고 작업에 적합한 성게를 구분합니다."},
                              {"img": A + "process-work.webp", "title": "선별 · 손질", "desc": "작업 공간에서 우니를 선별하고 제품화에 필요한 손질을 진행합니다."},
                              {"img": A + "uni-pack-label.webp", "title": "소분 · 포장", "desc": "20g씩 5칸 트레이에 나누어 담아 100g 한 팩으로 구성합니다."}],
                    "foot": "공정 사진은 제품이 원물에서 포장 단계로 이어지는 흐름을 이해하기 위한 자료입니다. 실제 작업 환경과 포장 형태는 생산 시점 및 상품 구성에 따라 달라질 수 있습니다."},
        "direct": {"quote": "오션페루의 신선도는<br><em>‘더 적게 거치는 구조’</em>에서 만들어집니다.",
                   "desc": "중간 유통 단계가 늘어날수록 제품이 머무는 시간과 관리 지점도 늘어납니다. 오션페루는 페루 현지 자체 공장에서 선별·가공한 제품을 항공으로 운송하고, 통관 후 직접 받아 고객에게 전달하는 흐름을 기준으로 관리합니다.",
                   "points": [("페루 현지 자체 공장", "원물 확인과 제품화의 출발점을 직접 관리합니다."), ("항공 운송", "긴 이동 과정에서 불필요한 지연을 줄입니다."), ("직접 전달", "복잡한 중간 도매망 없이 고객에게 이어집니다.")],
                   "strip": ["PERU OWN FACTORY", "AIR FREIGHT", "DIRECT DELIVERY"]},
        "storage": {"title": "좋은 상태로 받았다면,<br>좋은 상태로 사용하는 법도 중요합니다",
                    "desc": "상세페이지에서는 핵심 온도만 안내하고, 냉장·냉동 보관과 저온 해동 방법은 오션페루 공식 메뉴얼에서 자세히 확인할 수 있습니다.",
                    "temps": ["냉장 0~2℃", "냉동 -18℃ 이하", "냉장실 0~5℃ 저온 해동"], "manual": "우니 보관·해동 공식 메뉴얼"},
        "info": [("제품명", "페루산 성게알(우니)"), ("수입원", "상품 별도 표기"), ("판매원", "주식회사 오션페루"), ("원산지", "페루"), ("내용량", "100g"),
                 ("원재료명 및 함량", "상품 별도 표기"), ("보관 방법", "냉장 또는 냉동 보관"), ("소비기한", "상품 별도 표기")],
    },
    # 2) 참다랑어: 기존 Figma 상세페이지 내용을 결합한 축약형 (유통 구조 모듈 없음)
    "preview-tuna": {
        "title": "참다랑어 (축약형)", "name": "참다랑어",
        "hero": {"eyebrow": "원양산 참다랑어 · 참치뱃살 3번 도로", "title": "기름짐과 담백함,", "em": "딱 그 사이",
                 "desc": "배꼽도로, 오도로, 주도로가 함께 붙은 <strong>참치뱃살 3번</strong>입니다. 기름진 부위가 부담스러운 분께 맞는 균형 잡힌 맛입니다.",
                 "rail": [T + "hero.webp"], "pack": T + "part-02.webp", "packCaption": "뱃살 3번 · 6 / 12kg"},
        "facts": [("원양산", "", "ORIGIN", "태평양 · 인도양"), ("3", "부위", "CUT", "배꼽 · 오도로 · 주도로"), ("3", "WAYS", "MENU APPLICATION", "회 · 초밥 · 덮밥")],
        "gallery": {"label": "PART CHECK", "title": "기름진 게 부담된다면,<br>3번 도로", "desc": "부위별 맛의 차이를 사진으로 확인해 주세요.",
                    "slides": [{"img": T + "part-01.webp", "title": "배꼽도로", "sub": "꼬독함 · 고소함", "thumb": "배꼽"},
                               {"img": T + "part-02.webp", "title": "오도로 (대뱃살)", "sub": "부드러움 · 풍부한 지방", "thumb": "오도로"},
                               {"img": T + "part-03.webp", "title": "주도로 (중뱃살)", "sub": "담백함 · 깔끔함", "thumb": "주도로"}],
                    "cardLabel": "BLUEFIN TUNA · BELLY 3", "cardTitle": "한 덩어리에서<br>세 가지 맛", "cardDesc": "뱃살 3번은 세 부위가 이어져 있어 메뉴에 따라 나눠 쓸 수 있습니다.",
                    "proofs": [("배꼽도로", "꼬독함 · 고소함"), ("오도로 (대뱃살)", "부드러움 · 풍부한 지방"), ("주도로 (중뱃살)", "담백함 · 깔끔함")]},
        "menu": {"title": "덮밥부터 회·초밥까지", "cards": [{"img": T + "use-01.webp", "en": "RICE BOWL", "title": "덮밥"}, {"img": T + "use-02.webp", "en": "SASHIMI · SUSHI", "title": "회 · 초밥"}]},
        "product": {"title": "참다랑어 뱃살 3번 구성", "img": T + "detail-main.webp",
                    "specs": [("제품명", "참다랑어 뱃살 3번"), ("원산지", "원양산 (태평양/인도양)"), ("규격", "6 / 12kg"), ("부위", "배꼽도로 · 오도로 · 주도로"), ("대표 활용", "회 · 초밥 · 덮밥"), ("보관", "냉동")],
                    "note": "원물 크기에 따라 형태·중량에 차이가 있을 수 있어요."},
        "process": {"title": "재단부터 배송까지", "steps": [{"img": T + "step-01.webp", "title": "2.5cm 재단"}, {"img": T + "step-02.webp", "title": "비닐 밀봉"}, {"img": T + "step-03.webp", "title": "냉동 택배"}]},
        "storage": {"title": "받은 즉시 냉동 보관해 주세요", "desc": "냉동 상태 그대로 아이스 박스와 아이스 팩으로 포장해 보내드립니다.",
                    "temps": ["?냉동 -40℃ 이하 (기존 표기 40°C, 확인 필요)", "냉장실 저온 해동"], "tips": ["?해동 방법 문구 확인 필요"]},
        "info": [("제품명", "참다랑어 뱃살 3번"), ("수입원", "상품 별도 표기"), ("판매원", "주식회사 오션페루"), ("원산지", "원양산 (태평양/인도양)"), ("내용량", "6 / 12kg"),
                 ("원재료명 및 함량", "상품 별도 표기"), ("보관 방법", "냉동 보관"), ("소비기한", "상품 별도 표기")],
    },
    # 3) 초생강 3종: 한 페이지에 여러 상품, 최소 구성 (사진 확인·공정·유통 구조 없음)
    "preview-ginger": {
        "title": "초생강 3종 (최소형 · 여러 상품)", "name": "초생강",
        "hero": {"eyebrow": "스시 · 사시미 곁들임", "title": "느끼함을", "em": "상쾌함으로",
                 "desc": "편과 채, 용량을 골라 쓰는 <strong>초생강 3종</strong>입니다.", "rail": [None]},
        "facts": [("?확인", "", "ORIGIN", "원산지"), ("3", "종", "LINE-UP", "편 · 채 선택"), ("2", "WAYS", "MENU APPLICATION", "횟감 · 구이")],
        "menu": {"title": "어떤 요리에도 깔끔하게", "cards": [{"img": None, "en": "SASHIMI", "title": "횟감 곁들임"}, {"img": None, "en": "GRILL", "title": "구이 곁들임"}]},
        "product": {"title": "취향대로 고르는 3가지", "items": [
            {"name": "백초생강 (편)", "spec": "1.3kg × 10팩", "storage": "냉장 0~2℃"},
            {"name": "백초생강 (채)", "spec": "?1.3kg × 10팩", "storage": "냉장 0~2℃"},
            {"name": "채초생강", "spec": "100g × 100팩", "storage": "냉장 0~2℃"}]},
        "storage": {"title": "받은 즉시 냉장 보관해 주세요", "desc": "개봉 후에는 밀봉해 냉장 보관하고 가급적 빨리 사용해 주세요.", "temps": ["냉장 0~2℃"]},
        "info": [("제품명", "백초생강 (편)\n백초생강 (채)\n채초생강"), ("판매원", "주식회사 오션페루"), ("원산지", "?확인 필요"),
                 ("내용량", "백초생강 (편): 1.3kg × 10팩\n백초생강 (채): 1.3kg × 10팩 (확인 필요)\n채초생강: 100g × 100팩"),
                 ("원재료명 및 함량", "상품 별도 표기"), ("보관 방법", "냉장 0~2℃"), ("소비기한", "상품 별도 표기")],
    },
}

if __name__ == "__main__":
    for name, d in PRODUCTS.items():
        (OUT / f"{name}.html").write_text(re.sub(r"[ \t]+\n", "\n", page(d)), encoding="utf-8")
        print("wrote", name)
