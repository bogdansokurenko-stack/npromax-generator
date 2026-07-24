# -*- coding: utf-8 -*-
"""NPROMAX static site generator. Corporate colors: orange #EE7A0E / black / white."""
import os, re, json, html
from build_lib import build_cards, translit, esc, SITE

os.makedirs(os.path.join(SITE,'assets'), exist_ok=True)

CATS = [
 ('kava-v-zernakh','Кава в зернах','Зернова кава для кавомашин, турки та еспресо','beans','для кавомашини',
  'Кава в зернах NPROMAX — це моносорти 100% арабіки та ароматизовані зерна у форматі 1 кг. Спочатку — натуральні моносорти, наприкінці списку — ароматизована кава. Ідеальний вибір для кавомашин, гейзерних кавоварок і турки після помелу.'),
 ('svizhomelena-kava','Свіжомелена кава','Мелена кава — більше аромату в кожній чашці','ground','свіжий помел',
  'Свіжомелена кава NPROMAX — вибір для тих, хто хоче отримати максимум аромату без власної кавомолки. Кожен сорт краще розкривається саме у вашому способі приготування — від турки до фільтра.'),
 ('kapsuly-nespresso','Капсули, сумісні з Nespresso Original','Насичений еспресо у зручній капсулі','ncap','сумісні з Original',
  'Капсули NPROMAX, сумісні з системою Nespresso® Original — це насичений еспресо вдома та в офісі без складнощів. Обирайте бленди Premium, Espresso, Robusta або Decaffeinato.'),
 ('kapsuly-dolce-gusto','Капсули, сумісні з Dolce Gusto','Кава та напої для системи Dolce Gusto','dcap','сумісні з системою',
  'Капсули NPROMAX, сумісні з системою Dolce Gusto® — кавові бленди для щоденної чашки. Зручний формат для дому та офісу.'),
 ('napoyi-v-kapsulakh','Напої в капсулах','Чай, какао, капучино та матча у капсулах','drink','не тільки кава',
  'Напої в капсулах NPROMAX — чай, гарячий шоколад, капучино, молоко та матча, сумісні з системами Nespresso® та Dolce Gusto®. Урізноманітте свій кавовий куточок.'),
 ('monodozy-ese','E.S.E. монодози 44 мм','Чалди для еспресо-кавоварок стандарту E.S.E.','ese','44 мм для еспресо',
  'E.S.E. монодози NPROMAX стандарту 44 мм — ароматна кава з пінкою для кавоварок, що підтримують стандарт E.S.E. Готова порція для ідеального еспресо без зайвих зусиль.'),
 ('arabika-monosorty','Арабіка та моносорти','100% арабіка з різних куточків світу','mono','100% арабіка',
  'Моносорти 100% арабіки NPROMAX — кава з Ефіопії, Бразилії, Колумбії, Гватемали та інших країн. Для тих, хто цінує чистий смак походження та м’яку арабіку.'),
 ('kavovi-kupazhi','Кавові купажі','Збалансовані бленди арабіки та робусти','blend','арабіка + робуста',
  'Кавові купажі NPROMAX — збалансовані бленди арабіки та робусти у капсулах і монодозах. Щільне тіло, стабільна крема та насичений смак еспресо.'),
 ('kava-bez-kofeinu','Кава без кофеїну','Decaf — смак кави без кофеїну','decaf','decaf',
  'Кава без кофеїну NPROMAX — повноцінний смак улюбленої кави без кофеїну. Зерно, капсули та монодози decaf для вечірньої чашки.'),
 ('kava-dlya-biznesu','Кава для бізнесу','Опт, HoReCa, офіс та вендинг','b2b','опт та HoReCa',
  'Кава для бізнесу NPROMAX — ящики капсул, монодози та зернова кава 1 кг для офісів, кафе, ресторанів, HoReCa та вендингу. Вигідні формати та регулярні поставки.'),
]
CATMAP = {c[0]:c for c in CATS}
BAND_IMG = {
 'kava-v-zernakh':'band-beans.jpg','svizhomelena-kava':'band-ground.jpg',
 'kapsuly-nespresso':'band-espresso.jpg','kapsuly-dolce-gusto':'band-flatwhite.jpg',
 'napoyi-v-kapsulakh':'band-drinks.jpg','monodozy-ese':'band-portafilter.jpg',
 'arabika-monosorty':'band-sack.jpg','kavovi-kupazhi':'band-mix.jpg',
 'kava-bez-kofeinu':'band-decaf.jpg','catalog':'band-texture.jpg','academy':'band-book.jpg',
}
def band_open(key):
    img=BAND_IMG.get(key)
    if img:
        return f'<div class="cat-band cat-band-photo" style="background-image:linear-gradient(90deg, var(--crema) 40%, rgba(242,231,213,.72) 58%, rgba(242,231,213,.10) 90%), url(&#39;assets/img/{img}&#39;)">'
    return '<div class="cat-band">' 
NAV = ['kava-v-zernakh','svizhomelena-kava','kapsuly-nespresso','kapsuly-dolce-gusto','monodozy-ese','arabika-monosorty','kava-dlya-biznesu']

def money(v):
    return f"{int(round(v)):,}".replace(',', ' ')

def logo_svg(h=30, dark=False):
    # Преміальний мінімалістичний знак: кавове зерно в колі + чистий вордмарк NPRO/MAX.
    # Монохромно-адаптивний: 'ink' світлішає на темному фоні, помаранчевий акцент постійний.
    ink = '#F4EEE6' if dark else '#241812'
    return f'''<svg viewBox="0 0 292 60" height="{h}" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="NPROMAX" style="display:block">
<g transform="translate(30,30)"><circle r="25" fill="#EE7A0E"/><circle r="25" fill="none" stroke="#000" stroke-opacity=".06" stroke-width="1.5"/><path d="M0,-16.5 C 10.5,-6 -10.5,6 0,16.5" stroke="#fff" stroke-width="3.1" fill="none" stroke-linecap="round" opacity=".96"/></g>
<text x="67" y="40" font-family="'Segoe UI',system-ui,-apple-system,Arial,sans-serif" font-weight="800" font-size="33" letter-spacing="0.4" fill="{ink}">NPRO<tspan fill="#EE7A0E">MAX</tspan></text>
</svg>'''

ICON = {
 'search':'<svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="7"/><path d="M21 21l-4-4"/></svg>',
 'cart':'<svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2"><circle cx="9" cy="20" r="1.4"/><circle cx="18" cy="20" r="1.4"/><path d="M2 3h3l2.4 12.3a2 2 0 0 0 2 1.7h8.2a2 2 0 0 0 2-1.6L23 7H6"/></svg>',
 'menu':'<svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 6h18M3 12h18M3 18h18"/></svg>',
 'arrow':'<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 12h14M13 6l6 6-6 6"/></svg>',
 'check':'<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="#EE7A0E" stroke-width="2.5"><path d="M20 6L9 17l-5-5"/></svg>',
 'phone':'<svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3 19.5 19.5 0 0 1-6-6 19.8 19.8 0 0 1-3-8.6A2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1 1 .4 1.9.7 2.8a2 2 0 0 1-.5 2.1L8.1 9.9a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.8.7a2 2 0 0 1 1.7 2z"/></svg>',
 'truck':'<svg viewBox="0 0 24 24" width="26" height="26" fill="none" stroke="#EE7A0E" stroke-width="1.8"><path d="M1 3h15v13H1zM16 8h4l3 3v5h-7"/><circle cx="5.5" cy="18.5" r="2"/><circle cx="18.5" cy="18.5" r="2"/></svg>',
 'shield':'<svg viewBox="0 0 24 24" width="26" height="26" fill="none" stroke="#EE7A0E" stroke-width="1.8"><path d="M12 2l8 3v6c0 5-3.4 9-8 11-4.6-2-8-6-8-11V5z"/><path d="M9 12l2 2 4-4"/></svg>',
 'refresh':'<svg viewBox="0 0 24 24" width="26" height="26" fill="none" stroke="#EE7A0E" stroke-width="1.8"><path d="M3 12a9 9 0 0 1 15-6.7L21 8M21 3v5h-5M21 12a9 9 0 0 1-15 6.7L3 16M3 21v-5h5"/></svg>',
 'star':'<svg viewBox="0 0 24 24" width="26" height="26" fill="none" stroke="#EE7A0E" stroke-width="1.8"><path d="M12 2l3 6.3 6.9 1-5 4.9 1.2 6.8L12 17.8 5.9 21l1.2-6.8-5-4.9 6.9-1z"/></svg>',
}

def layout(title, desc, body, active='', canonical=''):
    navlinks = ''.join(
        f'<a href="{s}.html" class="{"nav-a active" if s==active else "nav-a"}">{CATMAP[s][1] if len(CATMAP[s][1])<20 else CATMAP[s][2].split("—")[0]}</a>'
        for s in NAV)
    # shorter nav labels
    short = {'kava-v-zernakh':'Кава в зернах','svizhomelena-kava':'Свіжомелена','kapsuly-nespresso':'Nespresso',
             'kapsuly-dolce-gusto':'Dolce Gusto','monodozy-ese':'E.S.E. монодози','arabika-monosorty':'Арабіка','kava-dlya-biznesu':'Для бізнесу'}
    navlinks = ''.join(f'<a href="{s}.html" class="nav-a{" active" if s==active else ""}">{short[s]}</a>' for s in NAV)
    # NPX-018: dropdown «Каталог» з усіма 10 категоріями (desktop; на mobile усе є в drawer)
    cat_items = ''.join(
        '<a href="%s.html" role="menuitem"%s>%s</a>' % (c[0], ' class="active"' if c[0]==active else '', esc(c[1]))
        for c in CATS)
    cat_top_cls = 'nav-a active' if active=='catalog' else 'nav-a'
    catalog_dd = ('<div class="nav-drop">'
        + '<a href="catalog.html" class="%s" aria-haspopup="true" aria-expanded="false">Каталог ▾</a>' % cat_top_cls
        + '<div class="nav-menu" role="menu">' + cat_items + '</div></div>')
    navlinks = catalog_dd + navlinks
    drawer = ''.join(f'<a href="{c[0]}.html">{c[1]}</a>' for c in CATS)
    return f'''<!DOCTYPE html>
<html lang="uk">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="https://www.npromax.com.ua/{canonical}">
<link rel="icon" type="image/svg+xml" href="data:image/svg+xml,%3Csvg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 64 64%22%3E%3Crect width=%2264%22 height=%2264%22 rx=%2214%22 fill=%22%23EE7A0E%22/%3E%3Cg transform=%22translate(32,32) rotate(-28)%22%3E%3Cellipse rx=%2214%22 ry=%2221%22 fill=%22%23fff%22/%3E%3Cpath d=%22M0,-19 C 9,-7 -9,7 0,19%22 stroke=%22%23EE7A0E%22 stroke-width=%224%22 fill=%22none%22 stroke-linecap=%22round%22/%3E%3C/g%3E%3C/svg%3E">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:type" content="website">
<meta property="og:image" content="https://www.npromax.com.ua/assets/img/mood.jpg">
<meta property="og:locale" content="uk_UA">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#221510">
<link rel="stylesheet" href="assets/style.css?v=9">
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"Organization","name":"NPROMAX","url":"https://www.npromax.com.ua/","email":"info@npromax.com.ua","description":"Інтернет-магазин кави NPROMAX: зернова, свіжомелена, капсульна кава, E.S.E. монодози та рішення для бізнесу.","sameAs":["https://npro.prom.ua"]}}</script>
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"WebSite","name":"NPROMAX","url":"https://www.npromax.com.ua/","inLanguage":"uk-UA","potentialAction":{{"@type":"SearchAction","target":"https://www.npromax.com.ua/catalog.html?q={{search_term_string}}","query-input":"required name=search_term_string"}}}}</script>
</head>
<body>
<div class="topbar">
  <div class="wrap tb">
    <span>Доставка по всій Україні · Нова Пошта</span>
    <span class="tb-right">
      <a href="mailto:info@npromax.com.ua">{ICON['phone']} info@npromax.com.ua</a>
      <span>Пн–Пт 9:00–18:00</span>
    </span>
  </div>
</div>
<header class="header">
  <div class="wrap hd">
    <button class="burger" onclick="toggleMenu()" aria-label="Меню">{ICON['menu']}</button>
    <a href="/" class="logo">{logo_svg(34)}</a>
    <nav class="nav">{navlinks}</nav>
    <div class="hd-actions">
      <button class="icon-btn" id="searchToggle" onclick="toggleSearch()" aria-label="Пошук" aria-controls="searchbar" aria-expanded="false">{ICON['search']}</button>
      <a href="cart.html" class="icon-btn cart-link" aria-label="Кошик">{ICON['cart']}<span class="cart-badge" id="cartBadge">0</span></a>
    </div>
  </div>
  <div class="searchbar" id="searchbar"><div class="wrap"><input type="text" id="siteSearch" placeholder="Пошук: арабіка, капсули, Ефіопія, артикул…" oninput="siteSearch(this.value)" onkeydown="searchKey(event)"><div id="searchResults" class="search-results"></div></div></div>
</header>
<div class="drawer" id="drawer">
  <div class="drawer-in">
    <div class="drawer-h"><span>Каталог</span><button onclick="toggleMenu()" aria-label="Закрити">✕</button></div>
    {drawer}
    <a href="orenda-kavomashyny.html">Оренда кавомашини</a><a href="academy.html">Академія смаку</a><a href="about.html">Про бренд</a><a href="dostavka-i-oplata.html">Доставка й оплата</a><a href="kontakty.html">Контакти</a>
  </div>
</div>
<main>{body}</main>
<footer class="footer">
  <div class="wrap ft">
    <div class="ft-col ft-brand">
      <div class="ft-logo">{logo_svg(30, True)}</div>
      <p>Кава, яка дає максимум смаку без зайвої складності — для дому, офісу й бізнесу.</p>
      <p class="ft-slogan">NPROMAX — кава, яку хочеться повторити</p>
    </div>
    <div class="ft-col"><h4>Каталог</h4>
      <a href="kava-v-zernakh.html">Кава в зернах</a><a href="svizhomelena-kava.html">Свіжомелена кава</a>
      <a href="kapsuly-nespresso.html">Капсули Nespresso</a><a href="kapsuly-dolce-gusto.html">Капсули Dolce Gusto</a>
      <a href="monodozy-ese.html">E.S.E. монодози</a></div>
    <div class="ft-col"><h4>Інформація</h4>
      <a href="about.html">Про бренд</a><a href="dostavka-i-oplata.html">Доставка й оплата</a>
      <a href="povernennya.html">Повернення та обмін</a><a href="kontakty.html">Контакти</a>
      <a href="privacy.html">Політика конфіденційності</a><a href="oferta.html">Публічна оферта</a><a href="terms.html">Користувацька угода</a>
      <a href="kava-dlya-biznesu.html">Кава для бізнесу</a><a href="orenda-kavomashyny.html">Оренда кавомашини</a><a href="academy.html">Академія смаку</a></div>
    <div class="ft-col"><h4>Контакти</h4>
      <a href="mailto:info@npromax.com.ua">info@npromax.com.ua</a>
      <a href="kontakty.html">Форма зв'язку</a>
      <p class="ft-small">Пн–Пт 9:00–18:00 · Україна</p></div>
  </div>
  <div class="wrap ft-legal">
    <span>© 2026 NPROMAX. Усі права захищені.</span>
    <span class="ft-disc">Nespresso® / Dolce Gusto® — торговельні марки їхніх власників. NPROMAX не афілійований з ними; назви позначають технічну сумісність.</span>
  </div>
</footer>
<script src="assets/app.js"></script>
</body>
</html>'''

# ---------- product card ----------
def badge(card):
    label=None
    if card['monosort']: label='100% арабіка'
    elif card['decaf']: label='Без кофеїну'
    elif card['aroma']: label='Ароматизована'
    return f'<span class="bdg">{label}</span>' if label else ''

def price_html(card):
    pfx = 'від ' if len(card['variants'])>1 else ''
    return f'<div class="price"><span class="now">{pfx}{money(card["price_min"])} ₴</span></div>'

def card_html(card):
    data = f'data-slug="{esc(card["slug"])}" data-type="{card["type"]}" data-price="{int(card["price_min"])}" data-comp="{esc(card["composition"] or "")}" data-country="{esc(card["country"] or "")}" data-avail="{1 if card["available"] else 0}" data-aroma="{1 if card["aroma"] else 0}" data-decaf="{1 if card["decaf"] else 0}" data-name="{esc(card["title"].lower())}"'
    avail = '<span class="in-stock">В наявності</span>' if card['available'] else '<span class="no-stock">Немає</span>'
    return f'''<article class="card" {data}>
  <a href="p-{card['slug']}.html" class="card-img"><img src="{esc(card['image'])}" alt="{esc(card['title'])} — фото упаковки" loading="lazy" width="400" height="400"><div class="badges">{badge(card)}</div></a>
  <div class="card-body">
    <a href="p-{card['slug']}.html" class="card-title">{esc(card['title'])}</a>
    <div class="card-meta">{avail}{(' · '+esc(card['country'])) if card['country'] else ''}</div>
    {price_html(card)}
    <button class="btn btn-buy" onclick='addToCart({json.dumps({"slug":card["slug"],"sku":card["vendor_code"] or "","title":card["title"],"price":card["price_min"],"img":card["image"],"variant":card["variants"][0]["label"]}, ensure_ascii=False)})'>У кошик</button>
  </div>
</article>'''

CSS = r'''
:root{
 --orange:#EE7A0E; --orange-d:#D96A05; --orange-l:#FBEFE0;
 --ink:#241812; --ink2:#43322a; --muted:#6f5d4c; --line:#e7dccb;
 --bg:#fff; --soft:#f6f0e4; --crema:#f2e7d5; --espresso:#221510; --green:#3f7a3f; --radius:12px;
 --wrap:1200px; --font:'Segoe UI',system-ui,-apple-system,Roboto,Arial,sans-serif;
}
*{box-sizing:border-box;margin:0;padding:0}
html{scroll-behavior:smooth}
body{font-family:var(--font);color:var(--ink);background:var(--bg);line-height:1.55;font-size:15px}
a{color:inherit;text-decoration:none}
img{max-width:100%;display:block}
.wrap{max-width:var(--wrap);margin:0 auto;padding:0 20px}
h1,h2,h3,h4{line-height:1.2;font-weight:800}
h1{font-size:34px}h2{font-size:26px}
.btn{display:inline-flex;align-items:center;justify-content:center;gap:8px;border:none;cursor:pointer;font-family:inherit;
 font-weight:700;font-size:14px;padding:12px 22px;border-radius:10px;transition:.15s;background:var(--orange);color:#fff}
.btn:hover{background:var(--orange-d)}
.btn-ghost{background:transparent;color:var(--ink);border:2px solid var(--ink)}
.btn-ghost:hover{background:var(--ink);color:#fff}
.btn-outline{background:transparent;color:var(--orange);border:2px solid var(--orange)}
.btn-outline:hover{background:var(--orange);color:#fff}
.btn-buy{width:100%;margin-top:10px;padding:10px}
.btn-lg{padding:15px 30px;font-size:16px}
/* topbar */
.topbar{background:var(--espresso);color:#cfc2b5;font-size:12.5px}
.tb{display:flex;justify-content:space-between;align-items:center;height:36px}
.tb-right{display:flex;gap:18px;align-items:center}
.tb-right a{display:inline-flex;align-items:center;gap:6px}
.tb-right a:hover{color:#fff}
.langs b{color:var(--orange)}
/* header */
.header{position:sticky;top:0;z-index:50;background:#fff;border-bottom:1px solid var(--line)}
.hd{display:flex;align-items:center;gap:24px;height:70px}
.logo{flex-shrink:0}
.nav{display:flex;gap:15px;flex:1}
.nav-a{font-size:13.5px;font-weight:600;color:var(--ink2);padding:6px 0;border-bottom:2px solid transparent;white-space:nowrap}
.nav-a:hover,.nav-a.active{color:var(--orange);border-color:var(--orange)}
/* NPX-018 dropdown «Каталог» */
.nav-drop{position:relative}
.nav-menu{position:absolute;top:100%;left:0;min-width:230px;background:#fff;border:1px solid var(--line);border-radius:10px;
 box-shadow:0 12px 30px rgba(0,0,0,.10);padding:6px;display:none;z-index:60}
.nav-drop:hover .nav-menu,.nav-drop:focus-within .nav-menu{display:block}
.nav-menu a{display:block;padding:9px 12px;border-radius:8px;font-size:13.5px;font-weight:500;color:var(--ink2);white-space:nowrap}
.nav-menu a:hover,.nav-menu a.active{background:var(--soft);color:var(--orange)}
.hd-actions{display:flex;gap:6px;align-items:center}
.icon-btn{background:none;border:none;cursor:pointer;color:var(--ink);padding:8px;border-radius:8px;position:relative;display:inline-flex}
.icon-btn:hover{background:var(--soft)}
.cart-badge{position:absolute;top:2px;right:2px;background:var(--orange);color:#fff;font-size:10px;font-weight:700;min-width:16px;height:16px;border-radius:8px;display:flex;align-items:center;justify-content:center;padding:0 4px}
.burger{display:none;background:none;border:none;cursor:pointer;color:var(--ink)}
.searchbar{display:none;border-top:1px solid var(--line);padding:14px 0;background:#fff}
.searchbar.open{display:block}
.searchbar input{width:100%;padding:12px 16px;border:2px solid var(--line);border-radius:10px;font-size:15px;font-family:inherit}
.searchbar input:focus{outline:none;border-color:var(--orange)}
.search-results{margin-top:10px}
.search-results a{display:flex;gap:10px;align-items:center;padding:8px;border-radius:8px}
.search-results a:hover{background:var(--soft)}
.search-results img{width:38px;height:38px;object-fit:cover;border-radius:6px}
/* drawer */
.drawer{position:fixed;inset:0;background:rgba(0,0,0,.4);z-index:100;display:none}
.drawer.open{display:block}
.drawer-in{position:absolute;left:0;top:0;bottom:0;width:290px;background:#fff;padding:0 0 20px;overflow:auto}
.drawer-h{display:flex;justify-content:space-between;align-items:center;padding:18px 20px;border-bottom:1px solid var(--line);font-weight:800;font-size:18px}
.drawer-h button{background:none;border:none;font-size:20px;cursor:pointer}
.drawer-in a{display:block;padding:12px 20px;border-bottom:1px solid var(--soft);font-weight:500}
.drawer-in a:hover{background:var(--soft);color:var(--orange)}
/* hero */
.hero{background:linear-gradient(95deg, rgba(24,13,7,.95) 0%, rgba(24,13,7,.82) 42%, rgba(24,13,7,.45) 75%, rgba(24,13,7,.30) 100%), url('img/hero-bg.jpg') center right/cover no-repeat var(--espresso);color:#fff;position:relative;overflow:hidden}
.hero-b2b{background:linear-gradient(95deg, rgba(24,13,7,.95) 0%, rgba(24,13,7,.82) 42%, rgba(24,13,7,.40) 100%), url('img/b2b-hero.jpg') center right/cover no-repeat var(--espresso)}
.hero-in{padding:70px 0 76px;position:relative;z-index:2;max-width:640px}
.hero .kicker{color:var(--orange);letter-spacing:3px;font-size:13px;font-weight:700;margin-bottom:16px}
.hero h1{font-size:46px;line-height:1.08;margin-bottom:18px}
.hero h1 span{color:var(--orange)}
.hero p{color:#c9c9c9;font-size:18px;margin-bottom:30px;max-width:520px}
.hero-cta{display:flex;gap:14px;flex-wrap:wrap}
.hero-cta .btn-ghost{color:#fff;border-color:#5a4433}
.hero-cta .btn-ghost:hover{background:#fff;color:var(--ink)}
.hero-deco{position:absolute;right:-80px;top:0;bottom:0;width:50%;background:var(--orange);transform:skewX(-12deg);opacity:.14;z-index:1}
.hero-bean{position:absolute;right:6%;top:50%;transform:translateY(-50%);z-index:2;font-size:200px;opacity:.08}
/* strip */
.strip{background:var(--soft);border-bottom:1px solid var(--line)}
.strip-in{display:grid;grid-template-columns:repeat(4,1fr);gap:16px;padding:22px 0}
.strip-item{display:flex;gap:12px;align-items:center}
.strip-item b{display:block;font-size:14px}
.strip-item span{font-size:12.5px;color:var(--muted)}
/* sections */
.section{padding:56px 0}
.section-h{margin-bottom:28px}
.section-h .sub{color:var(--muted);margin-top:6px;font-size:15px;font-weight:400}
.section-h.row{display:flex;justify-content:space-between;align-items:flex-end}
.section-h .more{color:var(--orange);font-weight:700;font-size:14px;display:inline-flex;gap:6px;align-items:center}
/* categories */
.cat-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:18px}
.cat-card{background:#fff;border:1px solid var(--line);border-radius:var(--radius);padding:22px;transition:.15s;position:relative;overflow:hidden}
.cat-card:hover{border-color:var(--orange);transform:translateY(-3px);box-shadow:0 10px 30px rgba(0,0,0,.06)}
.cat-ic{width:46px;height:46px;border-radius:10px;background:var(--orange-l);display:flex;align-items:center;justify-content:center;margin-bottom:14px}
.cat-card h3{font-size:17px;margin-bottom:6px}
.cat-card p{color:var(--muted);font-size:13px;margin-bottom:12px}
.cat-hint{display:inline-block;background:var(--soft);color:var(--ink2);font-size:11.5px;font-weight:600;padding:4px 10px;border-radius:20px}
.cat-count{position:absolute;top:20px;right:20px;font-size:13px;font-weight:700;color:var(--orange)}
.cat-card-img{padding:0;overflow:hidden}
.cc-img{position:relative;height:158px;background:var(--soft)}
.cc-img img{width:100%;height:100%;object-fit:cover;display:block}
.cc-img:after{content:'';position:absolute;inset:0;background:linear-gradient(180deg,rgba(34,21,16,.05),rgba(34,21,16,0) 40%)}
.cc-count{position:absolute;top:12px;right:12px;background:rgba(255,255,255,.95);border-radius:20px;padding:3px 11px;font-size:13px;font-weight:800;color:var(--orange);z-index:2}
.cc-body{padding:16px 20px 20px}
.cat-card-img h3{margin-bottom:6px}
/* product grid + card */
.grid{display:grid;grid-template-columns:repeat(4,1fr);gap:18px}
.card{background:#fff;border:1px solid var(--line);border-radius:var(--radius);overflow:hidden;display:flex;flex-direction:column;transition:.15s}
.card:hover{border-color:var(--orange);box-shadow:0 8px 26px rgba(0,0,0,.07)}
.card-img{position:relative;display:block;aspect-ratio:1;background:var(--soft)}
.card-img img{width:100%;height:100%;object-fit:cover}
.badges{position:absolute;top:10px;left:10px;display:flex;flex-direction:column;gap:5px;align-items:flex-start}
.bdg{font-size:10px;font-weight:600;padding:3px 9px;border-radius:12px;background:rgba(255,255,255,.94);color:var(--ink2);border:1px solid var(--line)}
.bdg-sale{background:#e23b3b}.bdg-green{background:var(--green)}.bdg-orange{background:var(--orange)}.bdg-dark{background:var(--ink)}
.card-body{padding:14px;display:flex;flex-direction:column;flex:1}
.card-title{font-size:12.5px;font-weight:500;color:var(--ink2);line-height:1.4;min-height:34px}
.card-title:hover{color:var(--orange)}
.card-meta{font-size:12px;color:var(--muted);margin:7px 0}
.in-stock{color:var(--green);font-weight:600}.no-stock{color:#c33}
.price{display:flex;align-items:baseline;gap:8px;margin-top:auto}
.price .now{font-size:17px;font-weight:700;color:var(--ink)}
.price .old{font-size:13px;color:var(--muted);text-decoration:line-through}
/* how to choose */
.chips{display:flex;gap:10px;flex-wrap:wrap}
.chip{background:#fff;border:1px solid var(--line);border-radius:24px;padding:10px 18px;font-size:14px;font-weight:600;cursor:pointer;transition:.15s}
.chip:hover{border-color:var(--orange);color:var(--orange)}
/* b2b banner */
.b2b-band{background:var(--espresso);border-radius:16px;padding:34px 40px;display:flex;align-items:center;gap:24px;color:#fff;flex-wrap:wrap}
.b2b-band .kicker{color:var(--orange);letter-spacing:2px;font-size:12px;font-weight:700;margin-bottom:8px}
.b2b-band h2{margin-bottom:6px}
.b2b-band p{color:#bdbdbd;font-size:15px}
.b2b-band .b2b-txt{flex:1;min-width:260px}
.aroma-divider{grid-column:1/-1;display:flex;align-items:center;gap:16px;margin:20px 0 2px;font-weight:800;font-size:18px;color:var(--ink)}
.aroma-divider:before,.aroma-divider:after{content:'';flex:1;height:1px;background:var(--line)}
.cat-band-photo{background-size:cover!important;background-position:right center!important;background-repeat:no-repeat!important}
.cat-band-photo .cat-head{min-height:130px;display:flex;flex-direction:column;justify-content:center}
.cat-band{background:var(--crema) url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="150" height="150"><g fill="none" stroke="%23B08A62" stroke-opacity=".16" stroke-width="3"><g transform="rotate(-25 40 40)"><ellipse cx="40" cy="40" rx="15" ry="23"/><path d="M40 19c7 13-7 29 0 42"/></g><g transform="rotate(28 110 105)"><ellipse cx="110" cy="105" rx="15" ry="23"/><path d="M110 84c7 13-7 29 0 42"/></g></g></svg>');border-bottom:1px solid var(--line)}
.hero-beans{position:absolute;right:6%;top:50%;transform:translateY(-50%);z-index:1}
.oneclick{display:flex;gap:10px;margin:6px 0 8px;flex-wrap:wrap}
.oneclick input{flex:1;min-width:200px;padding:12px 14px;border:2px solid var(--line);border-radius:10px;font-family:inherit;font-size:14px}
.oneclick input:focus{outline:none;border-color:var(--orange)}
.pd-buy{flex-wrap:wrap}
/* breadcrumb */
.crumb{font-size:13px;color:var(--muted);padding:18px 0 0}
.crumb a:hover{color:var(--orange)}
.crumb span{margin:0 6px}
/* category layout */
.cat-head{padding:20px 0 8px}
.cat-head h1{font-size:30px;margin-bottom:8px}
.cat-head .lead{color:var(--muted);max-width:760px}
.catalog{display:grid;grid-template-columns:250px 1fr;gap:28px;padding:24px 0 60px;align-items:start}
.filters{position:sticky;top:90px;background:#fff;border:1px solid var(--line);border-radius:var(--radius);padding:18px}
.filters h4{font-size:13px;text-transform:uppercase;letter-spacing:.5px;color:var(--muted);margin:16px 0 10px}
.filters h4:first-child{margin-top:0}
.f-opt{display:flex;align-items:center;gap:9px;padding:5px 0;font-size:14px;cursor:pointer}
.f-opt input{width:16px;height:16px;accent-color:var(--orange)}
.f-reset{margin-top:16px;width:100%;font-size:13px;color:var(--orange);background:none;border:1px solid var(--orange);border-radius:8px;padding:8px;cursor:pointer;font-weight:600}
.toolbar{display:flex;justify-content:space-between;align-items:center;margin-bottom:18px;gap:14px;flex-wrap:wrap}
.toolbar .found{color:var(--muted);font-size:14px}
.toolbar select{padding:9px 12px;border:1px solid var(--line);border-radius:8px;font-family:inherit;font-size:14px;cursor:pointer}
.empty{padding:60px 20px;text-align:center;color:var(--muted)}
.mobile-filter-btn{display:none}
/* product page */
.pd{display:grid;grid-template-columns:1fr 1fr;gap:44px;padding:24px 0 40px;align-items:start}
.gallery-main{border:1px solid var(--line);border-radius:var(--radius);overflow:hidden;background:var(--soft);aspect-ratio:1}
.gallery-main img{width:100%;height:100%;object-fit:cover}
.thumbs{display:flex;gap:10px;margin-top:12px;flex-wrap:wrap}
.thumbs img{width:66px;height:66px;object-fit:cover;border:2px solid var(--line);border-radius:8px;cursor:pointer}
.thumbs img.active,.thumbs img:hover{border-color:var(--orange)}
.pd-info h1{font-size:26px;margin-bottom:10px}
.pd-badges{display:flex;gap:6px;margin-bottom:14px;flex-wrap:wrap}
.pd-meta{font-size:13px;color:var(--muted);margin-bottom:16px}
.pd-price{display:flex;align-items:baseline;gap:12px;margin:14px 0}
.pd-price .now{font-size:32px;font-weight:800}
.pd-price .old{font-size:18px;color:var(--muted);text-decoration:line-through}
.variants{margin:18px 0}
.variants .vlab{font-size:13px;font-weight:600;margin-bottom:8px}
.vopts{display:flex;gap:10px;flex-wrap:wrap}
.vopt{border:2px solid var(--line);border-radius:10px;padding:8px 14px;cursor:pointer;font-size:14px;text-align:center;transition:.12s}
.vopt.active{border-color:var(--orange);background:var(--orange-l)}
.vopt b{display:block;font-size:15px}
.vopt span{font-size:12px;color:var(--muted)}
.pd-buy{display:flex;gap:12px;align-items:center;margin:20px 0}
.qty{display:flex;align-items:center;border:2px solid var(--line);border-radius:10px}
.qty button{width:40px;height:44px;border:none;background:none;font-size:20px;cursor:pointer}
.qty input{width:44px;text-align:center;border:none;font-size:16px;font-family:inherit}
.pd-feats{display:flex;flex-direction:column;gap:10px;margin-top:20px;padding-top:20px;border-top:1px solid var(--line)}
.pd-feat{display:flex;gap:10px;font-size:13.5px;align-items:flex-start;color:var(--ink2)}
.pd-section{padding:30px 0;border-top:1px solid var(--line)}
.pd-section h2{font-size:20px;margin-bottom:16px}
.pd-desc{max-width:820px;color:var(--ink2)}
.pd-desc p{margin-bottom:12px}
.spec-table{width:100%;border-collapse:collapse;max-width:640px}
.spec-table td{padding:10px 14px;border-bottom:1px solid var(--line);font-size:14px}
.spec-table td:first-child{color:var(--muted);width:45%}
.spec-table td:last-child{font-weight:600}
.profile{display:flex;flex-direction:column;gap:12px;max-width:420px}
.prof-row{display:grid;grid-template-columns:110px 1fr;align-items:center;gap:14px;font-size:14px}
.prof-bar{height:8px;background:var(--soft);border-radius:4px;overflow:hidden}
.prof-bar i{display:block;height:100%;background:var(--orange)}
.brew-list{display:flex;gap:10px;flex-wrap:wrap}
.brew-item{display:flex;align-items:center;gap:8px;background:var(--soft);border-radius:10px;padding:10px 14px;font-size:13.5px;font-weight:600}
.disclaimer{background:var(--soft);border-left:3px solid var(--orange);padding:14px 18px;font-size:12.5px;color:var(--muted);border-radius:0 8px 8px 0;margin-top:16px}
.grind-note{background:var(--orange-l);border-radius:10px;padding:16px;font-size:13.5px;margin-top:8px}
.grind-note b{color:var(--orange-d)}
/* cart */
.cart-wrap{display:grid;grid-template-columns:1fr 360px;gap:32px;padding:26px 0 60px;align-items:start}
.cart-item{display:flex;gap:16px;padding:16px 0;border-bottom:1px solid var(--line);align-items:center}
.cart-item img{width:82px;height:82px;object-fit:cover;border-radius:8px;background:var(--soft)}
.cart-item .ci-t{flex:1}
.cart-item .ci-t a{font-weight:600;font-size:14.5px}
.cart-item .ci-v{font-size:12.5px;color:var(--muted);margin-top:3px}
.ci-price{font-weight:800;font-size:16px;white-space:nowrap}
.ci-remove{background:none;border:none;color:var(--muted);cursor:pointer;font-size:13px}
.ci-remove:hover{color:#c33}
.summary{background:var(--soft);border-radius:var(--radius);padding:24px;position:sticky;top:90px}
.summary h3{margin-bottom:16px}
.sum-row{display:flex;justify-content:space-between;padding:8px 0;font-size:15px}
.sum-total{display:flex;justify-content:space-between;font-size:20px;font-weight:800;border-top:1px solid var(--line);margin-top:10px;padding-top:14px}
.form-row{margin-bottom:14px}
.form-row label{display:block;font-size:13px;font-weight:600;margin-bottom:6px}
.form-row input,.form-row select,.form-row textarea{width:100%;padding:11px 14px;border:1px solid var(--line);border-radius:9px;font-family:inherit;font-size:14px}
.form-row input:focus,.form-row select:focus,.form-row textarea:focus{outline:none;border-color:var(--orange)}
.cart-empty{text-align:center;padding:60px 0}
.cart-empty svg{color:var(--line)}
/* page/content */
.page{padding:30px 0 60px;max-width:820px}
.page h1{margin-bottom:20px}
.page h2{font-size:21px;margin:26px 0 12px}
.page p{margin-bottom:14px;color:var(--ink2)}
.page ul{margin:0 0 14px 20px;color:var(--ink2)}
.page li{margin-bottom:7px}
.seo-block{background:var(--soft);border-radius:var(--radius);padding:28px;margin-top:40px}
.seo-block h2{font-size:20px;margin-bottom:14px}
.seo-block p{color:var(--ink2);margin-bottom:12px;font-size:14.5px}
.faq details{border-bottom:1px solid var(--line);padding:14px 0}
.faq summary{font-weight:700;cursor:pointer;font-size:15px}
.faq p{margin-top:10px;color:var(--muted);font-size:14px}
/* quiz */
.quiz{background:var(--espresso);color:#fff;border-radius:16px;padding:32px}
.quiz h3{color:#fff;margin-bottom:6px}
.quiz .q-sub{color:#bbb;font-size:14px;margin-bottom:20px}
.quiz-step .qz-q{font-size:17px;font-weight:700;margin-bottom:14px}
.quiz-opts{display:flex;gap:10px;flex-wrap:wrap;margin-bottom:16px}
.quiz-opts button{background:#33221a;border:2px solid #4a3628;color:#fff;padding:11px 18px;border-radius:10px;cursor:pointer;font-family:inherit;font-size:14px;font-weight:600}
.quiz-opts button:hover,.quiz-opts button.sel{border-color:var(--orange);background:#3d2a1f}
.quiz-nav{display:flex;justify-content:space-between;align-items:center;margin-top:8px}
.quiz-dots{display:flex;gap:6px}
.quiz-dots i{width:8px;height:8px;border-radius:50%;background:#4a3628}
.quiz-dots i.on{background:var(--orange)}
.cb-flex{display:flex;align-items:center;gap:28px;justify-content:space-between}
.cat-thumb{width:118px;height:118px;object-fit:cover;border-radius:14px;border:1px solid var(--line);background:#fff;box-shadow:0 12px 28px rgba(60,35,10,.14);flex-shrink:0}
.acad-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:18px}
.acad-card{background:#fff;border:1px solid var(--line);border-radius:var(--radius);padding:22px;display:flex;flex-direction:column;transition:.15s}
.acad-card:hover{border-color:var(--orange);transform:translateY(-3px);box-shadow:0 10px 30px rgba(60,35,10,.08)}
.acad-card .tag{font-size:11px;font-weight:700;letter-spacing:1.5px;color:var(--orange);margin-bottom:10px}
.acad-card h3{font-size:17px;margin-bottom:8px;line-height:1.35}
.acad-card p{color:var(--muted);font-size:13.5px;flex:1}
.acad-card .more{color:var(--orange);font-weight:700;font-size:13.5px;margin-top:14px;display:inline-flex;gap:6px;align-items:center}
.art{max-width:760px;padding:34px 0 60px}
.art h1{font-size:32px;margin-bottom:10px}
.art .art-meta{color:var(--muted);font-size:13.5px;margin-bottom:26px}
.art h2{font-size:21px;margin:30px 0 12px}
.art p{margin-bottom:14px;color:var(--ink2);font-size:15.5px;line-height:1.7}
.art ul,.art ol{margin:0 0 16px 22px;color:var(--ink2);line-height:1.7}
.art li{margin-bottom:8px}
.art .tip{background:var(--orange-l);border-left:3px solid var(--orange);border-radius:0 10px 10px 0;padding:14px 18px;margin:18px 0;font-size:14.5px}
.art .art-cta{background:var(--espresso);color:#fff;border-radius:14px;padding:24px;margin-top:34px;display:flex;align-items:center;gap:18px;flex-wrap:wrap}
.art .art-cta p{color:#d8c9b8;margin:0;flex:1;min-width:220px}
.lineup-sec{background:var(--crema)}
.lineup-sec img{border-radius:16px;border:1px solid var(--line);box-shadow:0 16px 40px rgba(60,35,10,.10)}
@media(max-width:720px){.acad-grid{grid-template-columns:1fr}.cat-thumb{display:none}.lineup-sec .wrap{grid-template-columns:1fr!important}}
.acad-card img{width:100%;height:150px;object-fit:cover;border-radius:10px;margin-bottom:14px;border:1px solid var(--line)}
.art-cover{width:100%;max-height:340px;object-fit:cover;border-radius:14px;margin:16px 0 10px}
.mood-img{width:100%;border-radius:16px;border:1px solid var(--line);display:block;box-shadow:0 16px 40px rgba(60,35,10,.10)}
/* footer */
.footer{background:var(--espresso);color:#c8bbae;padding:50px 0 0;margin-top:60px}
.ft{display:grid;grid-template-columns:2fr 1fr 1fr 1fr;gap:30px;padding-bottom:36px}
.ft-brand p{font-size:13.5px;margin-top:14px;max-width:300px}
.ft-slogan{color:var(--orange)!important;font-weight:700}
.ft-col h4{color:#fff;font-size:14px;margin-bottom:14px}
.ft-col a{display:block;font-size:13.5px;padding:5px 0}
.ft-col a:hover{color:var(--orange)}
.ft-small{font-size:12.5px;margin-top:8px}
.ft-legal{border-top:1px solid #3d2b1e;padding:18px 20px;display:flex;justify-content:space-between;gap:20px;font-size:11.5px;color:#888;flex-wrap:wrap}
.ft-disc{max-width:640px}
/* responsive */
@media(max-width:1000px){
 .nav{display:none}.burger{display:block}
 .cat-grid{grid-template-columns:repeat(2,1fr)}
 .grid{grid-template-columns:repeat(3,1fr)}
 .pd{grid-template-columns:1fr;gap:24px}
 .cart-wrap{grid-template-columns:1fr}
 .ft{grid-template-columns:1fr 1fr}
}
@media(max-width:720px){
 h1{font-size:26px}.hero h1{font-size:32px}.hero-in{padding:48px 0}
 .strip-in{grid-template-columns:1fr 1fr}
 .grid{grid-template-columns:repeat(2,1fr);gap:12px}
 .cat-grid{grid-template-columns:1fr 1fr}
 .catalog{grid-template-columns:1fr}
 .filters{display:none;position:static}
 .filters.open{display:block;margin-bottom:20px}
 .mobile-filter-btn{display:inline-flex}
 .b2b-band{padding:24px}.section{padding:40px 0}.hero-beans{display:none}
 .ft{grid-template-columns:1fr}
 .card-title{font-size:13px}
}
@media(max-width:420px){.grid{grid-template-columns:1fr 1fr;gap:10px}}
/* NPX-032/033 лендінг оренди POLTI */
.lp-hero{background:linear-gradient(120deg,var(--espresso) 0%,#3a2519 100%);color:#fff;overflow:hidden}
.lp-hero-in{display:grid;grid-template-columns:1.1fr .9fr;gap:36px;align-items:center;padding:54px 20px 58px}
.lp-hero-txt h1{font-size:38px;line-height:1.1;margin-bottom:16px}
.lp-sub{color:#e4d7c8;font-size:18px;margin-bottom:24px;max-width:520px}
.lp-sub b{color:#fff}
.lp-cta{display:flex;gap:12px;flex-wrap:wrap;margin-bottom:20px}
.lp-cta .btn-ghost{color:#fff;border-color:#6b5240}.lp-cta .btn-ghost:hover{background:#fff;color:var(--ink)}
.lp-badges{display:flex;gap:14px;flex-wrap:wrap;font-size:12.5px;color:#cbb9a8;align-items:center}
.lp-badges svg{width:15px;height:15px;vertical-align:middle;margin-right:3px}
.lp-hero-vis{display:flex;flex-direction:column;align-items:center;gap:16px}
.lp-offer-badge{width:200px;height:200px;border-radius:50%;background:radial-gradient(circle at 50% 40%,var(--orange),var(--orange-d));
 display:flex;flex-direction:column;align-items:center;justify-content:center;color:#fff;box-shadow:0 20px 50px rgba(238,122,14,.35);text-align:center}
.lp-0{font-size:56px;font-weight:800;line-height:.9;display:flex;flex-direction:column}
.lp-0 small{font-size:15px;font-weight:600;margin-top:4px}
.lp-cond{font-size:13px;font-weight:600;margin-top:8px;opacity:.95;max-width:150px}
.lp-photo{width:100%;max-width:340px;border-radius:16px;display:block;box-shadow:0 18px 44px rgba(0,0,0,.28)}
.lp-photo-ph{width:100%;max-width:280px;aspect-ratio:4/3;border:2px dashed rgba(255,255,255,.3);border-radius:14px;
 display:flex;align-items:center;justify-content:center;text-align:center;color:#b09a86;font-size:13px;padding:14px;background:rgba(255,255,255,.04)}
.lp-hero-vis .lp-offer-badge{width:150px;height:150px}
.lp-hero-vis .lp-0{font-size:42px}
.offer-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:18px}
.offer-tile{background:#fff;border:1px solid var(--line);border-radius:14px;padding:26px 22px;text-align:center}
.offer-tile.offer-hi{border-color:var(--orange);box-shadow:0 12px 34px rgba(238,122,14,.14)}
.offer-big{font-size:34px;font-weight:800;color:var(--orange);margin-bottom:8px}
.offer-big small{font-size:16px;color:var(--muted);font-weight:600}
.offer-tile p{color:var(--ink2);font-size:14.5px}
.offer-ic{margin-bottom:8px}.offer-ic svg{width:34px;height:34px}
.steps{display:grid;grid-template-columns:repeat(4,1fr);gap:18px}
.step{background:#fff;border:1px solid var(--line);border-radius:14px;padding:22px;position:relative}
.step-n{display:flex;width:38px;height:38px;border-radius:50%;background:var(--orange);color:#fff;font-weight:800;align-items:center;justify-content:center;margin-bottom:12px}
.step h3{font-size:16px;margin-bottom:6px}.step p{color:var(--muted);font-size:13.5px}
.calc{background:var(--espresso);color:#fff;border-radius:16px;padding:30px;max-width:640px;margin:0 auto;text-align:center}
.calc label{display:block;font-weight:700;margin-bottom:16px;font-size:16px}
.calc input[type=range]{width:100%;accent-color:var(--orange);margin-bottom:16px}
.calc-out{font-size:15px;color:#d8c9b8;margin-bottom:8px}.calc-out #rcChalds,.calc-out #rcCupsV{color:#fff;font-weight:700}
.rc-status{display:inline-block;font-size:20px;font-weight:800;padding:8px 20px;border-radius:10px;margin-top:6px}
.rc-free{background:rgba(63,138,63,.25);color:#8fe08f}.rc-paid{background:rgba(238,122,14,.2);color:var(--orange)}
.calc-note{color:#b7a695;font-size:13px;margin-top:16px}
.spec-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:12px;max-width:820px}
.spec-cell{background:#fff;border:1px solid var(--line);border-radius:10px;padding:12px 16px;display:flex;flex-direction:column}
.spec-cell span{color:var(--muted);font-size:12.5px}.spec-cell b{font-size:14.5px}
.seg-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:12px}
.seg{background:#fff;border:1px solid var(--line);border-radius:10px;padding:16px;text-align:center;font-weight:600;font-size:14.5px}
.lp-form-h{text-align:center;color:#fff;margin-bottom:22px}.lp-form-h h2{color:#fff}.lp-form-h p{color:#cbb9a8;margin-top:8px}
.lp-form-h+form,section .rentalForm{background:#fff;border-radius:14px;padding:24px}
.lp-sticky{display:none}
@media(max-width:960px){.lp-hero-in{grid-template-columns:1fr;text-align:center}.lp-hero-txt h1{font-size:30px}
 .lp-cta,.lp-badges{justify-content:center}.lp-sub{margin-left:auto;margin-right:auto}
 .offer-grid{grid-template-columns:1fr}.steps{grid-template-columns:1fr 1fr}.spec-grid{grid-template-columns:1fr}.seg-grid{grid-template-columns:1fr 1fr}}
@media(max-width:720px){.steps{grid-template-columns:1fr}
 .lp-sticky{position:fixed;left:0;right:0;bottom:0;z-index:60;background:#fff;border-top:1px solid var(--line);
  box-shadow:0 -6px 20px rgba(0,0,0,.1);padding:10px 14px calc(10px + env(safe-area-inset-bottom));
  display:flex;align-items:center;justify-content:space-between;gap:12px}
 .lp-sticky span{font-size:13px}.lp-sticky .btn{padding:11px 16px;min-height:44px}
 body.lp-page{padding-bottom:74px}}
/* NPX-034 хаб-лендинг оренди: преміальні блоки */
.lp-eyebrow{font-size:12px;font-weight:700;letter-spacing:2.5px;color:var(--orange);margin-bottom:14px}
.opt-grid{display:grid;grid-template-columns:1fr 1fr;gap:22px;align-items:start}
.opt-card{background:#fff;border:1px solid var(--line);border-radius:18px;padding:30px 28px;position:relative}
.opt-card.opt-hi{border:2px solid var(--orange);box-shadow:0 18px 44px rgba(238,122,14,.14)}
.opt-tag{display:inline-block;font-size:11.5px;font-weight:700;letter-spacing:1px;color:var(--muted);margin-bottom:14px;text-transform:uppercase}
.opt-hi .opt-tag{color:var(--orange)}
.opt-price{font-size:44px;font-weight:800;color:var(--ink);line-height:1;margin-bottom:12px}
.opt-price small{font-size:16px;font-weight:600;color:var(--muted);margin-left:4px}
.opt-hi .opt-price{color:var(--orange)}
.opt-lead{color:var(--ink2);font-size:15.5px;margin-bottom:18px}
.opt-flow{display:flex;flex-direction:column;gap:8px}
.flow-step{display:flex;align-items:center;gap:10px;background:var(--soft);border-radius:12px;padding:13px 16px;font-size:14.5px;font-weight:600}
.flow-step svg{flex-shrink:0;width:20px;height:20px}
.flow-final{background:var(--orange-l);color:var(--orange-d)}
.flow-arrow{text-align:center;color:var(--orange);font-size:18px;line-height:.6;font-weight:800}
.opt-list{list-style:none;display:flex;flex-direction:column;gap:11px}
.opt-list li{display:flex;align-items:flex-start;gap:10px;font-size:14.5px;color:var(--ink2)}
.opt-list svg,.ese-why svg,.incl svg{flex-shrink:0;width:19px;height:19px}
.ese-explain{display:grid;grid-template-columns:1.15fr .85fr;gap:40px;align-items:center}
.ese-txt h2{margin-bottom:14px}.ese-txt p{color:var(--ink2);margin-bottom:14px;font-size:15.5px;line-height:1.7}
.ese-txt .btn{margin-top:6px}
.ese-why{background:#fff;border:1px solid var(--line);border-radius:16px;padding:26px 28px}
.ese-why h3{font-size:18px;margin-bottom:16px}
.ese-why ul{list-style:none;display:grid;grid-template-columns:1fr 1fr;gap:12px}
.ese-why li{display:flex;align-items:center;gap:9px;font-size:14px;font-weight:600}
.chald-grid{display:grid;grid-template-columns:repeat(5,1fr);gap:16px}
.chald-card{background:#fff;border:1px solid var(--line);border-radius:14px;overflow:hidden;transition:.15s;display:flex;flex-direction:column}
.chald-card:hover{border-color:var(--orange);transform:translateY(-3px);box-shadow:0 12px 30px rgba(60,35,10,.10)}
.chald-img{aspect-ratio:1;background:var(--soft)}.chald-img img{width:100%;height:100%;object-fit:cover}
.chald-b{padding:13px 14px;display:flex;flex-direction:column;gap:3px}
.chald-b b{font-size:14px;line-height:1.3}
.chald-q{font-size:12.5px;color:var(--muted)}
.chald-pc{font-size:12.5px;font-weight:700;color:var(--orange)}
.cmp{display:grid;grid-template-columns:.9fr 1.1fr;gap:36px;align-items:center}
.cmp-photo img{width:100%;border-radius:18px;border:1px solid var(--line);box-shadow:0 16px 40px rgba(60,35,10,.10)}
.cmp-colors{display:flex;align-items:center;gap:10px;flex-wrap:wrap;font-weight:600;font-size:14px;margin-bottom:18px}
.clr{width:20px;height:20px;border-radius:50%;display:inline-block;border:1px solid var(--line);vertical-align:middle}
.clr-w{background:#fff}.clr-b{background:#26211d}
.cmp-note{color:var(--muted);font-size:13px;margin-top:14px}
.incl-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}
.incl{background:#fff;border:1px solid var(--line);border-radius:14px;padding:20px;display:flex;flex-direction:column;gap:4px}
.incl svg{margin-bottom:6px}.incl b{font-size:15px}.incl span{font-size:13px;color:var(--muted)}
.clr-pick{display:flex;gap:18px;padding-top:4px}
.clr-pick label{display:flex;align-items:center;gap:7px;font-weight:600;font-size:14px;cursor:pointer}
.clr-pick input{width:17px;height:17px;accent-color:var(--orange)}
@media(max-width:960px){.opt-grid{grid-template-columns:1fr}.ese-explain{grid-template-columns:1fr;gap:24px}
 .ese-why ul{grid-template-columns:1fr 1fr}.chald-grid{grid-template-columns:repeat(2,1fr)}
 .cmp{grid-template-columns:1fr;gap:22px}.incl-grid{grid-template-columns:1fr}}
@media(max-width:520px){.chald-grid{grid-template-columns:1fr 1fr}.ese-why ul{grid-template-columns:1fr}.opt-price{font-size:38px}}
/* sticky mobile CTA (NPX-028) */
.sticky-cta{display:none}
@media(max-width:720px){
 .sticky-cta{position:fixed;left:0;right:0;bottom:0;z-index:60;background:#fff;border-top:1px solid var(--line);
  box-shadow:0 -6px 20px rgba(0,0,0,.08);padding:10px 16px calc(10px + env(safe-area-inset-bottom));
  display:flex;align-items:center;gap:14px;transform:translateY(110%);transition:transform .2s}
 .sticky-cta.show{transform:translateY(0)}
 .sticky-cta .sc-price{font-size:18px;font-weight:800;white-space:nowrap}
 .sticky-cta .btn{flex:1;min-height:44px}
 body.has-sticky-cta{padding-bottom:76px}
}

/* ==================== ПРЕМІУМ-ЛЕНДИНГ ОРЕНДИ (rental hub v2) ==================== */
/* video facade */
.rh-video{position:relative;max-width:900px;margin:0 auto;aspect-ratio:16/9;border-radius:20px;overflow:hidden;cursor:pointer;box-shadow:0 30px 70px -30px rgba(0,0,0,.5);background:#000}
.rh-video img{width:100%;height:100%;object-fit:cover;display:block;transition:transform .4s,opacity .3s}
.rh-video:hover img{transform:scale(1.04);opacity:.82}
.rh-video iframe{width:100%;height:100%;border:0;display:block}
.rh-play{position:absolute;inset:0;margin:auto;width:88px;height:62px;border:0;background:none;cursor:pointer;padding:0}
.rh-play svg{width:100%;height:100%;filter:drop-shadow(0 6px 16px rgba(0,0,0,.45));transition:transform .2s}
.rh-video:hover .rh-play svg{transform:scale(1.12)}
/* photo gallery */
.rh-gallery{display:grid;grid-template-columns:repeat(5,1fr);gap:14px;margin-top:34px}
.rh-gallery a{display:block;border-radius:16px;overflow:hidden;border:1px solid var(--line);background:var(--soft);aspect-ratio:3/4;box-shadow:0 10px 26px rgba(60,35,10,.08);transition:transform .3s,box-shadow .3s}
.rh-gallery a:hover{transform:translateY(-4px);box-shadow:0 20px 42px rgba(60,35,10,.15)}
.rh-gallery img{width:100%;height:100%;object-fit:cover;display:block}
@media(max-width:820px){.rh-gallery{grid-template-columns:repeat(3,1fr)}}
@media(max-width:480px){.rh-gallery{grid-template-columns:1fr 1fr}}

.reveal{opacity:0;transform:translateY(26px);transition:opacity .7s cubic-bezier(.16,1,.3,1),transform .7s cubic-bezier(.16,1,.3,1)}
.reveal.in{opacity:1;transform:none}
@media(prefers-reduced-motion:reduce){.reveal{opacity:1;transform:none;transition:none}}
.rh-wrap{max-width:var(--wrap);margin:0 auto;padding:0 20px}
.rh-sec{padding:76px 0}
.rh-sec.tight{padding-top:0}
.rh-head{text-align:center;max-width:720px;margin:0 auto 44px}
.rh-kicker{font-size:12px;letter-spacing:2.5px;font-weight:700;color:var(--orange);margin-bottom:12px}
.rh-head h2{font-size:clamp(26px,3.4vw,40px);line-height:1.12;letter-spacing:-.5px;margin:0 0 12px}
.rh-head .rh-hsub{color:var(--muted);font-size:16.5px;line-height:1.55}

/* HERO */
.rh-hero{position:relative;background:radial-gradient(130% 130% at 88% -10%,#3c2517 0%,var(--espresso) 58%);color:#fff;overflow:hidden}
.rh-hero::before{content:"";position:absolute;top:-25%;right:-8%;width:560px;height:560px;background:radial-gradient(circle,rgba(238,122,14,.34),transparent 62%);pointer-events:none}
.rh-hero-in{position:relative;display:grid;grid-template-columns:1.05fr .95fr;gap:48px;align-items:center;padding:66px 20px 78px;max-width:var(--wrap);margin:0 auto}
.rh-eyebrow{display:inline-flex;align-items:center;gap:8px;font-size:12px;letter-spacing:2.5px;font-weight:700;color:#ffd9ad;background:rgba(255,255,255,.08);border:1px solid rgba(255,255,255,.15);padding:7px 15px;border-radius:999px;margin-bottom:22px}
.rh-hero h1{font-size:clamp(33px,5vw,58px);line-height:1.04;letter-spacing:-1px;margin:0 0 18px;font-weight:800}
.rh-hero h1 .hl{color:var(--orange)}
.rh-hero .rh-lead{font-size:clamp(16px,1.55vw,19px);line-height:1.55;color:#e8ddd2;max-width:540px;margin-bottom:22px}
.rh-fire{display:flex;align-items:center;gap:12px;background:linear-gradient(90deg,rgba(238,122,14,.20),rgba(238,122,14,0));border-left:3px solid var(--orange);padding:13px 17px;border-radius:0 12px 12px 0;margin-bottom:28px;font-size:15px;line-height:1.4}
.rh-fire b{color:#fff}
.rh-herocta{display:flex;gap:14px;flex-wrap:wrap;margin-bottom:26px}
.rh-trust{display:flex;gap:22px;flex-wrap:wrap;font-size:13.5px;color:#cdbfb2}
.rh-trust span{display:inline-flex;align-items:center;gap:7px}
.rh-trust svg{width:16px;height:16px;color:var(--orange)}
.rh-hero-vis{position:relative;display:flex;justify-content:center}
.rh-frame{position:relative;background:linear-gradient(158deg,#fbf6ee,#eee1cf);border-radius:30px;padding:20px;box-shadow:0 44px 90px -34px rgba(0,0,0,.62);width:100%;max-width:430px}
.rh-frame img{width:100%;height:auto;border-radius:18px;display:block}
.rh-chip{position:absolute;left:-16px;bottom:30px;background:var(--orange);color:#fff;border-radius:20px;padding:15px 22px;box-shadow:0 18px 38px rgba(238,122,14,.5);text-align:center;transform:rotate(-4deg)}
.rh-chip .p0{font-size:36px;font-weight:800;line-height:.95}
.rh-chip .pc{font-size:12px;opacity:.95;display:block;margin-top:3px}

/* TARIFFS */
.rh-tiers{display:grid;grid-template-columns:1fr 1fr;gap:24px;align-items:stretch}
.rh-tier{position:relative;background:#fff;border:1px solid var(--line);border-radius:22px;padding:36px 30px;display:flex;flex-direction:column;transition:transform .3s,box-shadow .3s}
.rh-tier:hover{transform:translateY(-4px);box-shadow:0 26px 54px rgba(60,35,10,.13)}
.rh-tier.best{border:2px solid transparent;background:linear-gradient(#fff,#fff) padding-box,linear-gradient(135deg,var(--orange),#f6ab52) border-box;box-shadow:0 26px 62px rgba(238,122,14,.17)}
.rh-ribbon{position:absolute;top:-14px;left:28px;background:var(--orange);color:#fff;font-size:11.5px;font-weight:700;letter-spacing:1px;padding:6px 15px;border-radius:999px;box-shadow:0 6px 16px rgba(238,122,14,.4)}
.rh-tier .t-name{font-size:12px;letter-spacing:1.5px;font-weight:700;color:var(--muted);margin-bottom:16px}
.rh-tier .t-price{font-size:clamp(40px,5vw,54px);font-weight:800;color:var(--ink);line-height:.95;letter-spacing:-1.5px}
.rh-tier .t-price small{font-size:17px;font-weight:600;color:var(--muted);letter-spacing:0}
.rh-tier .t-lead{color:var(--ink2);margin:14px 0 22px;font-size:15px;line-height:1.5}
.rh-tier .t-lead b{color:var(--orange)}
.rh-flow{display:flex;flex-direction:column;gap:9px;margin-top:auto}
.rh-flow .fl{display:flex;align-items:center;gap:11px;background:var(--soft);border-radius:12px;padding:13px 15px;font-size:14px;font-weight:600}
.rh-flow .fl svg{width:18px;height:18px;color:var(--green);flex-shrink:0}
.rh-flow .fl.fin{background:var(--orange-l)}
.rh-flow .fl.fin svg{color:var(--orange-d)}
.rh-tlist{list-style:none;padding:0;margin:2px 0 auto;display:flex;flex-direction:column;gap:12px}
.rh-tlist li{display:flex;gap:10px;font-size:14.5px;color:var(--ink2);line-height:1.4}
.rh-tlist svg{width:18px;height:18px;color:var(--orange);flex-shrink:0;margin-top:1px}
.rh-tier .btn{margin-top:24px;width:100%}

/* RENT vs BUY + CALC */
.rh-vs{display:grid;grid-template-columns:1fr 1fr;gap:22px}
.vs-col{border-radius:18px;padding:30px}
.vs-rent{background:linear-gradient(160deg,#f0f7ef,#e2f0e1);border:1px solid #cfe6cd}
.vs-buy{background:var(--soft);border:1px solid var(--line)}
.vs-col h3{font-size:19px;margin:0 0 18px;display:flex;align-items:center;gap:10px}
.vs-col ul{list-style:none;padding:0;margin:0;display:flex;flex-direction:column;gap:13px}
.vs-col li{display:flex;gap:11px;font-size:14.5px;line-height:1.45;color:var(--ink2)}
.vs-rent li svg{color:var(--green);width:19px;height:19px;flex-shrink:0;margin-top:1px}
.vs-buy li::before{content:"✕";color:#c98b6a;font-weight:700;flex-shrink:0}
.rh-calc{background:radial-gradient(120% 130% at 100% 0%,#3a2417,var(--espresso));color:#fff;border-radius:24px;padding:36px;display:grid;grid-template-columns:1fr 1fr;gap:32px;align-items:center;margin-top:26px}
.rh-calc h3{font-size:23px;margin:0 0 6px}
.rh-calc .c-sub{color:#c9bab0;font-size:14px;margin-bottom:22px;line-height:1.5}
.rh-calc label{display:block;font-size:13px;color:#c9bab0;margin-bottom:10px}
.rh-calc input[type=range]{width:100%;height:6px;accent-color:var(--orange);cursor:pointer}
.c-cups{font-size:32px;font-weight:800;color:var(--orange);margin-bottom:2px}
.c-cups small{font-size:15px;color:#c9bab0;font-weight:600}
.rh-calc-out{background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.13);border-radius:18px;padding:24px}
.co-row{display:flex;justify-content:space-between;align-items:baseline;padding:11px 0;border-bottom:1px solid rgba(255,255,255,.1);font-size:14px;color:#e6dcd2}
.co-row:last-child{border:0;padding-bottom:0}
.co-row b{font-size:21px;color:#fff}
.co-free{color:#7ee08a!important}
.co-badge{display:inline-block;margin-top:14px;padding:8px 14px;border-radius:999px;font-size:13px;font-weight:700}
.co-badge.free{background:rgba(126,224,138,.16);color:#7ee08a}
.co-badge.paid{background:rgba(238,122,14,.18);color:#ffb968}

/* BIG-ICON FEATURES */
.rh-feat{display:grid;grid-template-columns:repeat(4,1fr);gap:18px}
.ft{background:#fff;border:1px solid var(--line);border-radius:18px;padding:28px 22px;text-align:center;transition:transform .3s,box-shadow .3s}
.ft:hover{transform:translateY(-5px);box-shadow:0 22px 46px rgba(60,35,10,.1)}
.ft-ic{width:58px;height:58px;margin:0 auto 15px;border-radius:16px;background:var(--orange-l);display:flex;align-items:center;justify-content:center;color:var(--orange-d)}
.ft-ic svg{width:28px;height:28px}
.ft b{display:block;font-size:15px;margin-bottom:5px}
.ft span{font-size:13px;color:var(--muted);line-height:1.45}

/* WHY / TRUST */
.rh-why{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}
.rh-w{display:flex;gap:14px;background:#fff;border:1px solid var(--line);border-radius:14px;padding:22px;transition:border-color .2s,transform .2s}
.rh-w:hover{border-color:var(--orange);transform:translateY(-2px)}
.rh-w-ic{width:44px;height:44px;border-radius:12px;background:var(--orange-l);display:flex;align-items:center;justify-content:center;color:var(--orange-d);flex-shrink:0}
.rh-w-ic svg{width:22px;height:22px}
.rh-w b{font-size:15px;display:block;margin-bottom:3px}
.rh-w span{font-size:13px;color:var(--muted);line-height:1.4}

/* SEGMENTS */
.rh-seg{display:grid;grid-template-columns:repeat(4,1fr);gap:14px}
.sg{display:flex;align-items:center;gap:12px;background:#fff;border:1px solid var(--line);border-radius:14px;padding:17px 18px;font-weight:600;font-size:14.5px;transition:border-color .2s,transform .2s}
.sg:hover{border-color:var(--orange);transform:translateY(-2px)}
.sg svg{width:22px;height:22px;color:var(--orange);flex-shrink:0}

/* FINAL CTA + contacts */
.rh-final{background:radial-gradient(120% 140% at 0% 0%,#3a2417,var(--espresso));color:#fff}
.rh-final-in{display:grid;grid-template-columns:1fr 1fr;gap:44px;align-items:start;max-width:var(--wrap);margin:0 auto;padding:70px 20px}
.rh-final h2{font-size:clamp(26px,3.2vw,38px);line-height:1.1;margin:0 0 14px}
.rh-final p{color:#d9ccc0;font-size:16px;line-height:1.6;margin-bottom:24px}
.rh-contacts{display:flex;flex-direction:column;gap:12px;margin-top:8px}
.rh-ct{display:inline-flex;align-items:center;gap:12px;color:#fff;text-decoration:none;font-weight:600;font-size:15px;background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.13);border-radius:12px;padding:13px 16px;transition:background .2s,border-color .2s}
.rh-ct:hover{background:rgba(255,255,255,.11);border-color:rgba(255,255,255,.25)}
.rh-ct svg{width:20px;height:20px;flex-shrink:0}
.rh-msgs{display:flex;gap:10px;flex-wrap:wrap;margin-top:4px}
.rh-msg{display:inline-flex;align-items:center;gap:8px;padding:11px 16px;border-radius:12px;font-weight:700;font-size:14px;color:#fff;text-decoration:none;transition:transform .2s,filter .2s}
.rh-msg:hover{transform:translateY(-2px);filter:brightness(1.08)}
.rh-msg svg{width:18px;height:18px}
.rh-msg.viber{background:#7360F2}.rh-msg.tg{background:#2AABEE}.rh-msg.wa{background:#25D366}
.rh-formcard{background:#fff;border-radius:22px;padding:30px;box-shadow:0 30px 70px -30px rgba(0,0,0,.5)}
.rh-formcard h3{font-size:19px;margin:0 0 6px;color:var(--ink)}
.rh-formcard .fc-sub{color:var(--muted);font-size:13.5px;margin-bottom:18px}

@media(max-width:960px){
 .rh-hero-in{grid-template-columns:1fr;text-align:center;padding:46px 18px 56px}
 .rh-hero .rh-lead,.rh-fire{margin-left:auto;margin-right:auto}
 .rh-herocta,.rh-trust{justify-content:center}
 .rh-tiers,.rh-vs,.rh-calc,.rh-why,.rh-final-in{grid-template-columns:1fr}
 .rh-feat,.rh-seg{grid-template-columns:1fr 1fr}
 .rh-chip{left:50%;transform:translateX(-50%) rotate(-4deg)}
 .rh-sec{padding:56px 0}
}
@media(max-width:480px){
 .rh-feat{grid-template-columns:1fr 1fr}
 .rh-calc,.rh-formcard{padding:22px}
 .rh-frame{max-width:340px}
}
'''

def write_css():
    open(os.path.join(SITE,'assets','style.css'),'w',encoding='utf-8').write(CSS)

JS = r'''
const CART_KEY='npromax_cart';
function getCart(){try{return JSON.parse(localStorage.getItem(CART_KEY))||[]}catch(e){return[]}}
function setCart(c){localStorage.setItem(CART_KEY,JSON.stringify(c));updateBadge();}
function updateBadge(){var n=getCart().reduce((s,i)=>s+i.qty,0);document.querySelectorAll('#cartBadge').forEach(b=>{b.textContent=n;b.style.display=n?'flex':'none';});}
function addToCart(p,qty){qty=qty||1;var c=getCart();var k=p.slug+'|'+(p.variant||'');var e=c.find(i=>i.key===k);
 if(e)e.qty+=qty;else c.push({key:k,slug:p.slug,sku:p.sku||'',title:p.title,price:p.price,img:p.img,variant:p.variant||'',qty:qty});
 setCart(c);toast('Додано в кошик: '+p.title);}
function toast(msg){var t=document.createElement('div');t.textContent=msg;
 t.style.cssText='position:fixed;bottom:24px;left:50%;transform:translateX(-50%);background:#1A1A1A;color:#fff;padding:13px 22px;border-radius:10px;z-index:999;font-size:14px;font-weight:600;box-shadow:0 8px 30px rgba(0,0,0,.25)';
 document.body.appendChild(t);setTimeout(()=>{t.style.opacity='0';t.style.transition='.3s';setTimeout(()=>t.remove(),300)},1800);}
function toggleMenu(){document.getElementById('drawer').classList.toggle('open');}
function setSearch(open){var s=document.getElementById('searchbar');if(!s)return;
 s.classList.toggle('open',open);
 var b=document.getElementById('searchToggle');if(b)b.setAttribute('aria-expanded',open?'true':'false');
 if(open)document.getElementById('siteSearch').focus();}
function toggleSearch(){var s=document.getElementById('searchbar');setSearch(!s.classList.contains('open'));}
function closeSearch(){setSearch(false);}
// NPX-025: Esc і клік-поза закривають пошук, фокус повертається на кнопку
function initSearchUx(){
 document.addEventListener('keydown',function(e){
  if(e.key==='Escape'){var s=document.getElementById('searchbar');
   if(s&&s.classList.contains('open')){closeSearch();var b=document.getElementById('searchToggle');if(b)b.focus();}}});
 document.addEventListener('click',function(e){
  var s=document.getElementById('searchbar');if(!s||!s.classList.contains('open'))return;
  if(s.contains(e.target)||e.target.closest('#searchToggle'))return;
  closeSearch();});}
// ---------- NPX-011: пошук v2 ----------
var SEARCH_INDEX=[];
// Згортання UA/RU-варіантів: «кенія» і «кения» → один рядок. Латиниця не зачіпається.
function sNorm(s){return (s||'').toLowerCase()
 .replace(/[’'`ʼ]/g,'')
 .replace(/[іїийы]/g,'и').replace(/[еєэё]/g,'е').replace(/ґ/g,'г').replace(/[ьъ]/g,'')
 .replace(/\s+/g,' ').trim();}
// Відстань редагування ≤1 (заміна/вставка/видалення) — без повного DP.
function ed1(a,b){var la=a.length,lb=b.length;if(Math.abs(la-lb)>1)return false;
 var i=0,j=0,d=0;
 while(i<la&&j<lb){
  if(a.charAt(i)===b.charAt(j)){i++;j++;continue;}
  if(++d>1)return false;
  if(la>lb)i++;else if(lb>la)j++;else{i++;j++;}
 }
 if(i<la||j<lb)d++;
 return d<=1;}
function sPrep(){SEARCH_INDEX.forEach(function(p){
 if(p._h)return;
 p._h=sNorm(p.t+' '+(p.tags||[]).join(' ')+' '+(p.tr||''));
 p._w=p._h.split(/[\s,()«»"\/]+/).filter(Boolean);
 p._sk=(p.skus&&p.skus.length?p.skus:[p.sku||'']).map(function(x){return (x||'').toLowerCase();});
});}
// Повертає масив збігів. Порядок: точний SKU → назва → теги.
function searchItems(q){
 sPrep();
 var raw=(q||'').trim().toLowerCase();
 if(!raw)return[];
 // 1) точний артикул: «04-0642» має дати 1 результат, а не префіксні 04-0642-2
 var exact=SEARCH_INDEX.filter(function(p){return p._sk.indexOf(raw)>=0;});
 if(exact.length)return exact;
 var nq=sNorm(raw);
 var toks=nq.split(' ').filter(Boolean);
 var hits=SEARCH_INDEX.filter(function(p){
  return toks.every(function(tk){
   if(p._h.indexOf(tk)>=0)return true;
   if(tk.length>=5)return p._w.some(function(w){return ed1(w,tk);});
   return false;
  });
 });
 if(!hits.length){ // 2) відкат: префікс артикула
  hits=SEARCH_INDEX.filter(function(p){return p._sk.some(function(s){return s.indexOf(raw)===0;});});
 }
 var tn=function(p){return sNorm(p.t);};
 return hits.sort(function(a,b){
  var aa=tn(a).indexOf(nq),bb=tn(b).indexOf(nq);
  if(aa<0)aa=999;if(bb<0)bb=999;
  return aa-bb;});
}
function siteSearch(q){var r=document.getElementById('searchResults');
 if(!q||!q.trim()){r.innerHTML='';return;}
 var hits=searchItems(q);
 if(!hits.length){
  r.innerHTML='<div style="padding:12px;color:var(--muted)">Нічого не знайдено за запитом «'+esc(q)+'».'
   +'<div style="margin-top:8px">Спробуйте: <a href="kava-v-zernakh.html" style="color:var(--orange)">кава в зернах</a> · '
   +'<a href="kapsuly-nespresso.html" style="color:var(--orange)">капсули</a> · '
   +'<a href="arabika-monosorty.html" style="color:var(--orange)">арабіка</a> · '
   +'<a href="catalog.html" style="color:var(--orange)">весь каталог</a></div></div>';
  return;}
 var top=hits.slice(0,6);
 var html=top.map(function(p){return '<a href="'+(p.u||('p-'+p.s+'.html'))+'"><img src="'+p.i+'" alt=""><span>'+esc(p.t)+'</span></a>';}).join('');
 if(hits.length>top.length)
  html+='<a href="catalog.html?q='+encodeURIComponent(q.trim())+'" style="font-weight:700;color:var(--orange);justify-content:center">Показати всі результати ('+hits.length+')</a>';
 r.innerHTML=html;}
function esc(s){return (s||'').replace(/[&<>"']/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c];});}
function searchKey(e){if(e.key==='Enter'){var v=e.target.value.trim();if(v)location.href='catalog.html?q='+encodeURIComponent(v);}}
// ?q= на сторінці каталогу
var SEARCH_SLUGS=null;
function initCatalogQuery(){
 var g=document.getElementById('prodGrid');if(!g)return;
 var q=new URLSearchParams(location.search).get('q');
 if(!q||!q.trim())return;
 var all=searchItems(q);
 var hits=all.filter(function(p){return !p.svc;});      // товари — є картки в сітці
 var svcs=all.filter(function(p){return p.svc;});        // послуги — окремі сторінки
 SEARCH_SLUGS={};hits.forEach(function(p){SEARCH_SLUGS[p.s]=1;});
 var bar=document.getElementById('searchBar');
 if(bar){bar.style.display='block';
  var h='Результати пошуку: <b>'+esc(q)+'</b> — знайдено '+hits.length
   +' <a href="catalog.html" style="color:var(--orange);margin-left:10px">× скинути</a>';
  if(svcs.length)h+='<div style="margin-top:8px">Також послуга: '
   +svcs.map(function(p){return '<a href="'+p.u+'" style="color:var(--orange);font-weight:700">'+esc(p.t)+'</a>';}).join(', ')+'</div>';
  bar.innerHTML=h;}
 var si=document.getElementById('siteSearch');if(si)si.value=q;
 applyFilters();}
// category filters
function applyFilters(){
 var checks=[...document.querySelectorAll('.f-opt input:checked')];
 var groups={};checks.forEach(c=>{(groups[c.dataset.g]=groups[c.dataset.g]||[]).push(c.value)});
 var mnEl=document.getElementById('fMin'),mxEl=document.getElementById('fMax');
 var mn=mnEl&&mnEl.value!==''?parseFloat(mnEl.value):0;
 var mx=mxEl&&mxEl.value!==''?parseFloat(mxEl.value):Infinity;
 var cards=[...document.querySelectorAll('#prodGrid .card')];var shown=0;
 cards.forEach(card=>{
  var ok=true;
  var pr=+card.dataset.price;
  if(pr<mn||pr>mx)ok=false;
  if(ok&&SEARCH_SLUGS&&!SEARCH_SLUGS[card.dataset.slug])ok=false;
  if(ok)for(var g in groups){
   var v=groups[g];var cv;
   if(g==='comp')cv=card.dataset.comp; else if(g==='country')cv=card.dataset.country;
   else if(g==='type')cv=card.dataset.type; else if(g==='avail')cv=card.dataset.avail;
   else if(g==='kind'){var ar=card.dataset.aroma==='1';var km=v.some(x=>(x==='aroma'&&ar)||(x==='natural'&&!ar));if(!km){ok=false;break;}continue;}
   else if(g==='prop'){var m=v.some(x=>(x==='aroma'&&card.dataset.aroma==='1')||(x==='decaf'&&card.dataset.decaf==='1'));if(!m){ok=false;break;}continue;}
   if(!v.includes(cv)){ok=false;break;}
  }
  card.style.display=ok?'':'none';if(ok)shown++;
 });
 var f=document.getElementById('foundCount');if(f)f.textContent=shown+' товар'+plural(shown);
 var e=document.getElementById('emptyMsg');
 if(e){e.style.display=shown?'none':'block';
  if(!shown)e.innerHTML=SEARCH_SLUGS?EMPTY_SEARCH_HTML:'Нічого не знайдено. Спробуйте змінити фільтри.';}
 updateDivider();
}
// AC-011: нуль результатів пошуку — не глухий кут, а підказка з категоріями
var EMPTY_SEARCH_HTML='<b>За вашим запитом нічого не знайдено.</b>'
 +'<div style="margin-top:10px">Перевірте написання або оберіть категорію:</div>'
 +'<div style="display:flex;gap:8px;flex-wrap:wrap;justify-content:center;margin-top:12px">'
 +'<a class="chip" href="kava-v-zernakh.html">Кава в зернах</a>'
 +'<a class="chip" href="svizhomelena-kava.html">Свіжомелена</a>'
 +'<a class="chip" href="kapsuly-nespresso.html">Капсули Nespresso</a>'
 +'<a class="chip" href="monodozy-ese.html">E.S.E. монодози</a>'
 +'<a class="chip" href="arabika-monosorty.html">Арабіка</a>'
 +'<a class="chip" href="catalog.html">Весь каталог</a></div>';
function plural(n){n=n%100;if(n>=11&&n<=14)return'ів';n=n%10;if(n===1)return'';if(n>=2&&n<=4)return'и';return'ів';}
function resetFilters(){document.querySelectorAll('.f-opt input').forEach(c=>c.checked=false);var a=document.getElementById('fMin'),b=document.getElementById('fMax');if(a)a.value='';if(b)b.value='';applyFilters();}
function sortGrid(v){var g=document.getElementById('prodGrid');if(!g)return;
 var div=document.getElementById('aromaDivider');
 var cards=[...g.querySelectorAll('.card')];
 cards.sort((a,b)=>{
  var ga=a.dataset.aroma==='1'?1:0,gb=b.dataset.aroma==='1'?1:0;
  if(ga!==gb)return ga-gb;
  var pa=+a.dataset.price,pb=+b.dataset.price;
  if(v==='price-asc')return pa-pb;if(v==='price-desc')return pb-pa;
  if(v==='name')return a.dataset.name.localeCompare(b.dataset.name);
  return (+a.dataset.idx||0)-(+b.dataset.idx||0);});
 cards.forEach(c=>g.appendChild(c));
 if(div){var fa=cards.find(c=>c.dataset.aroma==='1');if(fa)g.insertBefore(div,fa);}
 updateDivider();}
function updateDivider(){var div=document.getElementById('aromaDivider');if(!div)return;
 var cards=[...document.querySelectorAll('#prodGrid .card')];
 var vis=c=>c.style.display!=='none';
 var a=cards.some(c=>c.dataset.aroma==='1'&&vis(c)),n=cards.some(c=>c.dataset.aroma!=='1'&&vis(c));
 div.style.display=(a&&n)?'':'none';}
function toggleFilters(){document.querySelector('.filters').classList.toggle('open');}
// product variant
function selVariant(el,price,label){document.querySelectorAll('.vopt').forEach(v=>v.classList.remove('active'));el.classList.add('active');
 var pt=(Math.round(price)).toLocaleString('uk-UA').replace(/,/g,' ')+' ₴';
 document.getElementById('pdPrice').textContent=pt;
 var sc=document.getElementById('scPrice');if(sc)sc.textContent=pt;
 window.__pdVariant=label;window.__pdPrice=price;}
// sticky mobile CTA (NPX-028): show after scrolling past .pd-buy
function initStickyCta(){var bar=document.getElementById('stickyCta');if(!bar)return;
 var buy=document.querySelector('.pd-buy');if(!buy)return;
 var onScroll=function(){var r=buy.getBoundingClientRect();
  var past=r.bottom<0;bar.classList.toggle('show',past);
  document.body.classList.toggle('has-sticky-cta',past);};
 window.addEventListener('scroll',onScroll,{passive:true});onScroll();}
function pdAdd(go){var q=+document.getElementById('pdQty').value||1;
 addToCart({slug:window.__pdSlug,sku:window.__pdSku,title:window.__pdTitle,price:window.__pdPrice,img:window.__pdImg,variant:window.__pdVariant},q);
 if(go)location.href='cart.html';}
function oneClickBuy(e){e.preventDefault();var f=e.target;var fd=new FormData(f);
 if(fd.get('_honey')){return;}
 var btn=f.querySelector('button[type=submit]');btn.disabled=true;btn.textContent='Відправляємо…';
 fsSend('Купити в 1 клік: '+(window.__pdTitle||''),{
  name:fd.get('name')||'',phone:fd.get('phone')||'',product:window.__pdTitle||'',sku:window.__pdSku||'',variant:window.__pdVariant||'',price:(window.__pdPrice||'')+' грн',qty:(document.getElementById('pdQty')||{}).value||1,url:location.href})
 .then(()=>{ga('generate_lead',{type:'one_click'});f.style.display='none';var ok=document.getElementById('oneClickOk');if(ok)ok.style.display='block';})
 .catch(()=>{btn.disabled=false;btn.textContent='Купити в 1 клік';toast('Не вдалося відправити. Напишіть на info@npromax.com.ua');});}
function leadCapture(e){e.preventDefault();var f=e.target;var fd=new FormData(f);
 if(fd.get('_honey')){return;}
 var btn=f.querySelector('button');btn.disabled=true;btn.textContent='Відправляємо…';
 fsSend('Заявка на консультацію (головна)',{phone:fd.get('phone')||'',name:fd.get('name')||''})
 .then(()=>{ga('generate_lead',{type:'consult'});f.innerHTML='<p style="color:#fff;font-weight:700;margin:8px 0">Дякуємо! Зателефонуємо найближчим часом ✓</p>';})
 .catch(()=>{btn.disabled=false;btn.textContent='Передзвоніть мені';toast('Не вдалося відправити');});}
function contactSend(e){e.preventDefault();var f=e.target;var fd=new FormData(f);
 if(fd.get('_honey')){return;}
 var btn=f.querySelector('button[type=submit]');btn.disabled=true;btn.textContent='Відправляємо…';
 fsSend('Повідомлення зі сторінки Контакти',{name:fd.get('name')||'',email:fd.get('email')||'',message:fd.get('message')||''})
 .then(()=>{f.innerHTML='<p style="font-weight:700;color:var(--green)">Дякуємо! Повідомлення надіслано ✓</p>';})
 .catch(()=>{btn.disabled=false;btn.textContent='Надіслати';toast('Не вдалося відправити');});}
function pdQtyChange(d){var i=document.getElementById('pdQty');var v=(+i.value||1)+d;if(v<1)v=1;i.value=v;}
function swapImg(src,el){document.getElementById('galMain').src=src;document.querySelectorAll('.thumbs img').forEach(t=>t.classList.remove('active'));el.classList.add('active');}
// cart page
function renderCart(){var c=getCart();var box=document.getElementById('cartItems');var sum=document.getElementById('cartSummary');
 if(!box)return;
 if(!c.length){document.getElementById('cartMain').innerHTML='<div class="cart-empty"><svg viewBox="0 0 24 24" width="70" height="70" fill="none" stroke="currentColor" stroke-width="1.5"><circle cx="9" cy="20" r="1.4"/><circle cx="18" cy="20" r="1.4"/><path d="M2 3h3l2.4 12.3a2 2 0 0 0 2 1.7h8.2a2 2 0 0 0 2-1.6L23 7H6"/></svg><h2>Кошик порожній</h2><p style="color:#888;margin:10px 0 20px">Оберіть каву в каталозі</p><a href="/" class="btn">До каталогу</a></div>';
  if(sum)sum.style.display='none';return;}
 box.innerHTML=c.map((i,idx)=>`<div class="cart-item"><img src="${i.img}" alt=""><div class="ci-t"><a href="p-${i.slug}.html">${i.title}</a><div class="ci-v">${i.variant||''}</div><button class="ci-remove" onclick="rmItem(${idx})">Видалити</button></div>
  <div class="qty"><button onclick="chQty(${idx},-1)">−</button><input value="${i.qty}" readonly><button onclick="chQty(${idx},1)">+</button></div>
  <div class="ci-price">${(i.price*i.qty).toLocaleString('uk-UA').replace(/,/g,' ')} ₴</div></div>`).join('');
 var total=c.reduce((s,i)=>s+i.price*i.qty,0);var count=c.reduce((s,i)=>s+i.qty,0);
 document.getElementById('sumCount').textContent=count+' товар'+plural(count);
 document.getElementById('sumSubtotal').textContent=total.toLocaleString('uk-UA').replace(/,/g,' ')+' ₴';
 document.getElementById('sumTotal').textContent=total.toLocaleString('uk-UA').replace(/,/g,' ')+' ₴';}
function chQty(i,d){var c=getCart();c[i].qty+=d;if(c[i].qty<1)c[i].qty=1;setCart(c);renderCart();}
function rmItem(i){var c=getCart();c.splice(i,1);setCart(c);renderCart();}
var FS_URL='https://formsubmit.co/ajax/info@npromax.com.ua';
function fsSend(subject,data){
 var body=Object.assign({_subject:subject,_template:'table',_captcha:'false'},data);
 return fetch(FS_URL,{method:'POST',headers:{'Content-Type':'application/json','Accept':'application/json'},body:JSON.stringify(body)});}
function ga(ev,params){try{window.dataLayer=window.dataLayer||[];window.dataLayer.push(Object.assign({event:ev},params||{}));}catch(e){}}
function orderNum(){var d=new Date();var ymd=''+d.getFullYear()+('0'+(d.getMonth()+1)).slice(-2)+('0'+d.getDate()).slice(-2);
 return 'NPX-'+ymd+'-'+('000'+Math.floor(Math.random()*10000)).slice(-4);}
function submitOrder(e){e.preventDefault();var c=getCart();if(!c.length){toast('Кошик порожній');return;}
 var f=e.target;var fd=new FormData(f);var num=orderNum();
 var items=c.map(i=>i.title+' ['+(i.variant||'')+(i.sku?', арт. '+i.sku:'')+'] x'+i.qty+' = '+(i.price*i.qty)+' грн').join('; ');
 var total=c.reduce((s,i)=>s+i.price*i.qty,0);
 var btn=f.querySelector('button[type=submit]');btn.disabled=true;btn.textContent='Відправляємо…';
 fsSend('Замовлення '+num+' з сайту npromax.com.ua',{
  order:num,name:fd.get('name')||'',phone:fd.get('phone')||'',city:fd.get('city')||'',
  np_office:fd.get('np')||'',payment:fd.get('payment')||'',items:items,total:total+' грн'})
 .then(()=>{try{sessionStorage.setItem('npromax_last_order',JSON.stringify({id:num,value:total,
   items:c.map(i=>({item_id:i.sku||i.slug,item_name:i.title,price:i.price,quantity:i.qty}))}));}catch(err){}
  localStorage.removeItem(CART_KEY);updateBadge();location.href='thank-you.html';})
 .catch(()=>{btn.disabled=false;btn.textContent='Оформити замовлення';toast('Не вдалося відправити. Напишіть на info@npromax.com.ua');});}
// thank-you page (NPX-030): show order id + purchase event with repeat guard
function initThankYou(){var el=document.getElementById('tyOrder');if(!el)return;
 var q=new URLSearchParams(location.search);
 // NPX-032/033: лід оренди POLTI — подія generate_lead + Meta Lead один раз
 if(q.get('type')==='rental'){var color=q.get('color')||'';
  var cn=color==='bila'?'біла':(color==='chorna'?'чорна':color);
  el.textContent='Заявку на оренду POLTI'+(cn?(' ('+cn+')'):'')+' прийнято.';
  if(!sessionStorage.getItem('npx_lead_rental')){sessionStorage.setItem('npx_lead_rental','1');
   ga('generate_lead',{form:'rental',color:color,value:0,currency:'UAH'});
   try{if(window.fbq)fbq('track','Lead',{content_name:'rental_'+color});}catch(e){}}
  return;}
 var o=null;
 try{o=JSON.parse(sessionStorage.getItem('npromax_last_order'))}catch(e){}
 if(o&&o.id){el.textContent='Замовлення №'+o.id+' прийнято.';
  var flag='npx_purchase_'+o.id;
  if(!sessionStorage.getItem(flag)){sessionStorage.setItem(flag,'1');
   ga('purchase',{transaction_id:o.id,value:o.value,currency:'UAH',items:o.items||[]});}}
 else{el.textContent='Замовлення прийнято.';}}
function submitB2B(e){e.preventDefault();var f=e.target;var fd=new FormData(f);
 if(fd.get('_honey')){return;}
 var btn=f.querySelector('button[type=submit]');btn.disabled=true;btn.textContent='Відправляємо…';
 var data={};['name','phone','email','city','business','cups','equipment','products','comment'].forEach(k=>data[k]=fd.get(k)||'');
 fsSend('B2B заявка з npromax.com.ua',data)
 .then(()=>{ga('generate_lead',{type:'b2b'});f.style.display='none';document.getElementById('b2bThanks').style.display='block';})
 .catch(()=>{btn.disabled=false;btn.textContent='Надіслати заявку';toast('Не вдалося відправити. Напишіть на info@npromax.com.ua');});}
// NPX-032/033: захоплення UTM/fbclid (реклама FB/IG) у cookie на 30 днів
var TRACK_KEYS=['utm_source','utm_medium','utm_campaign','utm_content','utm_term','fbclid'];
function setCookie(n,v){try{document.cookie=n+'='+encodeURIComponent(v)+';path=/;max-age=2592000;samesite=lax';}catch(e){}}
function getCookie(n){var m=document.cookie.match('(?:^|; )'+n+'=([^;]*)');return m?decodeURIComponent(m[1]):'';}
function trackInit(){try{var q=new URLSearchParams(location.search);
 TRACK_KEYS.forEach(function(k){var v=q.get(k);if(v)setCookie(k,v);});}catch(e){}}
function getTrack(k){try{var q=new URLSearchParams(location.search);return q.get(k)||getCookie(k)||'';}catch(e){return getCookie(k)||'';}}
function rentCalc(){var el=document.getElementById('rcCups');if(!el)return;var cups=+el.value||0;var ch=cups*30;var free=ch>=600;
 var cv=document.getElementById('rcCupsV');if(cv)cv.textContent=cups;
 document.getElementById('rcChalds').textContent=ch;
 var s=document.getElementById('rcStatus');s.textContent=free?'Безкоштовно — 0 грн/міс':'Оренда 1000 грн/міс';
 s.className='rc-status '+(free?'rc-free':'rc-paid');}
function submitRental(e){e.preventDefault();var f=e.target;var fd=new FormData(f);
 if(fd.get('_honey')){return;}
 var btn=f.querySelector('button[type=submit]');btn.disabled=true;btn.textContent='Відправляємо…';
 var color=f.getAttribute('data-color')||fd.get('color')||'';
 var data={};['name','phone','city','place','color','cups','comment'].forEach(k=>data[k]=fd.get(k)||'');
 TRACK_KEYS.forEach(function(k){var v=getTrack(k);if(v)data[k]=v;});
 data.service='Оренда кавомашини POLTI ('+color+')';
 fsSend('Заявка на оренду POLTI ('+color+') — npromax.com.ua',data)
 .then(()=>{try{sessionStorage.setItem('npromax_lead',JSON.stringify({type:'rental',color:color}));}catch(err){}
  location.href='thank-you.html?type=rental&color='+encodeURIComponent(color);})
 .catch(()=>{btn.disabled=false;btn.textContent='Отримати безкоштовну кавомашину';toast('Не вдалося відправити. Напишіть на info@npromax.com.ua');});}
// quiz
var qz={0:null,1:null,2:null};
function qzPick(step,val,el){qz[step]=val;el.parentNode.querySelectorAll('button').forEach(b=>b.classList.remove('sel'));el.classList.add('sel');}
function qzNext(step){if(qz[step]==null){toast('Оберіть варіант');return;}
 if(step<2){document.getElementById('qz'+step).style.display='none';document.getElementById('qz'+(step+1)).style.display='block';
  document.querySelectorAll('.quiz-dots i')[step+1].classList.add('on');}
 else{var map={'кавомашина':'kava-v-zernakh','турка':'svizhomelena-kava','гейзерна':'svizhomelena-kava','фільтр':'svizhomelena-kava','френч-прес':'svizhomelena-kava','капсульна':'kapsuly-nespresso','офіс':'kava-dlya-biznesu'};
  var fmt={'зерно':'kava-v-zernakh','свіжомелена':'svizhomelena-kava','капсули':'kapsuly-nespresso','монодози':'monodozy-ese','набір':'catalog','бізнес':'kava-dlya-biznesu'};
  var dest=fmt[qz[2]]||map[qz[0]]||'catalog';location.href=dest+'.html';}}
document.addEventListener('DOMContentLoaded',function(){trackInit();updateBadge();renderCart();initThankYou();initStickyCta();initSearchUx();rentCalc();
 if(document.querySelector('.lp-sticky'))document.body.classList.add('lp-page');
 document.querySelectorAll('#prodGrid .card').forEach((c,i)=>c.dataset.idx=i);
 var em=document.getElementById('emptyMsg');if(em&&!em.textContent.trim())em.textContent='Нічого не знайдено. Спробуйте змінити фільтри.';
 if(window.SEARCH_DATA)SEARCH_INDEX=window.SEARCH_DATA;
 initCatalogQuery();});
'''
def write_js():
    open(os.path.join(SITE,'assets','app.js'),'w',encoding='utf-8').write(JS)

# category icons (inline)
def cat_icon(kind):
    p={'beans':'<circle cx="12" cy="8" r="4"/><circle cx="8" cy="15" r="3"/><circle cx="16" cy="15" r="3"/>',
       'ground':'<path d="M6 3h12l-1 5H7z"/><path d="M7 8h10v11a2 2 0 0 1-2 2H9a2 2 0 0 1-2-2z"/>',
       'ncap':'<rect x="8" y="3" width="8" height="12" rx="4"/><path d="M8 15h8l-1 5H9z"/>',
       'dcap':'<rect x="7" y="4" width="10" height="10" rx="5"/><path d="M9 14h6v5H9z"/>',
       'drink':'<path d="M4 8h13v5a5 5 0 0 1-5 5H9a5 5 0 0 1-5-5z"/><path d="M17 9h2a2 2 0 0 1 0 5h-2"/>',
       'ese':'<circle cx="12" cy="12" r="8"/><circle cx="12" cy="12" r="3"/>',
       'mono':'<path d="M12 2l3 6.3 6.9 1-5 4.9 1.2 6.8L12 17.8 5.9 21l1.2-6.8-5-4.9 6.9-1z"/>',
       'arom':'<path d="M12 3c0 3-3 4-3 7a3 3 0 0 0 6 0c0-3-3-4-3-7z"/><path d="M6 21h12"/>',
       'blend':'<circle cx="9" cy="9" r="5"/><circle cx="15" cy="15" r="5"/>',
       'decaf':'<circle cx="12" cy="12" r="9"/><path d="M6 6l12 12"/>',
       'b2b':'<path d="M3 21V8l6-4 6 4v13"/><path d="M15 21V11l6 3v7"/><path d="M7 12h2M7 16h2"/>'}
    return f'<svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="#EE7A0E" stroke-width="1.7" stroke-linejoin="round">{p.get(kind,p["beans"])}</svg>'

HOME_FAQ=[
 ("Як швидко ви відправляєте замовлення?","Протягом 1–2 робочих днів після підтвердження менеджером. Доставка — Новою Поштою по всій Україні, зазвичай 1–2 дні."),
 ("Чи можна оплатити при отриманні?","Так, накладеним платежем у відділенні Нової Пошти. Також можлива оплата за реквізитами за рахунком."),
 ("Капсули NPROMAX — це оригінальні Nespresso?","Ні. Це капсули NPROMAX, сумісні з системами Nespresso® Original або Dolce Gusto®. Вони не є продукцією цих брендів — назви вказують лише на технічну сумісність."),
 ("Яка кава підійде для кавомашини?","Зернова: моносорти 100% арабіки — для мʼякого смаку, купажі з робустою — для щільного еспресо з кремою. Підкажемо конкретний сорт — напишіть нам."),
 ("Чи працюєте з офісами та кафе?","Так: ящики капсул 50–100 шт, монодози, зерно 1 кг, регулярні поставки та документи для ФОП/юросіб. Залиште заявку на сторінці «Кава для бізнесу»."),
]
def home(cards, counts):
    home_faq=''.join(f'<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>' for q,a in HOME_FAQ)
    import json as _j
    faq_ld=','.join('{"@type":"Question","name":%s,"acceptedAnswer":{"@type":"Answer","text":%s}}'%(_j.dumps(q,ensure_ascii=False),_j.dumps(a,ensure_ascii=False)) for q,a in HOME_FAQ)
    acad_teasers=''.join(f'<a href="academy-{a["slug"]}.html" class="acad-card"><img src="{COVERS.get(a["slug"],"")}" alt="" loading="lazy"><div class="tag">{a["tag"]}</div><h3>{esc(a["title"])}</h3><p>{esc(a["teaser"])}</p><span class="more">Читати {ICON["arrow"]}</span></a>' for a in ARTICLES[:3])
    beans=[c for c in cards if 'kava-v-zernakh' in c['cats']]
    best= [c for c in cards if c['monosort']][:4] or beans[:4]
    # pick a varied bestsellers set
    picks=[]
    for cat in ['arabika-monosorty','kapsuly-nespresso','aromatyzovana-kava','monodozy-ese']:
        for c in cards:
            if cat in c['cats'] and c not in picks: picks.append(c); break
    while len(picks)<8:
        for c in cards:
            if c not in picks: picks.append(c); break
    picks=picks[:8]
    HOME_IMG={'kava-v-zernakh':'band-beans.jpg','svizhomelena-kava':'band-ground.jpg',
     'kapsuly-nespresso':'band-espresso.jpg','kapsuly-dolce-gusto':'band-flatwhite.jpg',
     'napoyi-v-kapsulakh':'band-drinks.jpg','monodozy-ese':'band-portafilter.jpg',
     'arabika-monosorty':'band-sack.jpg','kavovi-kupazhi':'band-mix.jpg','kava-dlya-biznesu':'b2b-hero.jpg'}
    cats_html=''.join(f'''<a href="{c[0]}.html" class="cat-card cat-card-img">
      <div class="cc-img"><img src="assets/img/{HOME_IMG.get(c[0],'band-texture.jpg')}" alt="{esc(c[1])}" loading="lazy"><span class="cc-count">{counts.get(c[0],0)}</span></div>
      <div class="cc-body"><h3>{esc(c[1])}</h3><p>{esc(c[2])}</p><span class="cat-hint">{esc(c[4])}</span></div></a>''' for c in CATS if c[0]!='kava-bez-kofeinu')
    brews=['Кавомашина','Турка','Гейзерна кавоварка','Френч-прес','Фільтр','Капсульна машина','Офіс']
    brew_dest={'Кавомашина':'kava-v-zernakh','Турка':'svizhomelena-kava','Гейзерна кавоварка':'svizhomelena-kava','Френч-прес':'svizhomelena-kava','Фільтр':'svizhomelena-kava','Капсульна машина':'kapsuly-nespresso','Офіс':'kava-dlya-biznesu'}
    chips=''.join(f'<a href="{brew_dest[b]}.html" class="chip">{b}</a>' for b in brews)
    seo_text='''<p>Ласкаво просимо до NPROMAX — місця, де кава стає щоденним ритуалом. Тут ви можете <b>купити каву</b> в зернах, свіжомелену каву, капсули та монодози з доставкою по всій Україні. У нашому каталозі — <b>кава в зернах</b> для кавомашин, ароматна <b>свіжомелена кава</b> для турки та френч-пресу, а також <b>капсули для кавомашини</b>, сумісні з системами Nespresso Original і Dolce Gusto.</p>
<p>Ми зібрали моносорти 100% <b>арабіки</b> з Ефіопії, Бразилії, Колумбії та інших країн, а також збалансовані купажі з <b>робустою</b> для щільного тіла й насиченої креми. Для тих, хто цінує різноманіття — 26 смаків ароматизованої кави. А для офісів, кафе та HoReCa у нас є вигідні формати: <b>кава для офісу</b>, ящики капсул і монодоз, зернова <b>кава для HoReCa</b> та регулярні поставки.</p>
<p><b>Кава для кавомашини</b>, турки, гейзерної кавоварки, фільтра чи капсульної системи — <b>кава NPROMAX</b> створена, щоб дати максимум смаку без зайвої складності. Актуальні ціни та наявність, зручне оформлення й швидка доставка Новою Поштою — оберіть свій смак, який захочеться повторити.</p>
<p>Не знаєте, з чого почати? Для еспресо в кавомашині беріть <a href="kavovi-kupazhi.html">купажі арабіки з робустою</a> — вони дають щільну крему та впевнену міцність. Для чорної кави без цукру — <a href="arabika-monosorty.html">моносорти 100% арабіки</a>: Бразилія подарує горіхово-шоколадну м'якість, Ефіопія — ягідну яскравість, Колумбія — збалансовану солодкість. Любите десертні смаки — обирайте серед 26 позицій ароматизованої кави наприкінці розділу <a href="kava-v-zernakh.html">«Кава в зернах»</a>. А тим, хто цінує швидкість, підійдуть <a href="kapsuly-nespresso.html">капсули</a> та <a href="monodozy-ese.html">E.S.E. монодози</a> — стабільна чашка одним рухом.</p>
<p>Ми відповідаємо на запитання до покупки, допомагаємо з вибором помелу та формату, відправляємо замовлення протягом 1–2 робочих днів і працюємо як з роздрібними покупцями, так і з <a href="kava-dlya-biznesu.html">бізнесом</a> — офісами, кав'ярнями та HoReCa по всій Україні.</p>'''
    body=f'''
<section class="hero">
  <div class="wrap hero-in">
    <div class="kicker">МАКСИМУМ СМАКУ В КОЖНІЙ ЧАШЦІ</div>
    <h1>NPROMAX — кава,<br>яку хочеться <span>повторити</span></h1>
    <p>Зернова, свіжомелена, капсульна кава та кавові рішення для дому, офісу й бізнесу.</p>
    <div class="hero-cta">
      <a href="catalog.html" class="btn btn-lg">Обрати каву</a>
      <a href="kava-dlya-biznesu.html" class="btn btn-ghost btn-lg">Кава для бізнесу</a>
      <a href="kapsuly-nespresso.html" class="btn btn-ghost btn-lg">Капсули NPROMAX</a>
    </div>
  </div>
</section>
<section class="strip"><div class="wrap strip-in">
  <div class="strip-item">{ICON['refresh']}<div><b>Свіжий помел</b><span>більше аромату в чашці</span></div></div>
  <div class="strip-item">{ICON['star']}<div><b>100% арабіка</b><span>моносорти світу</span></div></div>
  <div class="strip-item">{ICON['shield']}<div><b>Nespresso / Dolce Gusto</b><span>сумісні капсули</span></div></div>
  <div class="strip-item">{ICON['truck']}<div><b>Доставка по Україні</b><span>Нова Пошта</span></div></div>
</div></section>
<section class="section" style="background:var(--crema)"><div class="wrap">
  <div class="section-h"><h2>Оберіть свій формат</h2><div class="sub">Від моносортів до капсул, монодоз і рішень для бізнесу</div></div>
  <div class="cat-grid">{cats_html}</div>
</div></section>
<section class="section" style="padding-top:0"><div class="wrap">
  <div class="section-h row"><div><h2>Хіти продажів</h2><div class="sub">Улюблені смаки покупців NPROMAX</div></div><a href="catalog.html" class="more">Весь каталог {ICON['arrow']}</a></div>
  <div class="grid">{''.join(card_html(c) for c in picks)}</div>
</div></section>
<section class="section" style="padding-top:0"><div class="wrap">
  <div class="section-h"><h2>Як обиратимете каву?</h2><div class="sub">Підкажемо формат під ваш спосіб приготування</div></div>
  <div class="chips">{chips}</div>
</div></section>
<section class="section" style="padding-top:0"><div class="wrap">
  <img class="mood-img" src="assets/img/mood.jpg" alt="Вдома як в ресторані — улюблена кава кожен день" loading="lazy">
</div></section>
<section class="section" style="padding-top:0"><div class="wrap">
  <div class="b2b-band">
    <div class="b2b-txt"><div class="kicker">B2B</div><h2>Кава для офісу та бізнесу</h2>
    <p>Ящики капсул, монодози, зерно 1 кг · регулярні поставки для кафе, ресторанів, HoReCa та вендингу.</p></div>
    <a href="kava-dlya-biznesu.html" class="btn btn-lg">Залишити заявку</a>
  </div>
</div></section>
<section class="section lineup-sec"><div class="wrap" style="display:grid;grid-template-columns:1fr 1.2fr;gap:36px;align-items:center">
  <div><div class="kicker" style="color:var(--orange);letter-spacing:2px;font-size:12px;font-weight:700;margin-bottom:10px">НАША ЛІНІЙКА</div>
  <h2 style="margin-bottom:12px">Від моносортів до ароматизованих</h2>
  <p style="color:var(--muted);margin-bottom:18px">27 моносортів 100% арабіки з усього світу та 26 смаків ароматизованої кави — у зернах і свіжомеленій. Кожен пакет — 1 кг свіжого смаку.</p>
  <a href="kava-v-zernakh.html" class="btn">Обрати зерно</a></div>
  <img src="assets/img/lineup.jpg" alt="Лінійка кави NPROMAX" loading="lazy">
</div></section>
<section class="section" style="padding-top:0;padding-bottom:0"><div class="wrap">
  <div class="section-h row"><div><h2>Академія смаку</h2><div class="sub">Корисно про каву — коротко і по суті</div></div><a href="academy.html" class="more">Усі статті {ICON['arrow']}</a></div>
  <div class="acad-grid">{acad_teasers}</div>
</div></section>
<section class="section"><div class="wrap"><div class="quiz" id="quiz">
  <h3>Помічник вибору кави</h3><div class="q-sub">3 питання — і ми покажемо, з чого почати</div>
  <div class="quiz-dots" style="margin-bottom:18px"><i class="on"></i><i></i><i></i></div>
  <div class="quiz-step" id="qz0"><div class="qz-q">1. Де будете готувати каву?</div>
    <div class="quiz-opts">{''.join(f'<button onclick="qzPick(0,&#39;{b.lower()}&#39;,this)">{b}</button>' for b in ['Кавомашина','Турка','Гейзерна','Фільтр','Френч-прес','Капсульна','Офіс'])}</div>
    <div class="quiz-nav"><span></span><button class="btn" onclick="qzNext(0)">Далі</button></div></div>
  <div class="quiz-step" id="qz1" style="display:none"><div class="qz-q">2. Який смак любите?</div>
    <div class="quiz-opts">{''.join(f'<button onclick="qzPick(1,&#39;{b.lower()}&#39;,this)">{b}</button>' for b in ['М’який','Міцний','Шоколадний','Горіховий','Фруктовий','З кислинкою','Ароматизований'])}</div>
    <div class="quiz-nav"><span></span><button class="btn" onclick="qzNext(1)">Далі</button></div></div>
  <div class="quiz-step" id="qz2" style="display:none"><div class="qz-q">3. Який формат потрібен?</div>
    <div class="quiz-opts">{''.join(f'<button onclick="qzPick(2,&#39;{b.lower()}&#39;,this)">{b}</button>' for b in ['Зерно','Свіжомелена','Капсули','Монодози','Набір','Бізнес'])}</div>
    <div class="quiz-nav"><span></span><button class="btn" onclick="qzNext(2)">Показати добірку</button></div></div>
</div></div></section>
<section class="section" style="padding-top:0"><div class="wrap">
  <div class="section-h"><h2>Чому NPROMAX</h2><div class="sub">Чесно і без пафосу</div></div>
  <div class="cat-grid">
    <div class="cat-card"><h3>126 позицій кави</h3><p>Моносорти зі всього світу, ароматизовані смаки, капсули та монодози — все в одному місці.</p></div>
    <div class="cat-card"><h3>Ціни оновлюються щодня</h3><p>Сайт щодня синхронізується з нашим магазином на Prom.ua — ціни та наявність актуальні.</p></div>
    <div class="cat-card"><h3>Формати під вас</h3><p>Від упаковки 10 капсул для проби до ящиків і кілограмів зерна для офісу та HoReCa.</p></div>
    <div class="cat-card"><h3>Допоможемо обрати</h3><p>Не впевнені у смаку чи форматі? Напишіть нам — підкажемо під вашу кавомашину і звички.</p></div>
  </div>
</div></section>
<section class="section" style="padding-top:0"><div class="wrap">
  <div class="b2b-band" style="align-items:stretch">
    <div class="b2b-txt"><div class="kicker">КОНСУЛЬТАЦІЯ</div><h2>Не знаєте, що обрати?</h2>
    <p>Залиште номер — менеджер підкаже сорт і формат під ваш спосіб приготування.</p></div>
    <form onsubmit="leadCapture(event)" style="display:flex;gap:10px;align-items:center;flex-wrap:wrap;min-width:280px">
      <input type="text" name="name" placeholder="Ім'я" style="flex:1;min-width:110px;padding:12px 14px;border-radius:10px;border:none;font-family:inherit">
      <input type="tel" name="phone" required placeholder="Телефон" style="flex:1.2;min-width:140px;padding:12px 14px;border-radius:10px;border:none;font-family:inherit">
      <input type="text" name="_honey" style="display:none" tabindex="-1" autocomplete="off">
      <button class="btn">Передзвоніть мені</button>
    </form>
  </div>
</div></section>
<section class="section" style="padding-top:0"><div class="wrap"><div class="seo-block">
  <h2>Кава NPROMAX — купити свіжу каву в Україні</h2>{seo_text}
  <h2 style="margin-top:24px">Часті питання</h2>
  <div class="faq">{home_faq}</div>
</div></div></section>
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{faq_ld}]}}</script>
'''
    return layout('NPROMAX — кава, яку хочеться повторити | купити каву в Україні',
        'Купити каву NPROMAX: кава в зернах, свіжомелена кава, капсули для кавомашини (Nespresso, Dolce Gusto), E.S.E. монодози, 100% арабіка. Доставка по Україні.',
        body, active='', canonical='')

FAQ = {
 'kava-v-zernakh':[('Для яких кавомашин підходить зернова кава NPROMAX?','Зернова кава NPROMAX підходить для автоматичних кавомашин, ріжкових кавоварок, а після помелу — для турки, гейзерної кавоварки та френч-пресу.'),
  ('Який ступінь обсмаження у кави в зернах?','Більшість позицій має середнє обсмаження — універсальний баланс кислотності та щільності для еспресо й фільтра.'),
  ('Яка вага упаковки?','Основний формат — 1 кг, зручний для дому та офісу.'),
  ('Чи є моносорти?','Так, у нас представлені моносорти 100% арабіки з Ефіопії, Бразилії, Колумбії та інших країн.')],
 'svizhomelena-kava':[('Для якого способу приготування підходить помел?','У картці кожного товару вказано, для якого способу краще розкривається помел. Якщо потрібна порада — підкажемо за телефоном.'),
  ('Чим свіжомелена кава краща за зернову?','Свіжомелена кава — це готове рішення без власної кавомолки: ви одразу отримуєте аромат без додаткових пристроїв.'),
  ('Як зберігати мелену каву?','У щільно закритій упаковці, подалі від світла, вологи та сторонніх запахів.')],
 'kapsuly-nespresso':[('Чи це оригінальні капсули Nespresso?','Ні. Це капсули NPROMAX, сумісні з системою Nespresso® Original. Nespresso® — торговельна марка її власника; NPROMAX не афілійований з нею.'),
  ('Скільки капсул в упаковці?','Доступні упаковки 10 і 20 штук, а також ящики 50 і 100 штук для бізнесу.'),
  ('Які бленди є?','Premium, Espresso, Robusta та Decaffeinato (без кофеїну).')],
 'kava-dlya-biznesu':[('Які формати доступні для бізнесу?','Ящики капсул (50/100 шт), монодози E.S.E. та зернова кава 1 кг.'),
  ('Чи є регулярні поставки?','Так, ми налаштовуємо регулярні поставки під потреби офісу, кафе, ресторану чи вендингу.'),
  ('Як залишити заявку?','Заповніть форму на цій сторінці — менеджер зв’яжеться й підбере оптимальний формат.')],
}
DEFAULT_FAQ=[('Як оформити замовлення?','Додайте товари в кошик і заповніть дані для доставки Новою Поштою.'),
 ('Яка доставка?','Доставка по всій Україні Новою Пошта — на відділення або адресно.'),
 ('Чи актуальні ціни та наявність?','Так, ціни та наявність оновлюються щодня.')]

def merchant_feed(cards):
    """NPX-014: Google Merchant RSS 2.0 (g:). 126 позицій, link=self, image абсолютний.
    НЕ завантажується в Merchant без окремого «так» власника (§37, питання 17.1)."""
    import datetime as _dt
    BASE='https://www.npromax.com.ua/'
    GCAT={'drink':'413'}          # напої → Beverages; решта → Coffee 1868
    def absu(u): return u if (u or '').startswith('http') else BASE+(u or '').lstrip('/')
    def x(s): return esc(str(s or ''))
    items=[]
    for c in cards:
        sku=c['vendor_code']
        if not sku: continue
        gcat=GCAT.get(c['type'],'1868')
        items.append(
 f'''  <item>
    <g:id>{x(sku)}</g:id>
    <g:title>{x(c['title'])}</g:title>
    <g:description>{x(desc_intro(c)[:400])}</g:description>
    <g:link>{BASE}p-{x(c['slug'])}.html</g:link>
    <g:image_link>{x(absu(c['image']))}</g:image_link>
    <g:availability>{'in_stock' if c['available'] else 'out_of_stock'}</g:availability>
    <g:price>{int(c['price_min'])} UAH</g:price>
    <g:brand>NPROMAX</g:brand>
    <g:condition>new</g:condition>
    <g:identifier_exists>no</g:identifier_exists>
    <g:google_product_category>{gcat}</g:google_product_category>
    <g:custom_label_0>{x(CATMAP.get(c['primary'],['','' ,''])[1])}</g:custom_label_0>
  </item>''')
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
      '<rss version="2.0" xmlns:g="http://base.google.com/ns/1.0">\n<channel>\n'
      '<title>NPROMAX — кава</title>\n'
      f'<link>{BASE}</link>\n'
      '<description>Кавовий фід NPROMAX: зерно, мелена, капсули, монодози, напої.</description>\n'
      + '\n'.join(items) + '\n</channel>\n</rss>\n')

def crumb_ld(pairs):
    """NPX-018: BreadcrumbList schema. pairs = [(name, path)], path '' = головна."""
    BASE='https://www.npromax.com.ua/'
    els=[{"@type":"ListItem","position":i+1,"name":n,"item":BASE+(p or '')} for i,(n,p) in enumerate(pairs)]
    return '<script type="application/ld+json">'+json.dumps(
        {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":els},ensure_ascii=False)+'</script>'

def category_page(slug, cards, counts):
    meta=CATMAP[slug]
    items=[c for c in cards if slug in c['cats']]
    # order: available first, then price
    items.sort(key=lambda c:(1 if c['aroma'] else 0, 0 if c['available'] else 1, c['price_min']))
    # filter facets from items
    comps=sorted({c['composition'] for c in items if c['composition']})
    countries=sorted({c['country'] for c in items if c['country']})
    types=sorted({c['type'] for c in items})
    typenames={'beans':'Кава в зернах','ground':'Свіжомелена','ncap':'Капсули Nespresso','dcap':'Капсули Dolce Gusto','drink':'Напої в капсулах','ese':'E.S.E. монодози'}
    fhtml='<h4>Склад</h4>'+''.join(f'<label class="f-opt"><input type="checkbox" data-g="comp" value="{esc(x)}" onchange="applyFilters()">{esc(x)}</label>' for x in comps) if comps else ''
    if len(types)>1:
        fhtml+='<h4>Тип</h4>'+''.join(f'<label class="f-opt"><input type="checkbox" data-g="type" value="{t}" onchange="applyFilters()">{typenames.get(t,t)}</label>' for t in types)
    if countries:
        fhtml+='<h4>Країна</h4>'+''.join(f'<label class="f-opt"><input type="checkbox" data-g="country" value="{esc(x)}" onchange="applyFilters()">{esc(x)}</label>' for x in countries)
    has_ar=any(c['aroma'] for c in items); has_nat=any(not c['aroma'] for c in items)
    if has_ar and has_nat:
        fhtml+='<h4>Тип кави</h4>'
        fhtml+='<label class="f-opt"><input type="checkbox" data-g="kind" value="aroma" onchange="applyFilters()">Ароматизована</label>'
        fhtml+='<label class="f-opt"><input type="checkbox" data-g="kind" value="natural" onchange="applyFilters()">Натуральна (моносорт/купаж)</label>'
    if any(c['decaf'] for c in items) and any(not c['decaf'] for c in items):
        fhtml+='<h4>Властивості</h4><label class="f-opt"><input type="checkbox" data-g="prop" value="decaf" onchange="applyFilters()">Без кофеїну</label>'
    fhtml+='<h4>Ціна, ₴</h4><div style="display:flex;gap:8px"><input type="number" id="fMin" placeholder="від" min="0" style="width:50%;padding:8px;border:1px solid var(--line);border-radius:8px;font-family:inherit" oninput="applyFilters()"><input type="number" id="fMax" placeholder="до" min="0" style="width:50%;padding:8px;border:1px solid var(--line);border-radius:8px;font-family:inherit" oninput="applyFilters()"></div>'
    fhtml+='<h4>Наявність</h4><label class="f-opt"><input type="checkbox" data-g="avail" value="1" onchange="applyFilters()">В наявності</label>'
    nat=[c for c in items if not c['aroma']]; ar=[c for c in items if c['aroma']]
    grid=''.join(card_html(c) for c in nat)
    if nat and ar: grid+='<div class="aroma-divider" id="aromaDivider"><span>Ароматизована кава</span></div>'
    grid+=''.join(card_html(c) for c in ar)
    if not items: grid='<p class="empty">У цій категорії поки немає товарів.</p>'
    faq=FAQ.get(slug,DEFAULT_FAQ)
    faq_html=''.join(f'<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>' for q,a in faq)
    related=[x for x in CATS if x[0]!=slug][:6]
    rel_html=' · '.join(f'<a href="{r[0]}.html" style="color:var(--orange)">{esc(r[1])}</a>' for r in related)
    n=len(items)
    body=f'''
{crumb_ld([('Головна',''),(meta[1], slug+'.html')])}
<div class="wrap"><div class="crumb"><a href="/">Головна</a><span>›</span>{esc(meta[1])}</div></div>
{band_open(slug)}<div class="wrap cat-head"><h1>{esc(meta[1])}</h1><p class="lead">{esc(meta[5])}</p></div></div>
<div class="wrap"><div class="catalog">
  <aside class="filters">{fhtml}<button class="f-reset" onclick="resetFilters()">Скинути фільтри</button></aside>
  <div>
    <div class="toolbar">
      <button class="btn btn-outline mobile-filter-btn" onclick="toggleFilters()">Фільтри</button>
      <span class="found" id="foundCount">{n} товар{'ів' if n%100//10==1 or n%10 in(0,5,6,7,8,9) else ('' if n%10==1 else 'и')}</span>
      <select onchange="sortGrid(this.value)"><option value="">За популярністю</option><option value="price-asc">Ціна: спочатку дешевші</option><option value="price-desc">Ціна: спочатку дорожчі</option><option value="name">За назвою</option></select>
    </div>
    <div class="grid" id="prodGrid">{grid}</div>
    <p class="empty" id="emptyMsg" style="display:none"></p>
  </div>
</div></div>
<div class="wrap"><div class="seo-block">
  <h2>Про категорію «{esc(meta[1])}»</h2><p>{esc(meta[5])}</p>
  <p>Дивіться також: {rel_html}.</p>
  <h2 style="margin-top:24px">Часті питання</h2><div class="faq">{faq_html}</div>
</div></div>
<div style="height:40px"></div>
'''
    title=f'{meta[1]} — купити | NPROMAX'
    return layout(title, meta[5][:155], body, active=(slug if slug in NAV else ''), canonical=slug+'.html')

def catalog_page(cards):
    items=sorted(cards,key=lambda c:(1 if c['aroma'] else 0, 0 if c['available'] else 1, c['price_min']))
    nat=[c for c in items if not c['aroma']]; ar=[c for c in items if c['aroma']]
    grid=''.join(card_html(c) for c in nat)
    if nat and ar: grid+='<div class="aroma-divider" id="aromaDivider"><span>Ароматизована кава</span></div>'
    grid+=''.join(card_html(c) for c in ar)
    n=len(items)
    body=f'''
{crumb_ld([('Головна',''),('Каталог','catalog.html')])}
<div class="wrap"><div class="crumb"><a href="/">Головна</a><span>›</span>Каталог</div></div>
{band_open("catalog")}<div class="wrap cat-head"><h1>Каталог NPROMAX</h1><p class="lead">Уся кава NPROMAX: зерно, свіжомелена, капсули, монодози та рішення для бізнесу — {n} позицій.</p></div></div>
<div class="wrap"><div class="catalog">
  <aside class="filters">
    <h4>Тип</h4>
    <label class="f-opt"><input type="checkbox" data-g="type" value="beans" onchange="applyFilters()">Кава в зернах</label>
    <label class="f-opt"><input type="checkbox" data-g="type" value="ground" onchange="applyFilters()">Свіжомелена</label>
    <label class="f-opt"><input type="checkbox" data-g="type" value="ncap" onchange="applyFilters()">Капсули Nespresso</label>
    <label class="f-opt"><input type="checkbox" data-g="type" value="dcap" onchange="applyFilters()">Капсули Dolce Gusto</label>
    <label class="f-opt"><input type="checkbox" data-g="type" value="ese" onchange="applyFilters()">E.S.E. монодози</label>
    <label class="f-opt"><input type="checkbox" data-g="type" value="drink" onchange="applyFilters()">Напої в капсулах</label>
    <h4>Тип кави</h4>
    <label class="f-opt"><input type="checkbox" data-g="kind" value="aroma" onchange="applyFilters()">Ароматизована</label>
    <label class="f-opt"><input type="checkbox" data-g="kind" value="natural" onchange="applyFilters()">Натуральна (моносорт/купаж)</label>
    <h4>Властивості</h4>
    <label class="f-opt"><input type="checkbox" data-g="prop" value="decaf" onchange="applyFilters()">Без кофеїну</label>
    <h4>Ціна, ₴</h4><div style="display:flex;gap:8px"><input type="number" id="fMin" placeholder="від" min="0" style="width:50%;padding:8px;border:1px solid var(--line);border-radius:8px;font-family:inherit" oninput="applyFilters()"><input type="number" id="fMax" placeholder="до" min="0" style="width:50%;padding:8px;border:1px solid var(--line);border-radius:8px;font-family:inherit" oninput="applyFilters()"></div>
    <h4>Наявність</h4><label class="f-opt"><input type="checkbox" data-g="avail" value="1" onchange="applyFilters()">В наявності</label>
    <button class="f-reset" onclick="resetFilters()">Скинути фільтри</button>
  </aside>
  <div>
    <div id="searchBar" class="grind-note" style="display:none;margin-bottom:14px"></div>
    <div class="toolbar"><button class="btn btn-outline mobile-filter-btn" onclick="toggleFilters()">Фільтри</button>
      <span class="found" id="foundCount">{n} товарів</span>
      <select onchange="sortGrid(this.value)"><option value="">За популярністю</option><option value="price-asc">Ціна ↑</option><option value="price-desc">Ціна ↓</option><option value="name">За назвою</option></select></div>
    <div class="grid" id="prodGrid">{grid}</div>
    <p class="empty" id="emptyMsg" style="display:none"></p>
  </div>
</div></div><div style="height:40px"></div>
'''
    return layout('Каталог кави NPROMAX — купити каву в Україні','Весь каталог NPROMAX: кава в зернах, свіжомелена, капсули, монодози. Купити каву з доставкою по Україні.',body,active='',canonical='catalog.html')

def desc_intro(card):
    t=card['type']
    if t=='beans': return f"Кава в зернах NPROMAX{(' '+card['title'].split('NPROMAX')[-1].strip()) if 'NPROMAX' in card['title'] else ''} — це насичений аромат і стабільний смак у кожній чашці. Створена для тих, хто цінує якісну каву вдома та в офісі."
    if t=='ground': return "Свіжомелена кава NPROMAX — це більше аромату в кожній чашці. Готове рішення без власної кавомолки: ви одразу отримуєте зручний формат для улюбленого способу приготування."
    if t in('ncap','dcap'): return "Насичений еспресо у зручній капсулі — швидко, чисто та стабільно смачно. Ідеально для дому та офісу."
    if t=='ese': return "E.S.E. монодоза — готова порція меленої кави для ідеального еспресо з пінкою. Просто вставте чалду 44 мм у сумісну кавоварку."
    if t=='drink': return "Улюблений напій у зручній капсулі — швидке приготування без зайвих зусиль."
    return "Смачна кава NPROMAX для вашого щоденного ритуалу."

def brew_methods(card):
    t=card['type']
    if t=='beans': return ['Автоматична кавомашина','Ріжкова кавоварка','Гейзерна кавоварка','Турка (після помелу)','Френч-прес','Фільтр']
    if t=='ground': return ['Турка','Гейзерна кавоварка','Френч-прес','Фільтр']
    if t=='ncap': return ['Кавомашини Nespresso® Original']
    if t=='dcap': return ['Кавомашини Dolce Gusto®']
    if t=='ese': return ['Кавоварки стандарту E.S.E. 44 мм']
    return ['Капсульна кавомашина']

def profile_bars(card):
    # derive from params; neutral defaults
    p=card['params']
    def lvl(name,default):
        v=(p.get(name) or '').lower()
        if 'высок' in v or 'висок' in v or 'сильн' in v: return 85
        if 'средн' in v or 'серед' in v: return 55
        if 'низк' in v or 'низьк' in v or 'слаб' in v: return 30
        if 'без' in v: return 10
        return default
    rows=[('Міцність',lvl('Крепость кофе',55)),('Кислотність',lvl('Кислотность кофе',45)),('Гірчинка',lvl('Горечь кофе',50))]
    return ''.join(f'<div class="prof-row"><span>{n}</span><div class="prof-bar"><i style="width:{w}%"></i></div></div>' for n,w in rows)

def product_page(card, cards):
    slug=card['slug']; meta=CATMAP[card['primary']]
    imgs=card['images'] or [card['image']]
    thumbs=''.join(f'<img src="{esc(u)}" alt="{esc(card["title"])} — фото {i+1}" class="{"active" if i==0 else ""}" width="66" height="66" onclick="swapImg(&#39;{esc(u)}&#39;,this)">' for i,u in enumerate(imgs[:5])) if len(imgs)>1 else ''
    vopts=''
    if len(card['variants'])>1:
        vparts=[]
        for i,v in enumerate(card['variants']):
            vp=v['price'] or 0
            vlab=esc(v['label'])
            vprice=money(v['price']) if v['price'] else '—'
            act='active' if i==0 else ''
            vparts.append(f'<div class="vopt {act}" onclick="selVariant(this,{vp},&#39;{vlab}&#39;)"><b>{vlab}</b><span>{vprice} ₴</span></div>')
        vopts=''.join(vparts)
    # specs
    p=card['params']
    specrows=[]
    def add(k,v):
        if v: specrows.append((k,v))
    tn={'beans':'Кава в зернах','ground':'Свіжомелена кава','ncap':'Капсули (Nespresso Original compatible)','dcap':'Капсули (Dolce Gusto compatible)','ese':'E.S.E. монодози 44 мм','drink':'Напій у капсулах'}
    add('Тип',tn.get(card['type']))
    add('Склад',card['composition'])
    add('Країна походження',card['country'])
    add('Ступінь обсмаження',{'Средняя':'Середня','Высокая':'Висока','Слабая':'Слабка'}.get(p.get('Степень обжарки'),p.get('Степень обжарки')))
    if p.get('Вес') and p.get('Вес')!='0':
        w=p.get('Вес')
        # Prom-дані непослідовні: більшість ваг у грамах ('1000'=1кг, '275'=275г),
        # але ящики мають десяткове значення в кг ('6.5' = 6.5 кг). int(w) на '6.5' крешив увесь білд.
        try:
            wi=int(w)
            wv='1 кг' if wi==1000 else f'{w} г'
        except ValueError:
            try:
                wv=f'{float(w):g} кг'   # десяткові — це кілограми (великі упаковки)
            except ValueError:
                wv=str(w)
        add('Вага', wv)
    add('Кількість в упаковці', p.get('Количество в упаковке (шт.)') or p.get('Количество в упаковке'))
    add('Кофеїн',{'Средний':'Середній','Высокий':'Високий','Без кофеина':'Без кофеїну'}.get(p.get('Кофеин'),p.get('Кофеин')))
    add('Бренд','NPROMAX'); add('Артикул',card['vendor_code'])
    spec_html=''.join(f'<tr><td>{esc(k)}</td><td>{esc(str(v))}</td></tr>' for k,v in specrows)
    brews=brew_methods(card)
    brew_html=''.join(f'<div class="brew-item">{ICON["check"]}{esc(b)}</div>' for b in brews)
    disclaimer=''
    if card['type'] in('ncap','dcap','drink') or 'nespresso' in card['title'].lower() or 'dolce' in card['title'].lower():
        disclaimer='<div class="disclaimer">Nespresso® / Dolce Gusto® є зареєстрованими торговельними марками їхніх власників. Продукт NPROMAX не виробляється та не афілійований з власниками цих торговельних марок. Назва використовується виключно для позначення технічної сумісності.</div>'
    grind_note=''
    if card['type']=='ground':
        grind_note='<div class="grind-note"><b>Свіжомелена кава NPROMAX — це більше аромату в кожній чашці.</b> Ми мелемо каву так, щоб вона краще розкривалася саме у вашому способі приготування: для турки — дуже дрібний помел, для еспресо — дрібний, для гейзерної кавоварки — середньо-дрібний, для фільтра — середній, для френч-пресу — грубий.</div>'
    # related
    related=[c for c in cards if c['primary']==card['primary'] and c['slug']!=slug][:4]
    if len(related)<4:
        for c in cards:
            if c not in related and c['slug']!=slug: related.append(c)
            if len(related)>=4: break
    rel_html=''.join(card_html(c) for c in related[:4])
    old = ''
    avail='<span class="in-stock">В наявності</span>' if card['available'] else '<span class="no-stock">Немає в наявності</span>'
    # NPX-017: absolute image URLs, offers.url = canonical, priceValidUntil = build_date+30d
    import datetime as _dt
    BASE='https://www.npromax.com.ua/'
    absu=lambda u: u if u.startswith('http') else BASE+u.lstrip('/')
    canonical_url=f"{BASE}p-{slug}.html"
    price_valid=(_dt.date.today()+_dt.timedelta(days=30)).isoformat()
    jsonld=json.dumps({"@context":"https://schema.org","@type":"Product","name":card['title'],
      "image":[absu(u) for u in imgs[:3]],"description":desc_intro(card),"sku":card['vendor_code'],"brand":{"@type":"Brand","name":"NPROMAX"},
      "offers":{"@type":"Offer","url":canonical_url,"priceCurrency":"UAH","price":int(card['price_min']),
        "priceValidUntil":price_valid,
        "availability":"https://schema.org/InStock" if card['available'] else "https://schema.org/OutOfStock",
        "itemCondition":"https://schema.org/NewCondition"}},ensure_ascii=False)
    breadcrumb_ld=json.dumps({"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
      {"@type":"ListItem","position":1,"name":"Головна","item":BASE},
      {"@type":"ListItem","position":2,"name":meta[1],"item":f"{BASE}{card['primary']}.html"},
      {"@type":"ListItem","position":3,"name":card['title'],"item":canonical_url}]},ensure_ascii=False)
    addbtn=json.dumps({"slug":slug,"sku":card['vendor_code'] or '',"title":card['title'],"price":card['price_min'],"img":card['image'],"variant":card['variants'][0]['label']},ensure_ascii=False)
    body=f'''
<script type="application/ld+json">{jsonld}</script>
<script type="application/ld+json">{breadcrumb_ld}</script>
<script>var __pd={addbtn};window.__pdSlug=__pd.slug;window.__pdSku=__pd.sku;window.__pdTitle=__pd.title;window.__pdPrice=__pd.price;window.__pdImg=__pd.img;window.__pdVariant=__pd.variant;</script>
<div class="wrap"><div class="crumb"><a href="/">Головна</a><span>›</span><a href="{card['primary']}.html">{esc(meta[1])}</a><span>›</span>{esc(card['title'])}</div></div>
<div class="wrap"><div class="pd">
  <div>
    <div class="gallery-main"><img src="{esc(imgs[0])}" alt="{esc(card['title'])} — фото упаковки" id="galMain" width="600" height="600"></div>
    <div class="thumbs">{thumbs}</div>
  </div>
  <div class="pd-info">
    <div class="pd-badges">{badge(card)}</div>
    <h1>{esc(card['title'])}</h1>
    <div class="pd-meta">{avail} · Артикул: {esc(card['vendor_code'] or '—')}</div>
    <div class="pd-price">{old}<span class="now" id="pdPrice">{money(card['price_min'])} ₴</span></div>
    {'<div class="variants"><div class="vlab">Оберіть упаковку:</div><div class="vopts">'+vopts+'</div></div>' if vopts else ''}
    <div class="pd-buy">
      <div class="qty"><button onclick="pdQtyChange(-1)">−</button><input id="pdQty" value="1" readonly><button onclick="pdQtyChange(1)">+</button></div>
      <button class="btn btn-lg" style="flex:1.2" onclick="pdAdd(true)">Купити зараз</button>
      <button class="btn btn-ghost btn-lg" style="flex:1" onclick="pdAdd()">Додати в кошик</button>
    </div>
    <form class="oneclick" onsubmit="oneClickBuy(event)">
      <input type="text" name="name" placeholder="Ім'я">
      <input type="tel" name="phone" required placeholder="Телефон">
      <input type="text" name="_honey" style="display:none" tabindex="-1" autocomplete="off">
      <button type="submit" class="btn btn-outline">Купити в 1 клік</button>
    </form>
    <p style="font-size:11.5px;color:var(--muted);margin:0 0 8px">Натискаючи кнопку, ви погоджуєтесь із <a href="privacy.html" style="color:var(--orange)">політикою конфіденційності</a>.</p>
    <div id="oneClickOk" class="grind-note" style="display:none"><b>Дякуємо! Заявку прийнято.</b> Менеджер зателефонує найближчим часом, підтвердить замовлення та відповість на запитання.</div>
    {grind_note}
    <div class="pd-feats">
      <div class="pd-feat">{ICON['truck']}<div><b>Доставка Новою Поштою</b> по всій Україні — на відділення, поштомат або адресно.</div></div>
      <div class="pd-feat">{ICON['refresh']}<div><b>Повернення 14 днів</b> згідно з чинним законодавством України.</div></div>
      <div class="pd-feat">{ICON['shield']}<div><b>Оплата:</b> при отриманні (накладений платіж) або за рахунком.</div></div>
    </div>
    {disclaimer}
  </div>
</div></div>
<div class="wrap"><div class="pd-section"><h2>Опис</h2><div class="pd-desc">
{desc_blocks(card)}
</div></div></div>
<div class="wrap"><div class="pd-section"><h2>Смаковий профіль</h2><div class="profile">{profile_bars(card)}</div></div></div>
<div class="wrap"><div class="pd-section"><h2>Способи приготування</h2><div class="brew-list">{brew_html}</div></div></div>
<div class="wrap"><div class="pd-section"><h2>Характеристики</h2><table class="spec-table">{spec_html}</table></div></div>
<div class="wrap"><div class="pd-section"><h2>Схожі товари</h2><div class="grid">{rel_html}</div></div></div>
<div style="height:30px"></div>
<div class="sticky-cta" id="stickyCta"><span class="sc-price" id="scPrice">{money(card['price_min'])} ₴</span><button class="btn" onclick="pdAdd()">У кошик</button></div>
'''
    st=card['title']
    st=st.replace(', сумісних із системою Nespresso®',' — Nespresso Original сумісні').replace(', сумісних із системою Dolce Gusto®',' — Dolce Gusto сумісні').replace(', сумісних з системою Nespresso®',' — Nespresso Original сумісні')
    if len(st)>62: st=st[:62].rsplit(' ',1)[0]
    title=f"{st} купити | NPROMAX"
    return layout(title, (desc_intro(card)[:150]), body, active='', canonical=f"p-{slug}.html")

def b2b_page(cards):
    items=[c for c in cards if 'kava-dlya-biznesu' in c['cats']]
    items.sort(key=lambda c:c['price_min'])
    grid=''.join(card_html(c) for c in items[:12])
    blocks=[('Рішення для офісу','Зернова кава для кавомашин, капсули та монодози — щоб колеги завжди мали смачну чашку.'),
            ('Кафе та ресторани','Стабільні бленди для еспресо, вигідні формати та регулярні поставки для HoReCa.'),
            ('Оренда кавомашини','Polti Coffea S18 під чалди E.S.E. 44 мм: 500 грн/міс або безкоштовно від 300 чалд на місяць.'),
            ('Вендинг','Кава в зернах і капсулах для вендингових автоматів — надійний смак у кожному стакані.'),
            ('Регулярні поставки','Налаштуємо графік поставок під ваше споживання — без перебоїв і зайвого клопоту.')]
    bl_html=''.join(f'<div class="cat-card"><h3>{esc(t)}</h3><p>{esc(d)}</p></div>' for t,d in blocks)
    body=f'''
{crumb_ld([('Головна',''),('Кава для бізнесу','kava-dlya-biznesu.html')])}
<div class="wrap"><div class="crumb"><a href="/">Головна</a><span>›</span>Кава для бізнесу</div></div>
<section class="hero hero-b2b"><div class="wrap hero-in">
  <div class="kicker">B2B · ОПТ · HORECA</div>
  <h1>Кава для офісу<br>та <span>бізнесу</span></h1>
  <p>Підберемо каву під ваш формат: зерно, капсули, монодози та великі упаковки. Зручні ящики, гуртові позиції та регулярні поставки.</p>
  <a href="#lead" class="btn btn-lg">Залишити заявку</a>
</div></section>
<section class="section"><div class="wrap">
  <div class="section-h"><h2>Підберемо каву під ваш формат</h2><div class="sub">Для офісів, кафе, ресторанів, HoReCa, вендингу та оптових клієнтів</div></div>
  <div class="cat-grid">{bl_html}</div>
</div></section>
<section class="section" style="padding-top:0"><div class="wrap">
  <div class="section-h"><h2>Популярні бізнес-формати</h2><div class="sub">Ящики капсул, монодози та зерно 1 кг</div></div>
  <div class="grid">{grid}</div>
</div></section>
<section class="section" style="padding-top:0"><div class="wrap"><a href="#lead"><img class="mood-img" src="assets/img/b2b-banner.jpg" alt="Кава для бізнесу — вигідні формати для офісу, кафе та HoReCa" loading="lazy"></a></div></section>
<section class="section" style="padding-top:0" id="lead"><div class="wrap"><div style="max-width:640px;margin:0 auto;background:var(--soft);border-radius:16px;padding:34px">
  <h2 style="margin-bottom:6px">Залишити заявку</h2><p style="color:var(--muted);margin-bottom:22px">Менеджер зв’яжеться й підбере оптимальний формат та ціну.</p>
  <form onsubmit="submitB2B(event)" id="b2bForm">
    <div class="form-row"><label>Ім’я *</label><input name="name" required placeholder="Ваше ім’я"></div>
    <div class="form-row"><label>Телефон *</label><input name="phone" required type="tel" placeholder="+38 (0__) ___-__-__"></div>
    <div class="form-row"><label>Email</label><input name="email" type="email" placeholder="you@company.com"></div>
    <div class="form-row"><label>Місто</label><input name="city" placeholder="Місто доставки"></div>
    <div class="form-row"><label>Формат бізнесу</label><select name="business"><option>Офіс</option><option>Кафе / ресторан</option><option>HoReCa</option><option>Вендинг</option><option>Магазин</option><option>Опт</option></select></div>
    <div class="form-row"><label>Скільки чашок кави на день?</label><input name="cups" placeholder="Напр. 30–50"></div>
    <div class="form-row"><label>Яке обладнання використовуєте?</label><input name="equipment" placeholder="Кавомашина, капсульна система…"></div>
    <div class="form-row"><label>Які товари цікавлять?</label><input name="products" placeholder="Зерно 1 кг, капсули ящиками, монодози…"></div>
    <div class="form-row"><label>Коментар</label><textarea name="comment" rows="3" placeholder="Додаткові побажання"></textarea></div>
    <input type="text" name="_honey" style="display:none" tabindex="-1" autocomplete="off">
    <label class="f-opt" style="margin:4px 0 10px"><input type="checkbox" required> Погоджуюсь з <a href="privacy.html" style="color:var(--orange)">політикою конфіденційності</a></label>
    <button type="submit" class="btn btn-lg" style="width:100%">Надіслати заявку</button>
  </form>
  <div id="b2bThanks" style="display:none;text-align:center;padding:20px">
    <div style="font-size:48px">✓</div><h2>Дякуємо! Заявку отримано.</h2><p style="color:var(--muted)">Менеджер зв'яжеться з вами протягом робочого дня, уточнить деталі та підготує пропозицію під ваш формат.</p></div>
</div></div></section>
'''
    return layout('Кава для офісу та бізнесу — NPROMAX','Кава для офісу, кафе, ресторанів, HoReCa та вендингу. Ящики капсул, монодози, зерно 1 кг, регулярні поставки. Залиште заявку — NPROMAX.',body,active='kava-dlya-biznesu',canonical='kava-dlya-biznesu.html')

def cart_page():
    body='''
<div class="wrap"><div class="crumb"><a href="/">Головна</a><span>›</span>Кошик</div></div>
<div class="wrap" id="cartWrap"><h1 style="padding:16px 0">Кошик</h1>
<div class="cart-wrap"><div id="cartMain"><div id="cartItems"></div></div>
<div class="summary" id="cartSummary"><h3>Разом</h3>
  <div class="sum-row"><span id="sumCount">0 товарів</span><span id="sumSubtotal">0 ₴</span></div>
  <div class="sum-row"><span>Доставка</span><span>за тарифами Нової Пошти</span></div>
  <div class="sum-total"><span>До сплати</span><span id="sumTotal">0 ₴</span></div>
  <form onsubmit="submitOrder(event)" style="margin-top:20px">
    <div class="form-row"><label>Ім’я та прізвище *</label><input name="name" required placeholder="Отримувач"></div>
    <div class="form-row"><label>Телефон *</label><input name="phone" required type="tel" placeholder="+38 (0__) ___-__-__"></div>
    <div class="form-row"><label>Місто *</label><input name="city" required placeholder="Місто"></div>
    <div class="form-row"><label>Відділення / поштомат Нової Пошти *</label><input name="np" required placeholder="№ відділення або поштомата"></div>
    <div class="form-row"><label>Оплата</label><select name="payment"><option>При отриманні (накладений платіж)</option><option>За реквізитами (менеджер надішле рахунок)</option></select></div>
    <input type="text" name="_honey" style="display:none" tabindex="-1" autocomplete="off">
    <label class="f-opt" style="margin:2px 0 10px;font-size:13px"><input type="checkbox" required> Погоджуюсь з <a href="oferta.html" style="color:var(--orange)">офертою</a> та <a href="privacy.html" style="color:var(--orange)">політикою конфіденційності</a></label>
    <button type="submit" class="btn btn-lg" style="width:100%">Оформити замовлення</button>
  </form>
</div></div></div><div style="height:40px"></div>
'''
    return layout('Кошик — NPROMAX','Ваш кошик NPROMAX.',body,active='',canonical='cart.html')

# ---------- NPX-011: розширений пошуковий індекс ----------
# Латиниця для пошуку: схема «як шукають люди» (я→ya, ї→yi), НЕ slug-транслітерація (я→ia).
_LAT = {'а':'a','б':'b','в':'v','г':'h','ґ':'g','д':'d','е':'e','є':'ye','ж':'zh','з':'z',
 'и':'y','і':'i','ї':'yi','й':'y','к':'k','л':'l','м':'m','н':'n','о':'o','п':'p','р':'r',
 'с':'s','т':'t','у':'u','ф':'f','х':'kh','ц':'ts','ч':'ch','ш':'sh','щ':'shch','ь':'',
 'ю':'yu','я':'ya','ё':'e','ъ':'','ы':'y','э':'e'}
def lat(s):
    out=[]
    for ch in (s or '').lower():
        out.append(_LAT.get(ch, ch if (ch.isalnum() or ch.isspace()) else ' '))
    return re.sub(r'\s+',' ',''.join(out)).strip()

TYPE_TAGS = {
 'beans':  ['кава в зернах','зернова кава','зерно','кофе в зернах','зерновой','zerno','beans'],
 'ground': ['свіжомелена кава','мелена кава','помел','молотый кофе','melena','ground'],
 'ncap':   ['капсули','капсульна кава','сумісні з nespresso','nespresso','капсулы','kapsuly','capsules'],
 'dcap':   ['капсули','капсульна кава','сумісні з dolce gusto','dolce gusto','капсулы','kapsuly','capsules'],
 'ese':    ['монодози','чалди','e.s.e.','ese','44 мм','монодозы','чалды','monodozy'],
 'drink':  ['напої в капсулах','напій','капсули','напитки','napoyi'],
}
# Англійські назви країн: на сайті вони українською, але шукають і латиною.
COUNTRY_EN = {
 'ефіопія':'ethiopia','бразилія':'brazil','колумбія':'colombia','гватемала':'guatemala',
 'гондурас':'honduras','індія':'india','перу':'peru','уганда':'uganda',"в'єтнам":'vietnam',
 'кенія':'kenya','коста-ріка':'costa rica','мексика':'mexico','нікарагуа':'nicaragua',
 'панама':'panama','сальвадор':'salvador','танзанія':'tanzania','руанда':'rwanda','бурунді':'burundi',
}
CAT_TAGS = {
 'kava-v-zernakh':'кава в зернах','svizhomelena-kava':'свіжомелена кава',
 'kapsuly-nespresso':'капсули nespresso','kapsuly-dolce-gusto':'капсули dolce gusto',
 'napoyi-v-kapsulakh':'напої в капсулах','monodozy-ese':'монодози e.s.e.',
 'arabika-monosorty':'моносорт арабіка','aromatyzovana-kava':'ароматизована кава',
 'kavovi-kupazhi':'купаж','kava-bez-kofeinu':'без кофеїну','kava-dlya-biznesu':'для бізнесу опт',
}

def search_entry(card):
    """{s,t,i,sku,tags[],tr} — NPX-011. tr = латиниця назви+тегів для запитів на кшталт 'kenya'."""
    tags=set()
    for t in TYPE_TAGS.get(card['type'],[]): tags.add(t)
    for cat in card['cats']:
        if cat in CAT_TAGS: tags.add(CAT_TAGS[cat])
    if card['decaf']: tags.update(['без кофеїну','декаф','decaf','без кофеина'])
    if card['aroma']: tags.update(['ароматизована кава','aromatyzovana'])
    if card['monosort']: tags.update(['100% арабіка','моносорт','арабика','arabika','arabica'])
    if card['country']:
        c=card['country'].lower(); tags.add(c)
        if COUNTRY_EN.get(c): tags.add(COUNTRY_EN[c])
    if card['composition']: tags.add(card['composition'].lower())
    if 'робуста' in (card['composition'] or '').lower(): tags.add('robusta')
    # узагальнені синоніми: щоб «кофе»/«coffee» знаходили всю каву (напої — не кава)
    if card['type']!='drink': tags.update(['кава','кофе','coffee'])
    # смак ароматизованої — з лапок у назві («Амаретто», "Ром, Ваніль")
    for m in re.findall(r'[«"]([^»"]{2,40})[»"]', card['title']):
        for part in re.split(r'[,/]', m):
            part=part.strip().lower()
            if part: tags.add(part)
    tags.add('npromax')
    tags={t for t in tags if t}
    skus=[v['sku'] for v in card['variants'] if v.get('sku')]
    # tr = латиниця лише НАЗВИ: латинські синоніми тегів уже лежать у tags,
    # тож дублювати їх транслітерацію в кожній картці немає сенсу (індекс важить менше).
    return {'s':card['slug'],'t':card['title'],'i':card['image'],
            'sku':card['vendor_code'] or '','skus':skus,
            'tags':sorted(tags),'tr':lat(card['title'])}

# ---------- NPX-032/033: лендінги оренди POLTI (біла/чорна) ----------
# Оффер (нові умови власника 22.07.2026): 0 грн/міс за купівлі від 600 чалдів E.S.E./міс, інакше 1000 грн/міс.
RENT_FREE_CHALDS=600
RENT_FEE=1000
RENT_COLORS={
 'bila':{'name':'біла','acc':'білу','model':'POLTI Coffea S18W','url':'orenda-kavomashyny-polti-bila.html','img':'assets/img/polti-bila.jpg','photo':True,'npx':'NPX-032'},
 'chorna':{'name':'чорна','acc':'чорну','model':'POLTI Coffea S15B','url':'orenda-kavomashyny-polti-chorna.html','img':'assets/img/polti-chorna.jpg','photo':True,'npx':'NPX-033'},
}
POLTI_SPECS=[
 ('Сумісність','Чалди E.S.E. 44 мм (паперові монодози)'),
 ('Тиск помпи','19 бар'),
 ('Режими','Еспресо / подовжена кава'),
 ('Налаштування','Програмування об’єму, 3 рівні температури'),
 ('Контейнер для чалд','Автоскид, ~10 шт'),
 ('Резервуар для води','0,85 л, знімний'),
 ('Автовимкнення','через 25 хв'),
 ('Час нагріву','≈1 хв'),
 ('Розміри (Ш×Г×В)','10,5 × 35 × 23 см'),
 ('Вага','≈2,9 кг'),
]
RENT_SEGMENTS=['Офіс','Кафе та кав’ярні','Магазин','Салон краси','Барбершоп','Автомийка / СТО','Готель, апартаменти','Приймальня, переговорна','Шоурум']
def rent_faq(decaf_link):
    return [
 ('Що таке чалда E.S.E. 44 мм?','Це готова порція меленої кави, спресована у паперовому фільтрі стандарту E.S.E. (Easy Serving Espresso). Вставляєте в машину — і за секунди отримуєте еспресо з пінкою, без кавомолки, темпера й прибирання гущі.'),
 ('Чи підходять капсули Nespresso, Dolce Gusto, Lavazza?','Ні. POLTI Coffea S18 працює лише зі стандартними паперовими чалдами E.S.E. 44 мм. Капсульні системи не сумісні.'),
 ('Що буде, якщо за місяць куплю менше 600 чалдів?','Тоді оренда апарата — 1000 грн за цей місяць. Щойно закупівля знову досягає 600 чалдів на місяць — оренда безкоштовна.'),
 ('Скільки чашок дає одна чалда?','Одна чалда — одна порція кави. 600 чалдів на місяць — це приблизно 20 чашок на день.'),
 ('Чи є кава без кофеїну?','Так, серед монодоз E.S.E. NPROMAX є варіант без кофеїну — <a href="'+decaf_link+'" style="color:var(--orange)">дивіться в каталозі</a>.'),
 ('Кому належить машина?','Апарат залишається власністю NPROMAX — це оренда, а не продаж. Укладається договір оренди; умови передачі, доставки й обслуговування узгоджує менеджер.'),
 ('Хто платить за доставку і обслуговування?','Умови доставки апарата й сервісу узгоджуються індивідуально та фіксуються в договорі оренди — залиште заявку, менеджер розкаже деталі.'),
 ('Чи можна викупити апарат?','Умови викупу уточнюйте в менеджера при оформленні.'),
]

def _rent_form(color_key):
    """Форма заявки з передзаповненим кольором + приховані UTM/fbclid поля."""
    utm=''.join(f'<input type="hidden" name="{k}" id="f_{k}">' for k in ['utm_source','utm_medium','utm_campaign','utm_content','utm_term','fbclid'])
    return f'''<form onsubmit="submitRental(event)" class="rentalForm" data-color="{color_key}">
  <input type="hidden" name="color" value="{color_key}">
  {utm}
  <div class="form-row"><label>Ім’я *</label><input name="name" required placeholder="Ваше ім’я"></div>
  <div class="form-row"><label>Телефон *</label><input name="phone" required type="tel" inputmode="tel" placeholder="+38 (0__) ___-__-__"></div>
  <div class="form-row"><label>Тип закладу</label><select name="place"><option>Офіс</option><option>Кафе / кав’ярня</option><option>Магазин</option><option>Салон краси / барбершоп</option><option>Автомийка / СТО</option><option>Готель / апартаменти</option><option>Інше</option></select></div>
  <div class="form-row"><label>Місто</label><input name="city" placeholder="Місто"></div>
  <div class="form-row"><label>Орієнтовно чашок на день</label><input name="cups" inputmode="numeric" placeholder="Напр. 20"></div>
  <div class="form-row"><label>Коментар</label><textarea name="comment" rows="2" placeholder="Питання чи побажання"></textarea></div>
  <input type="text" name="_honey" style="display:none" tabindex="-1" autocomplete="off">
  <label class="f-opt" style="margin:4px 0 10px"><input type="checkbox" required> Погоджуюсь з <a href="privacy.html" style="color:var(--orange)">політикою конфіденційності</a></label>
  <button type="submit" class="btn btn-lg" style="width:100%">Отримати безкоштовну кавомашину</button>
</form>'''

CONTACTS = {
    'email':'info@npromax.com.ua',
    'phone_display':'+38 (097) 575-16-47',   # напр. '+38 (097) 000-00-00' — БЕЗ підтвердження власника не заповнювати
    'phone_tel':'+380975751647',       # напр. '+380970000000'
    'viber':'viber://chat?number=%2B380975751647', 'telegram':'', 'whatsapp':'',  # посилання; пусто = не показувати
}

def _rent_form_hub():
    """Форма хабу: видимий вибір кольору + приховані UTM/fbclid."""
    utm=''.join(f'<input type="hidden" name="{k}" id="fh_{k}">' for k in ['utm_source','utm_medium','utm_campaign','utm_content','utm_term','fbclid'])
    return f'''<form onsubmit="submitRental(event)" class="rentalForm">
  {utm}
  <div class="form-row"><label>Ім’я *</label><input name="name" required placeholder="Ваше ім’я"></div>
  <div class="form-row"><label>Телефон *</label><input name="phone" required type="tel" inputmode="tel" placeholder="+38 (0__) ___-__-__"></div>
  <div class="form-row"><label>Колір кавомашини</label>
    <div class="clr-pick">
      <label><input type="radio" name="color" value="bila" checked> Біла (S18W)</label>
      <label><input type="radio" name="color" value="chorna"> Чорна (S18B)</label>
    </div></div>
  <div class="form-row"><label>Тип закладу</label><select name="place"><option>Дім</option><option>Офіс</option><option>Кафе / кав’ярня</option><option>Магазин</option><option>Салон краси / барбершоп</option><option>Інше</option></select></div>
  <div class="form-row"><label>Місто</label><input name="city" placeholder="Місто"></div>
  <div class="form-row"><label>Орієнтовно чашок на день</label><input name="cups" inputmode="numeric" placeholder="Напр. 20"></div>
  <input type="text" name="_honey" style="display:none" tabindex="-1" autocomplete="off">
  <label class="f-opt" style="margin:4px 0 10px"><input type="checkbox" required> Погоджуюсь з <a href="privacy.html" style="color:var(--orange)">політикою конфіденційності</a></label>
  <button type="submit" class="btn btn-lg" style="width:100%">Отримати кавомашину</button>
</form>'''

def rental_landing(ckey, cards):
    c=RENT_COLORS[ckey]; B='https://www.npromax.com.ua/'
    ese=[x for x in cards if x['type']=='ese'][:5]
    chalds=''.join(card_html(x) for x in ese)
    decaf=next((x for x in ese if x['decaf']), None)
    decaf_link=('p-'+decaf['slug']+'.html') if decaf else 'monodozy-ese.html'
    # #3: «грн за чашку» з реальних цін монодоз E.S.E. на сайті
    per=[]
    for x in ese:
        q=x['params'].get('Количество в упаковке (шт.)') or x['params'].get('Количество в упаковке')
        if q and str(q).isdigit() and int(q)>0 and x['price_min']:
            per.append(x['price_min']/int(q))
    from_cup=int(round(min(per))) if per else None
    cup_note=(f'Кава — <b>від ~{from_cup} грн за чашку</b>. ' if from_cup else '')
    # фото машини (біла — оброблене реальне; чорна поки плейсхолдер)
    if c.get('photo'):
        photo_html=(f'<picture><source srcset="assets/img/polti-{ckey}.webp" type="image/webp">'
          f'<img src="assets/img/polti-{ckey}.jpg" alt="Кавомашина {esc(c["model"])} ({c["name"]}) для чалдів E.S.E." '
          f'class="lp-photo" width="900" height="900" fetchpriority="high"></picture>')
    else:
        photo_html=f'<div class="lp-photo-ph" data-color="{c["name"]}"><span>Фото {c["model"]} ({c["name"]}) — додається</span></div>'
    specs_html=''.join('<div class="spec-cell"><span>%s</span><b>%s</b></div>'%(esc(k),esc(v)) for k,v in POLTI_SPECS)
    seg_html=''.join('<div class="seg">%s</div>'%esc(s) for s in RENT_SEGMENTS)
    faq_items=rent_faq(decaf_link)
    faq_html=''.join('<details><summary>%s</summary><p>%s</p></details>'%(esc(q),a) for q,a in faq_items)
    prod_ld=json.dumps({"@context":"https://schema.org","@type":"Product",
      "name":"Оренда кавомашини "+c['model']+" ("+c['name']+")","image":B+c['img'],
      "brand":{"@type":"Brand","name":"POLTI"},"category":"Оренда кавомашини",
      "description":"Безкоштовна оренда кавомашини "+c['model']+" під чалди E.S.E. 44 мм за умови купівлі від 600 чалдів E.S.E. на місяць; інакше 1000 грн/міс. Апарат лишається власністю NPROMAX (договір оренди).",
      "offers":{"@type":"Offer","priceCurrency":"UAH","price":1000,"url":B+c['url'],
        "availability":"https://schema.org/InStock","itemCondition":"https://schema.org/NewCondition",
        "description":"1000 грн/міс або 0 грн/міс за умови купівлі від 600 чалдів E.S.E. на місяць"}},ensure_ascii=False)
    faq_ld=json.dumps({"@context":"https://schema.org","@type":"FAQPage","mainEntity":[
      {"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":re.sub('<[^>]+>','',a)}} for q,a in faq_items]},ensure_ascii=False)
    crumbs=crumb_ld([('Головна',''),('Кава для бізнесу','kava-dlya-biznesu.html'),('Оренда POLTI '+c['name'], c['url'])])
    body=f'''
<script type="application/ld+json">{prod_ld}</script>
<script type="application/ld+json">{faq_ld}</script>
{crumbs}
<section class="lp-hero"><div class="wrap lp-hero-in">
  <div class="lp-hero-txt">
    <h1>Безкоштовна кавомашина POLTI для вашого офісу та бізнесу</h1>
    <p class="lp-sub">Ви платите лише за каву. Купуєте від <b>600 чалдів E.S.E.</b> на місяць — апарат <b>{c['name']}</b> POLTI працює у вас <b>безкоштовно</b>.</p>
    <div class="lp-cta"><a href="#zayavka" class="btn btn-lg">Залишити заявку</a><a href="#how" class="btn btn-ghost btn-lg">Як це працює</a></div>
    <div class="lp-badges">{ICON['check']}Договір оренди · {ICON['truck']}Доставка по Україні · {ICON['check']}Чалди E.S.E. в наявності</div>
  </div>
  <div class="lp-hero-vis">
    {photo_html}
    <div class="lp-offer-badge"><span class="lp-0">0<small>грн/міс</small></span><span class="lp-cond">від 600 чалдів E.S.E.</span></div>
  </div>
</div></section>

<section class="section"><div class="wrap">
  <div class="offer-grid">
    <div class="offer-tile offer-hi"><div class="offer-big">0 грн<small>/міс</small></div><p>Купуєте <b>від 600 чалдів E.S.E.</b> на місяць — оренда апарата безкоштовна.</p></div>
    <div class="offer-tile"><div class="offer-big">1000 грн<small>/міс</small></div><p>Якщо за місяць придбано <b>менше 600 чалдів</b> — оренда 1000 грн.</p></div>
    <div class="offer-tile"><div class="offer-ic">{ICON['shield']}</div><p><b>Машина — наша, кава — ваша.</b> Договір оренди + доставка по Україні.</p></div>
  </div>
</div></section>

<section class="section" id="how" style="background:var(--crema)"><div class="wrap">
  <div class="section-h"><h2>Як це працює</h2><div class="sub">Від заявки до першої чашки — 4 кроки</div></div>
  <div class="steps">
    <div class="step"><span class="step-n">1</span><h3>Обираєте колір</h3><p>Біла або чорна POLTI Coffea S18 — під ваш інтер’єр.</p></div>
    <div class="step"><span class="step-n">2</span><h3>Залишаєте заявку</h3><p>Ім’я і телефон — менеджер передзвонить у робочий день.</p></div>
    <div class="step"><span class="step-n">3</span><h3>Узгоджуємо умови</h3><p>Обсяг чалдів, доставку й договір оренди.</p></div>
    <div class="step"><span class="step-n">4</span><h3>Отримуєте машину</h3><p>Ставите на місце і замовляєте чалди E.S.E. — все.</p></div>
  </div>
</div></section>

<section class="section"><div class="wrap">
  <div class="section-h"><h2>Проста економіка</h2><div class="sub">600 чалдів на місяць ≈ 20 чашок на день — це маленький офіс чи заклад</div></div>
  <div class="calc">
    <label>Скільки чашок кави п’єте на день?</label>
    <input type="range" id="rcCups" min="1" max="60" value="20" oninput="rentCalc()">
    <div class="calc-out"><div><span id="rcCupsV">20</span> чашок/день · <span id="rcChalds">600</span> чалдів/міс</div>
    <div class="rc-status rc-free" id="rcStatus">Безкоштовно — 0 грн/міс</div></div>
    <p class="calc-note">{cup_note}Замість купівлі власної кавомашини — 0 грн оренди за умови закупівлі кави, яку ви й так п’єте.</p>
  </div>
</div></section>

<section class="section" style="background:var(--soft)"><div class="wrap">
  <div class="section-h"><h2>Характеристики POLTI Coffea S18{'W' if ckey=='bila' else 'B'}</h2><div class="sub">Компактна, вузька (лише 10,5 см), проста в користуванні</div></div>
  <div class="spec-grid">{specs_html}</div>
</div></section>

<section class="section"><div class="wrap">
  <div class="section-h row"><div><h2>Сумісні чалди E.S.E. 44 мм</h2><div class="sub">Саме на цій каві машина працює безкоштовно</div></div><a href="monodozy-ese.html" class="more">Усі монодози {ICON['arrow']}</a></div>
  <div class="grid">{chalds}</div>
  <div style="text-align:center;margin-top:20px"><a href="monodozy-ese.html" class="btn btn-outline btn-lg">Обрати чалди E.S.E.</a></div>
</div></section>

<section class="section" style="background:var(--crema)"><div class="wrap">
  <div class="section-h"><h2>Кому підходить</h2><div class="sub">Скрізь, де п’ють від ~20 чашок кави на день</div></div>
  <div class="seg-grid">{seg_html}</div>
</div></section>

<section class="section"><div class="wrap"><div class="b2b-band">
  <div class="b2b-txt"><div class="kicker">ДОВІРА</div><h2>4 400+ відгуків на Prom.ua</h2>
  <p>Власне обсмаження та фасування кави NPROMAX. Договір оренди, доставка Новою Поштою по всій Україні.</p></div>
  <a href="https://npro.prom.ua" rel="nofollow" class="btn btn-lg">Відгуки на Prom</a>
</div></div></section>

<section class="section" style="padding-top:0"><div class="wrap" style="max-width:820px">
  <div class="section-h"><h2>Часті питання</h2></div>
  <div class="faq">{faq_html}</div>
</div></section>

<section class="section" id="zayavka" style="background:var(--espresso)"><div class="wrap" style="max-width:620px">
  <div class="lp-form-h"><h2>Отримайте безкоштовну кавомашину POLTI ({c['name']})</h2>
  <p>Залиште заявку — менеджер зв’яжеться, узгодить умови й договір. Ви платите лише за каву.</p></div>
  {_rent_form(ckey)}
</div></section>
<div class="lp-sticky"><span><b>0 грн/міс</b> · POLTI {c['name']}</span><a href="#zayavka" class="btn">Залишити заявку</a></div>
<div style="height:10px"></div>
'''
    title=f"Безкоштовна оренда кавомашини POLTI ({c['name']}) для чалдів E.S.E. — NPROMAX"
    desc=f"Безкоштовна кавомашина POLTI Coffea S18 ({c['name']}) для офісу та бізнесу: від 600 чалдів E.S.E. на місяць — 0 грн/міс оренди, інакше 1000 грн. Договір, доставка по Україні."
    return layout(title, desc, body, active='kava-dlya-biznesu', canonical=c['url'])

HUB_FAQ_BASE=[
 ('Що таке чалда E.S.E. 44 мм?','Чалда E.S.E. (Easy Serving Espresso) — це готова порція меленої кави, спресована у паперовому фільтрі діаметром 44 мм. Ви просто вставляєте її в машину й отримуєте еспресо з пінкою за секунди — без кавомолки, темпера та прибирання гущі.'),
 ('Скільки коштує оренда кавомашини?','0 грн/міс, якщо ви купуєте у NPROMAX від 600 чалдів E.S.E. на місяць. Якщо менше 600 — оренда 1000 грн/міс. Ви платите лише за каву, яку й так п’єте.'),
 ('Що буде, якщо за місяць куплю менше 600 чалдів?','За цей місяць оренда складе 1000 грн. Наступного місяця, коли закупівля знову досягне 600 чалдів, — оренда знову безкоштовна.'),
 ('600 чалдів — це багато?','Ні. 600 чалдів на місяць — це приблизно 20 чашок кави на день. Стільки випиває невеликий офіс, кав’ярня-куточок, салон чи магазин.'),
 ('Кому належить кавомашина?','Апарат залишається власністю NPROMAX — це оренда, а не продаж. На передачу укладається договір оренди.'),
 ('Скільки чашок дає одна чалда?','Одна чалда — одна порція кави (еспресо або подовжена).'),
 ('Чи є кава без кофеїну?','Так, серед монодоз E.S.E. NPROMAX є варіант без кофеїну — <a href="'+'DECAF'+'" style="color:var(--orange)">дивіться в асортименті</a>.'),
 ('Чи підходять капсули Nespresso, Dolce Gusto, Lavazza?','Ні. Кавомашина працює лише зі стандартними паперовими чалдами E.S.E. 44 мм. Капсульні системи не сумісні.'),
 ('Чи складно користуватися машиною?','Ні. Вставили чалду — натиснули кнопку — отримали каву. Впорається будь-хто, спеціальних навичок не потрібно.'),
 ('Чи потрібна кавомолка?','Ні. У чалді вже відміряна й спресована мелена кава.'),
 ('Скільки готується чашка кави?','Машина нагрівається приблизно за хвилину, а сама чашка готується за секунди.'),
 ('Скільки місця займає апарат?','Дуже мало — корпус завширшки лише 10,5 см. Габарити 10,5 × 35 × 23 см, вага ≈2,9 кг. Поміститься навіть на вузькій поличці.'),
 ('Який колір можна обрати?','POLTI Coffea S18 доступна у двох кольорах — біла (S18W) і чорна (S18B). Оберіть у формі заявки.'),
 ('Хто платить за доставку і обслуговування?','Умови доставки апарата та сервісу узгоджуються індивідуально й фіксуються в договорі оренди. Залиште заявку — менеджер розкаже деталі під ваш формат.'),
 ('Чи можна продовжити оренду?','Так. Поки ви замовляєте каву — машина працює у вас. Умови продовження узгоджуються з менеджером.'),
 ('Де можна користуватися машиною?','Вдома, в офісі, салоні краси, магазині, шоурумі, приймальні, кабінеті — скрізь, де п’ють від ~20 чашок кави на день.'),
 ('Як залишити заявку?','Натисніть «Отримати кавомашину», заповніть ім’я і телефон — менеджер зв’яжеться з вами протягом робочого дня, узгодить умови й договір.'),
]

RENTAL_JS = r'''
<script>
(function(){
  var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target);}});},{threshold:.12,rootMargin:'0px 0px -40px 0px'});
  document.querySelectorAll('.reveal').forEach(function(el){io.observe(el);});
  var c=document.getElementById('rhCalc'); if(!c)return;
  var r=document.getElementById('rhCups'),cupsEl=document.getElementById('rhCupsVal'),
      chEl=document.getElementById('rhChalds'),rentEl=document.getElementById('rhRent'),
      coffeeEl=document.getElementById('rhCoffee'),badge=document.getElementById('rhBadge');
  var perCup=parseFloat(c.dataset.percup)||0,thr=parseInt(c.dataset.threshold)||600,rent=parseInt(c.dataset.rent)||1000;
  function fmt(n){return n.toLocaleString('uk-UA');}
  function upd(){
    var cups=parseInt(r.value),ch=cups*30,free=ch>=thr;
    cupsEl.textContent=cups; chEl.textContent=fmt(ch);
    rentEl.textContent=free?'0 ₴':fmt(rent)+' ₴'; rentEl.className=free?'co-free':'';
    coffeeEl.textContent=perCup?('≈ '+fmt(Math.round(ch*perCup))+' ₴'):'—';
    badge.className='co-badge '+(free?'free':'paid');
    badge.textContent=free?'✓ Оренда безкоштовна':('Оренда '+fmt(rent)+' ₴/міс');
  }
  r.addEventListener('input',upd); upd();
})();
window.rhPlay=function(el){el.innerHTML='<iframe src="https://www.youtube.com/embed/'+el.dataset.id+'?autoplay=1&rel=0" title="POLTI Coffea" allow="autoplay; encrypted-media; fullscreen" allowfullscreen></iframe>';};
</script>
'''

def rental_hub(cards):
    B='https://www.npromax.com.ua/'
    ese=[x for x in cards if x['type']=='ese'][:5]
    decaf=next((x for x in ese if x['decaf']), None)
    decaf_link=('p-'+decaf['slug']+'.html') if decaf else 'monodozy-ese.html'
    def per_cup(x):
        q=x['params'].get('Количество в упаковке (шт.)') or x['params'].get('Количество в упаковке')
        try: return x['price_min']/int(q) if (q and int(q)>0 and x['price_min']) else None
        except Exception: return None
    percs=[p for p in (per_cup(x) for x in ese) if p]
    from_cup=int(round(min(percs))) if percs else None
    # ---- асортимент чалдів (реальні фото товарів) ----
    def chald_card(x):
        q=x['params'].get('Количество в упаковке (шт.)') or x['params'].get('Количество в упаковке') or ''
        pc=per_cup(x); pc_s=('≈ %.1f грн/чашка'%pc).replace('.',',') if pc else ''
        nm=x['title'].replace('Кава в монодозах NPROMAX ','').split(' стандарту')[0].split(' аромат')[0].strip()
        return ('<a class="chald-card" href="p-%s.html">'
          '<div class="chald-img"><img src="%s" alt="Монодози E.S.E. NPROMAX %s" loading="lazy" width="320" height="320"></div>'
          '<div class="chald-b"><b>%s</b><span class="chald-q">%s шт · %s ₴</span>%s</div></a>') % (
          esc(x['slug']), esc(x['image']), esc(nm), esc(nm), esc(str(q)), money(x['price_min']),
          ('<span class="chald-pc">%s</span>'%pc_s if pc_s else ''))
    chalds_html=''.join(chald_card(x) for x in ese)
    specs_html=''.join('<div class="spec-cell"><span>%s</span><b>%s</b></div>'%(esc(k),esc(v)) for k,v in POLTI_SPECS)
    faq_items=[(q, a.replace('DECAF',decaf_link)) for q,a in HUB_FAQ_BASE]
    faq_html=''.join('<details><summary>%s</summary><p>%s</p></details>'%(esc(q),a) for q,a in faq_items)
    cup_line=(' · від ~%d грн за чашку'%from_cup) if from_cup else ''
    # ---- schema ----
    svc_ld=json.dumps({"@context":"https://schema.org","@type":"Service",
      "name":"Оренда кавомашини POLTI Coffea S18 для чалдів E.S.E.","serviceType":"Оренда кавомашини",
      "provider":{"@type":"Organization","name":"NPROMAX","url":B},"areaServed":{"@type":"Country","name":"Україна"},
      "image":B+"assets/img/polti-bila.jpg",
      "description":"Безкоштовна оренда кавомашини POLTI Coffea S18 за умови купівлі від 600 чалдів E.S.E. на місяць; інакше 1000 грн/міс. Апарат лишається власністю NPROMAX (договір оренди).",
      "offers":{"@type":"Offer","priceCurrency":"UAH","price":1000,"url":B+"orenda-kavomashyny.html",
        "description":"0 грн/міс від 600 чалдів E.S.E. на місяць, інакше 1000 грн/міс"}},ensure_ascii=False)
    faq_ld=json.dumps({"@context":"https://schema.org","@type":"FAQPage","mainEntity":[
      {"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":re.sub('<[^>]+>','',a)}} for q,a in faq_items]},ensure_ascii=False)
    crumbs=crumb_ld([('Головна',''),('Кава для бізнесу','kava-dlya-biznesu.html'),('Оренда кавомашини','orenda-kavomashyny.html')])

    # ---- іконки для преміум-блоків ----
    def _svg(p): return '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">'+p+'</svg>'
    FEAT = [
        (_svg('<rect x="6" y="3" width="12" height="18" rx="2"/><line x1="6" y1="8" x2="18" y2="8"/>'),'Компактна','10,5 см завширшки'),
        (_svg('<path d="M12 3l2.4 4.9 5.4.8-3.9 3.8.9 5.4L12 15.9 7.2 18.7l.9-5.4-3.9-3.8 5.4-.8z"/>'),'Стильний дизайн','Сучасний вигляд, який пасує інтер’єру'),
        (_svg('<path d="M13 2L4 14h6l-1 8 9-12h-6z"/>'),'Швидке нагрівання','Готова за секунди'),
        (_svg('<circle cx="12" cy="12" r="8"/><circle cx="12" cy="12" r="2.6" fill="currentColor" stroke="none"/>'),'Проста у користуванні','Одна кнопка'),
        (_svg('<circle cx="12" cy="12" r="8"/><circle cx="12" cy="12" r="3"/>'),'Працює на чалдах E.S.E.','Стандарт 44 мм'),
        (_svg('<path d="M12 3s6 5.6 6 10a6 6 0 0 1-12 0c0-4.4 6-10 6-10z"/>'),'Мінімальний догляд','Чалда сама в контейнер'),
        (_svg('<path d="M4 8h12v5a5 5 0 0 1-5 5H9a5 5 0 0 1-5-5z"/><path d="M16 9h2.2a2 2 0 0 1 0 5H16"/><path d="M7 3v2M11 3v2"/>'),'Ідеальна кава щоразу','Щільна пінка щоразу'),
    ]
    feat_html=''.join('<div class="ft"><div class="ft-ic">%s</div><b>%s</b><span>%s</span></div>'%(ic,t,d) for ic,t,d in FEAT)
    GALLERY=[('polti-bila-a','Кавомашина POLTI Coffea S18W (біла) — вигляд збоку'),
             ('polti-bila-b','Кавомашина POLTI Coffea S18W (біла) — верхня частина'),
             ('polti-chorna','Кавомашина POLTI Coffea S15B (чорна) — фронт із логотипом Coffea'),
             ('polti-chorna-a','Кавомашина POLTI Coffea S15B (чорна) — вигляд 3/4'),
             ('polti-chorna-b','Кавомашина POLTI Coffea S15B (чорна) — панель керування зверху')]
    gallery_html=''.join('<a href="assets/img/%s.jpg" target="_blank" rel="noopener"><picture><source srcset="assets/img/%s.webp" type="image/webp"><img src="assets/img/%s.jpg" alt="%s" loading="lazy" width="562" height="1000"></picture></a>'%(b,b,b,esc(a)) for b,a in GALLERY)

    SEG = [('Офіс',_svg('<path d="M4 21V5a1 1 0 0 1 1-1h9a1 1 0 0 1 1 1v16"/><path d="M15 9h4a1 1 0 0 1 1 1v11"/><line x1="2" y1="21" x2="22" y2="21"/><line x1="8" y1="8" x2="8" y2="8"/><line x1="11" y1="8" x2="11" y2="8"/>')),
        ('Салон краси',_svg('<circle cx="6" cy="6" r="3"/><circle cx="6" cy="18" r="3"/><line x1="20" y1="4" x2="8.1" y2="15.9"/><line x1="8.1" y1="8.1" x2="20" y2="20"/>')),
        ('Магазин',_svg('<path d="M3 9l1-5h16l1 5"/><path d="M4 9v11h16V9"/><path d="M3 9h18"/>')),
        ('Шоурум',_svg('<rect x="3" y="4" width="18" height="13" rx="1"/><line x1="7" y1="21" x2="17" y2="21"/><line x1="12" y1="17" x2="12" y2="21"/>')),
        ('Стоматологія',_svg('<path d="M12 3c-3 0-5 1.6-5 4 0 3 1 4 1.4 7 .3 2 .6 5 1.6 5s1-3 2-3 1 3 2 3 1.3-3 1.6-5c.4-3 1.4-4 1.4-7 0-2.4-2-4-5-4z"/>')),
        ('Квартира',_svg('<path d="M3 11l9-7 9 7"/><path d="M5 10v10h14V10"/><rect x="10" y="14" width="4" height="6"/>')),
        ('Приватний будинок',_svg('<path d="M3 21h18M5 21V8l7-5 7 5v13"/><rect x="10" y="14" width="4" height="7"/>')),
    ]
    seg_html=''.join('<div class="sg">%s<span>%s</span></div>'%(ic,t) for t,ic in SEG)

    WHY = [
        (ICON['shield'],'Офіційна компанія','Власне обсмаження та фасування кави NPROMAX'),
        (ICON['truck'],'Швидка доставка','Новою Поштою по всій Україні'),
        (ICON['shield'],'Гарантія','Обслуговуємо апарат'),
        (ICON['refresh'],'Сервіс і заміна','Заміна при несправності'),
        (ICON['phone'],'Консультація і підбір','Підбір кави під вас'),
        (ICON['star'],'Великий вибір чалд E.S.E.','Класика, ароматизовані, без кофеїну'),
        (ICON['check'],'Постійна наявність','Кава завжди на складі'),
    ]
    why_html=''.join('<div class="rh-w"><div class="rh-w-ic">%s</div><div><b>%s</b><span>%s</span></div></div>'%(ic,t,d) for ic,t,d in WHY)

    # ---- контакти (телефон/месенджери — лише якщо заповнені у CONTACTS) ----
    ct=CONTACTS
    _rows=''
    if ct.get('phone_tel'):
        _rows+='<a class="rh-ct" href="tel:%s">%s<span>%s</span></a>'%(ct['phone_tel'],ICON['phone'],esc(ct['phone_display'] or ct['phone_tel']))
    _rows+='<a class="rh-ct" href="mailto:%s">%s<span>%s</span></a>'%(ct['email'],'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 6 9-6"/></svg>',ct['email'])
    _bubble='<svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 3C6.9 3 3 6.4 3 10.6c0 2.4 1.3 4.5 3.3 5.9-.1 1.1-.6 2.3-1.3 3.1-.2.2 0 .5.3.5 1.7-.2 3.2-.9 4.3-1.7.7.1 1.4.2 2.1.2 5.1 0 9-3.4 9-7.6S17.1 3 12 3z"/></svg>'
    _msgs=''
    if ct.get('viber'):    _msgs+='<a class="rh-msg viber" href="%s" rel="nofollow">%sViber</a>'%(ct['viber'],_bubble)
    if ct.get('telegram'): _msgs+='<a class="rh-msg tg" href="%s" rel="nofollow">%sTelegram</a>'%(ct['telegram'],_bubble)
    if ct.get('whatsapp'): _msgs+='<a class="rh-msg wa" href="%s" rel="nofollow">%sWhatsApp</a>'%(ct['whatsapp'],_bubble)
    msgs_html=('<div class="rh-msgs">%s</div>'%_msgs) if _msgs else ''
    contact_html='<div class="rh-contacts">%s%s</div>'%(_rows,msgs_html)

    body=f'''
<script type="application/ld+json">{svc_ld}</script>
<script type="application/ld+json">{faq_ld}</script>
{crumbs}

<section class="rh-hero"><div class="rh-hero-in">
  <div class="rh-hero-txt">
    <div class="rh-eyebrow">POLTI COFFEA · ЧАЛДИ E.S.E. 44 ММ</div>
    <h1>Оренда нової кавомашини — <span class="hl">від 1000 ₴/міс</span> або <span class="hl">безкоштовно</span></h1>
    <p class="rh-lead">Ви платите лише за каву, яку й так п’єте.</p>
    <div class="rh-fire">🔥&nbsp;<span>Від <b>600 чалдів E.S.E. на місяць</b> — оренда кавомашини <b>безкоштовна</b>.</span></div>
    <div class="rh-herocta">
      <a href="#zayavka" class="btn btn-lg">Отримати консультацію</a>
      <a href="#tarify" class="btn btn-ghost btn-lg">Два тарифи</a>
    </div>
    <div class="rh-trust"><span>{ICON['check']}Нова машина</span><span>{ICON['truck']}Доставка по Україні</span><span>{ICON['shield']}Договір оренди</span></div>
  </div>
  <div class="rh-hero-vis">
    <div class="rh-frame">
      <picture><source srcset="assets/img/polti-bila.webp" type="image/webp"><img src="assets/img/polti-bila.jpg" alt="Кавомашина POLTI Coffea S18 для чалдів E.S.E." width="900" height="900" fetchpriority="high"></picture>
      <div class="rh-chip"><span class="p0">0<small> ₴/міс</small></span><span class="pc">від 600 чалдів E.S.E.</span></div>
    </div>
  </div>
</div></section>

<section class="rh-sec" id="tarify"><div class="rh-wrap reveal">
  <div class="rh-head"><div class="rh-kicker">ДВІ УМОВИ СПІВПРАЦІ</div><h2>Оберіть свій тариф</h2><div class="rh-hsub">Та сама машина. Різниця — в обсязі кави.</div></div>
  <div class="rh-tiers">
    <div class="rh-tier best">
      <div class="rh-ribbon">НАЙВИГІДНІШЕ</div>
      <div class="t-name">ВАРІАНТ 1</div>
      <div class="t-price">0 ₴<small> /міс оренди</small></div>
      <p class="t-lead">Безкоштовна оренда за умови купівлі <b>від 600 чалдів E.S.E.</b> щомісяця.</p>
      <div class="rh-flow">
        <div class="fl">{ICON['check']}<span>Отримуєте нову кавомашину POLTI</span></div>
        <div class="fl">{ICON['check']}<span>Замовляєте від 600 чалдів щомісяця</span></div>
        <div class="fl fin">{ICON['check']}<span>Користуєтесь машиною безкоштовно</span></div>
      </div>
      <a href="#zayavka" class="btn btn-lg">Отримати безкоштовно</a>
    </div>
    <div class="rh-tier">
      <div class="t-name">ВАРІАНТ 2</div>
      <div class="t-price">1000 ₴<small> /міс оренди</small></div>
      <p class="t-lead">Якщо потрібно <b>менше ніж 600 чалдів</b> на місяць — фіксована оренда апарата.</p>
      <ul class="rh-tlist">
        <li>{ICON['check']}Та сама нова кавомашина POLTI</li>
        <li>{ICON['check']}Без зобов’язань щодо обсягу кави</li>
        <li>{ICON['check']}Перехід на безкоштовний тариф будь-коли</li>
      </ul>
      <a href="#zayavka" class="btn btn-outline btn-lg">Замовити кавомашину</a>
    </div>
  </div>
</div></section>

<section class="rh-sec" style="background:var(--soft)"><div class="rh-wrap reveal">
  <div class="rh-head"><div class="rh-kicker">ВИГІДНО</div><h2>Чому оренда вигідніша за покупку</h2><div class="rh-hsub">Без вкладень у техніку.</div></div>
  <div class="rh-vs">
    <div class="vs-col vs-rent">
      <h3>{ICON['check']} Оренда з NPRO MAX</h3>
      <ul>
        <li>{ICON['check']}Не потрібно вкладати десятки тисяч гривень одразу</li>
        <li>{ICON['check']}Обслуговування та підтримка — на нас</li>
        <li>{ICON['check']}Заміна апарата при несправності</li>
        <li>{ICON['check']}Завжди сучасна, справна кавомашина</li>
        <li>{ICON['check']}0 ₴/міс за умови купівлі від 600 чалдів</li>
      </ul>
    </div>
    <div class="vs-col vs-buy">
      <h3>Купівля апарата</h3>
      <ul>
        <li>Десятки тисяч гривень одразу «заморожені» в техніці</li>
        <li>Гарантійний ремонт і сервіс — ваш клопіт</li>
        <li>Ризик, що модель застаріє</li>
        <li>Простій у роботі, поки апарат у ремонті</li>
      </ul>
    </div>
  </div>

  <div class="rh-calc" id="rhCalc" data-percup="{from_cup or 0}" data-threshold="600" data-rent="1000">
    <div>
      <h3>Калькулятор</h3>
      <p class="c-sub">Порахуйте, скільки чалдів виходить за місяць і коли оренда стає безкоштовною.</p>
      <div class="c-cups"><span id="rhCupsVal">20</span> <small>чашок на день</small></div>
      <input type="range" id="rhCups" min="5" max="80" value="20" step="1" aria-label="Чашок на день">
    </div>
    <div class="rh-calc-out">
      <div class="co-row"><span>Чалдів на місяць</span><b id="rhChalds">600</b></div>
      <div class="co-row"><span>Оренда кавомашини</span><b id="rhRent">0 ₴</b></div>
      <div class="co-row"><span>Кава (орієнтовно)</span><b id="rhCoffee">—</b></div>
      <span class="co-badge free" id="rhBadge">✓ Оренда безкоштовна</span>
    </div>
  </div>
</div></section>

<section class="rh-sec" style="background:var(--crema)"><div class="rh-wrap ese-explain reveal">
  <div class="ese-txt">
    <div class="rh-kicker">ПРОСТО ПРО ГОЛОВНЕ</div>
    <h2>Що таке чалди E.S.E. 44 мм</h2>
    <p>Готова порція кави у фільтрі 44 мм — «пакетик» для еспресо. Вставили, натиснули — чашка з пінкою за секунди. Без кавомолки й гущі.</p>
    <a href="monodozy-ese.html" class="btn btn-outline">Дивитись усі чалди E.S.E.</a>
  </div>
  <div class="ese-why">
    <h3>Чому саме E.S.E.</h3>
    <ul>
      <li>{ICON['check']}Завжди однаковий смак</li><li>{ICON['check']}Правильне дозування</li>
      <li>{ICON['check']}Швидке приготування</li><li>{ICON['check']}Немає бруду й гущі</li>
      <li>{ICON['check']}Не треба молоти каву</li><li>{ICON['check']}Мінімальний догляд</li>
      <li>{ICON['check']}Ідеально для дому</li><li>{ICON['check']}Ідеально для офісу</li>
    </ul>
  </div>
</div></section>

<section class="rh-sec"><div class="rh-wrap reveal">
  <div class="rh-head"><div class="rh-kicker">КАВА ДЛЯ ВАШОЇ КАВОМАШИНИ</div><h2>Оберіть каву — і машина працює безкоштовно</h2><div class="rh-hsub">Обладнання й кава — одна система. Чалди тут, за цінами сайту, <b>без націнок</b>{cup_line}.</div></div>
  <div class="chald-grid">{chalds_html}</div>
  <div style="text-align:center;margin-top:30px"><a href="monodozy-ese.html" class="btn btn-lg">Перейти до каталогу чалдів {ICON['arrow']}</a></div>
</div></section>

<section class="rh-sec"><div class="rh-wrap reveal">
  <div class="rh-head"><div class="rh-kicker">КАВОМАШИНА POLTI COFFEA</div><h2>Переваги апарата</h2><div class="rh-hsub">Компактна, 10,5 см. Біла S18W / чорна S15B.</div></div>
  <div class="rh-feat">{feat_html}</div>
  <div class="rh-gallery">{gallery_html}</div>
  <div style="text-align:center;margin-top:16px;color:var(--muted);font-size:14px">Реальні фото апарата · колір (біла S18W / чорна S15B) обираєте у заявці</div>
</div></section>

<section class="rh-sec" style="background:var(--soft)"><div class="rh-wrap reveal">
  <div class="rh-head"><div class="rh-kicker">ВІДЕО</div><h2>Кавомашина POLTI Coffea в дії</h2><div class="rh-hsub">Одна кнопка — еспресо за секунди.</div></div>
  <div class="rh-video" onclick="rhPlay(this)" data-id="msJSEkVrUDg">
    <img src="https://img.youtube.com/vi/msJSEkVrUDg/hqdefault.jpg" alt="Відео огляд кавомашини POLTI Coffea для чалдів E.S.E." width="900" height="506" loading="lazy">
    <button class="rh-play" aria-label="Відтворити відео"><svg viewBox="0 0 68 48"><path d="M66.5 7.7c-.8-2.9-3-5.1-5.9-5.9C55.3.5 34 .5 34 .5S12.7.5 7.4 1.8C4.5 2.6 2.3 4.8 1.5 7.7.2 13 .2 24 .2 24s0 11 1.3 16.3c.8 2.9 3 5.1 5.9 5.9C12.7 47.5 34 47.5 34 47.5s21.3 0 26.6-1.3c2.9-.8 5.1-3 5.9-5.9C67.8 35 67.8 24 67.8 24s0-11-1.3-16.3z" fill="#f00"/><path d="M27 34l18-10-18-10z" fill="#fff"/></svg></button>
  </div>
</div></section>



<section class="rh-sec" style="background:var(--soft)"><div class="rh-wrap reveal">
  <div class="rh-head"><div class="rh-kicker">ЯК ЦЕ ПРАЦЮЄ</div><h2>Оренда — у 4 кроки</h2><div class="rh-hsub">Від заявки до першої чашки кави.</div></div>
  <div class="steps">
    <div class="step"><span class="step-n">1</span><h3>Залишаєте заявку</h3><p>Ім’я, телефон і колір апарата.</p></div>
    <div class="step"><span class="step-n">2</span><h3>Ми доставляємо машину</h3><p>Узгоджуємо умови оренди й договір.</p></div>
    <div class="step"><span class="step-n">3</span><h3>Замовляєте чалди</h3><p>Обираєте кану до смаку — ми на зв’язку.</p></div>
    <div class="step"><span class="step-n">4</span><h3>Насолоджуєтесь кавою</h3><p>Професійний еспресо щодня.</p></div>
  </div>
</div></section>

<section class="rh-sec"><div class="rh-wrap reveal">
  <div class="rh-head"><div class="rh-kicker">ДЛЯ КОГО</div><h2>Де ставлять нашу кавомашину</h2><div class="rh-hsub">Офіс, салон, магазин, дім.</div></div>
  <div class="rh-seg">{seg_html}</div>
</div></section>

<section class="rh-sec" style="background:var(--crema)"><div class="rh-wrap reveal">
  <div class="rh-head"><div class="rh-kicker">ДОВІРА</div><h2>Чому саме NPRO MAX</h2><div class="rh-hsub">Своє обсмаження + повний супровід.</div></div>
  <div class="rh-why">{why_html}</div>
  <div class="b2b-band" style="margin-top:26px"><div class="b2b-txt"><div class="kicker">ВІДГУКИ</div><h2 style="color:#fff">4 400+ відгуків на Prom.ua</h2><p>Реальні оцінки покупців нашої кави. Договір оренди, доставка по всій Україні.</p></div><a href="https://npro.prom.ua" rel="nofollow" class="btn btn-lg">Дивитись відгуки</a></div>
</div></section>

<section class="rh-sec"><div class="rh-wrap reveal" style="max-width:860px">
  <div class="rh-head"><div class="rh-kicker">ПИТАННЯ І ВІДПОВІДІ</div><h2>Часті питання</h2></div>
  <div class="faq">{faq_html}</div>
</div></section>

<section class="rh-final" id="zayavka"><div class="rh-final-in reveal">
  <div class="rh-final-txt">
    <h2>Отримайте кавомашину POLTI вже цього тижня</h2>
    <p>Залиште заявку — менеджер зв’яжеться, підбере каву під ваш обсяг і узгодить договір. Ви платите лише за каву, а від 600 чалдів на місяць оренда — <b style="color:#ffb968">безкоштовна</b>.</p>
    {contact_html}
  </div>
  <div class="rh-formcard">
    <h3>Заявка на кавомашину</h3>
    <div class="fc-sub">Відповімо у робочі години. Це безкоштовно й ні до чого не зобов’язує.</div>
    {_rent_form_hub()}
  </div>
</div></section>

<div class="lp-sticky"><span><b>0 ₴/міс</b> · оренда POLTI</span><a href="#zayavka" class="btn">Отримати</a></div>
<div style="height:8px"></div>
'''
    body += RENTAL_JS
    return layout('Оренда кавомашини POLTI Coffea S18 для чалдів E.S.E. — 0 грн/міс | NPROMAX',
      'Оренда нової кавомашини POLTI Coffea S18 для дому та бізнесу: від 600 чалдів E.S.E. на місяць — 0 грн/міс, інакше 1000 грн. Калькулятор економії, умови, доставка по Україні.',
      body, active='kava-dlya-biznesu', canonical='orenda-kavomashyny.html')

def thank_you_page():
    body='''
<div class="wrap" style="text-align:center;padding:70px 20px 60px;max-width:640px">
<svg viewBox="0 0 24 24" width="80" height="80" fill="none" stroke="#3f8f3f" stroke-width="1.5" style="margin:0 auto 18px;display:block"><circle cx="12" cy="12" r="10"/><path d="M8 12l3 3 5-5"/></svg>
<h1 style="margin-bottom:10px">Дякуємо!</h1>
<p id="tyOrder" style="font-size:18px;font-weight:700;margin-bottom:18px">Замовлення прийнято.</p>
<div style="text-align:left;background:var(--soft);border-radius:14px;padding:22px;margin-bottom:24px">
<b>Що далі:</b>
<ul style="margin:10px 0 0 20px;color:var(--ink2)">
<li>Менеджер зв'яжеться з вами протягом робочого дня (Пн–Пт 9:00–18:00) для підтвердження.</li>
<li>Відправлення — Новою Поштою протягом 1–2 робочих днів після підтвердження; надішлемо номер ТТН.</li>
<li>Питання: <a href="mailto:info@npromax.com.ua" style="color:var(--orange)">info@npromax.com.ua</a></li>
</ul></div>
<div style="display:flex;gap:10px;flex-wrap:wrap;justify-content:center">
<a href="/" class="btn">На головну</a>
<a href="catalog.html" class="btn btn-outline">До каталогу</a>
</div>
</div>'''
    return layout('Дякуємо за замовлення — NPROMAX','Замовлення прийнято. Менеджер NPROMAX зв\'яжеться з вами для підтвердження.',body,canonical='thank-you.html')

def simple_page(title, h1, html_body, slug):
    body=f'''<div class="wrap"><div class="crumb"><a href="/">Головна</a><span>›</span>{esc(h1)}</div>
<div class="page"><h1>{esc(h1)}</h1>{html_body}</div></div>'''
    return layout(f'{title} — NPROMAX', title, body, canonical=slug+'.html')

def page404():
    body='''<div class="wrap" style="text-align:center;padding:70px 20px 60px;max-width:640px">
<img src="assets/img/notfound.jpg" alt="" style="width:260px;max-width:70%;border-radius:14px;margin:0 auto 16px;display:block">
<div style="font-size:60px;font-weight:800;color:var(--orange)">404</div>
<h1 style="margin:8px 0">Цю сторінку не знайдено, але кава вже чекає</h1>
<p style="color:var(--muted);margin-bottom:22px">Можливо, сторінку переміщено. Скористайтеся пошуком або оберіть розділ.</p>
<form onsubmit="event.preventDefault();var q=this.q.value.trim();if(q)location.href='catalog.html'" style="display:flex;gap:8px;max-width:420px;margin:0 auto 22px">
  <input name="q" placeholder="Пошук кави: арабіка, капсули, Ефіопія…" style="flex:1;padding:12px 14px;border:2px solid var(--line);border-radius:10px;font-family:inherit">
  <button class="btn">Знайти</button>
</form>
<div style="display:flex;gap:10px;flex-wrap:wrap;justify-content:center">
<a href="catalog.html" class="btn">До каталогу</a>
<a href="kava-v-zernakh.html" class="btn btn-outline">Кава в зернах</a>
<a href="kapsuly-nespresso.html" class="btn btn-outline">Капсули</a>
<a href="kontakty.html" class="btn btn-outline">Контакти</a>
</div>
</div>'''
    return layout('404 — сторінку не знайдено | NPROMAX','Сторінку не знайдено. Скористайтеся пошуком або перейдіть до каталогу кави NPROMAX.',body)

def build():
    cards=build_cards()
    counts={}
    for c in cards:
        for cat in c['cats']: counts[cat]=counts.get(cat,0)+1
    # статичні фото, доставлені разом з генератором (лежать поряд із site_products.json,
    # тобто в /home/npro/npromax-sync/ на сервері) → копіюємо у www/assets/img.
    # Генератор HTML/CSS/JS створює сам, а зображення переносить цей крок (щоб не робити ручних завантажень).
    import shutil
    _srcdir=os.path.dirname(os.environ.get('NPROMAX_SRC','') or '.') or '.'
    _imgdst=os.path.join(SITE,'assets','img'); os.makedirs(_imgdst,exist_ok=True)
    for _fn in ('polti-bila.webp','polti-bila.jpg','polti-chorna.webp','polti-chorna.jpg'):
        _s=os.path.join(_srcdir,_fn)
        if os.path.exists(_s):
            try: shutil.copy(_s, os.path.join(_imgdst,_fn))
            except Exception: pass
    # нові фото доставляються через git-репо: gen/assets/img/* -> www/assets/img
    _repoimg=os.path.join(_srcdir,'gen','assets','img')
    if os.path.isdir(_repoimg):
        for _fn in os.listdir(_repoimg):
            try: shutil.copy(os.path.join(_repoimg,_fn), os.path.join(_imgdst,_fn))
            except Exception: pass
    write_css(); write_js()
    def W(name,content): open(os.path.join(SITE,name),'w',encoding='utf-8').write(content)
    # search index injected into every page via a small json script — simplest: write once as JS global file
    sidx=[search_entry(c) for c in cards]
    # послуги: не картки товару, тому мають власний 'u' (URL) і не потрапляють у фільтр каталогу
    _rent_tags=['оренда','оренда кавомашини','аренда','аренда кофемашины','кавомашина','кофемашина',
              'polti','coffea','s18','s15','чалди','монодози','e.s.e.','ese','послуга','orenda','arenda','rent','безкоштовна']
    sidx.append({'s':'orenda-kavomashyny','u':'orenda-kavomashyny.html','svc':1,
      't':'Безкоштовна оренда кавомашини POLTI для чалдів E.S.E.',
      'i':RENT_COLORS['bila']['img'],'sku':'','skus':[],
      'tags':_rent_tags,'tr':lat('bezkoshtovna orenda kavomashyny polti coffea chaldy')})
    open(os.path.join(SITE,'assets','search.js'),'w',encoding='utf-8').write('window.SEARCH_DATA='+json.dumps(sidx,ensure_ascii=False)+';')
    # inject search.js reference by appending to app include? simplest: add <script> in layout. We'll patch pages: add before app.js.
    def inject(htmlpage):
        return htmlpage.replace('<script src="assets/app.js"></script>','<script src="assets/search.js"></script>\n<script src="assets/app.js"></script>')
    W('index.html', inject(home(cards,counts)))
    W('catalog.html', inject(catalog_page(cards)))
    for c in CATS:
        if c[0]=='kava-dlya-biznesu':
            W('kava-dlya-biznesu.html', inject(b2b_page(cards)))
        else:
            W(c[0]+'.html', inject(category_page(c[0],cards,counts)))
    for c in cards:
        W(f"p-{c['slug']}.html", inject(product_page(c,cards)))
    W('cart.html', inject(cart_page()).replace('</head>','<meta name="robots" content="noindex,follow">\n</head>'))
    W('thank-you.html', inject(thank_you_page()).replace('</head>','<meta name="robots" content="noindex,follow">\n</head>'))
    W('orenda-kavomashyny.html', inject(rental_hub(cards)))
    W('orenda-kavomashyny-polti-bila.html', inject(rental_landing('bila', cards)))
    W('orenda-kavomashyny-polti-chorna.html', inject(rental_landing('chorna', cards)))
    # static
    about='''<img src="assets/img/about.jpg" alt="NPROMAX — кава на кожен день" style="width:100%;border-radius:14px;margin-bottom:22px"><p>NPROMAX — торгова марка кави, створена для тих, хто хоче стабільно смачну чашку без зайвої складності. Ми відбираємо зерно, бленди та капсули так, щоб кожен формат давав максимум смаку — вдома, в офісі та в бізнесі.</p>
<h2>Наша ідея</h2><p>Від насиченого еспресо до м’якої арабіки, від зерна до свіжого помелу, від капсул до кавових рішень для офісу — NPROMAX створений, щоб дати більше смаку в кожній чашці.</p>
<img src="assets/img/about-2.jpg" alt="Затишна кава вдома" style="width:100%;border-radius:14px;margin:8px 0 18px" loading="lazy"><h2>Асортимент</h2><ul><li>Кава в зернах — моносорти 100% арабіки та ароматизовані бленди</li><li>Свіжомелена кава для турки, еспресо, гейзерної кавоварки, фільтра та френч-пресу</li><li>Капсули, сумісні з Nespresso® Original і Dolce Gusto®</li><li>E.S.E. монодози 44 мм</li><li>Формати для офісу, кафе, ресторанів, HoReCa та вендингу</li></ul>
<p class="ft-slogan" style="color:var(--orange);font-weight:700;font-size:18px">NPROMAX — кава, яку хочеться повторити.</p>'''
    W('about.html', inject(simple_page('Про бренд NPROMAX','Про бренд NPROMAX',about,'about')))
    delivery='''<h2>Доставка</h2>
<ul><li><b>Нова Пошта — відділення:</b> доставка по всій Україні, зазвичай 1–2 дні після відправлення.</li>
<li><b>Нова Пошта — поштомат:</b> зручно для невеликих замовлень (капсули, монодози).</li>
<li><b>Адресна доставка Новою Поштою</b> — кур'єром до дверей.</li>
<li><b>Термін відправлення:</b> протягом 1–2 робочих днів після підтвердження замовлення менеджером.</li>
<li><b>Вартість доставки:</b> за тарифами Нової Пошти, сплачується при отриманні (для великих B2B-замовлень умови доставки узгоджуються індивідуально).</li></ul>
<h2>Оплата</h2>
<ul><li><b>Накладений платіж</b> — оплата при отриманні у відділенні Нової Пошти (перевізник утримує комісію за переказ згідно зі своїми тарифами).</li>
<li><b>Оплата за реквізитами</b> — менеджер надішле рахунок після підтвердження замовлення (для ФОП/юросіб — з документами).</li></ul>
<h2>Для бізнесу</h2>
<ul><li>Гуртові партії, ящики капсул і регулярні поставки — умови та розрахунок доставки узгоджуються з менеджером.</li>
<li>Залиште заявку на сторінці <a href="kava-dlya-biznesu.html" style="color:var(--orange)">Кава для бізнесу</a>.</li></ul>
<h2>Часті питання</h2>
<div class="faq">
<details><summary>Коли відправите моє замовлення?</summary><p>Протягом 1–2 робочих днів після підтвердження менеджером. Про відправлення повідомимо і надішлемо номер ТТН.</p></details>
<details><summary>Чи можна оплатити при отриманні?</summary><p>Так, накладеним платежем у відділенні Нової Пошти. Зверніть увагу: перевізник утримує комісію за грошовий переказ.</p></details>
<details><summary>Як відстежити посилку?</summary><p>Після відправлення ви отримаєте номер ТТН — відстежуйте на сайті чи в застосунку Нової Пошти.</p></details>
<details><summary>Чи можна замовити для офісу з документами?</summary><p>Так, працюємо з ФОП та юрособами: рахунок, видаткова накладна. Деталі — через форму для бізнесу.</p></details>
<details><summary>Що робити, якщо посилка пошкоджена?</summary><p>Не приймайте відправлення без огляду: складіть акт у відділенні Нової Пошти та одразу напишіть нам на info@npromax.com.ua — замінимо товар.</p></details>
</div>'''
    W('dostavka-i-oplata.html', inject(simple_page('Доставка і оплата','Доставка і оплата',delivery,'dostavka-i-oplata')))
    ret='''<p>Ми хочемо, щоб кожна чашка кави NPROMAX радувала. Якщо із замовленням щось не так — розвʼяжемо питання швидко. Нижче — умови згідно із Законом України «Про захист прав споживачів».</p>
<h2>Товар неналежної якості</h2>
<p>Якщо ви отримали товар із дефектом (пошкоджена герметична упаковка, невідповідність позиції) — напишіть нам протягом <b>14 днів</b> з моменту отримання на <a href="mailto:info@npromax.com.ua" style="color:var(--orange)">info@npromax.com.ua</a> з фото. Ми за свій рахунок замінимо товар або повернемо кошти — на ваш вибір.</p>
<h2>Помилка комплектації</h2>
<p>Якщо приїхав не той сорт чи формат — заміна за наш рахунок у найкоротший строк. Повідомте нас із фото етикетки та накладної.</p>
<h2>Пошкодження під час доставки</h2>
<p>Оглядайте посилку при отриманні. Якщо упаковка пошкоджена — складіть акт у відділенні Нової Пошти та звʼяжіться з нами: замінимо товар.</p>
<h2>Товар належної якості</h2>
<p>Кава та інші харчові продукти належної якості обміну й поверненню не підлягають (Перелік, затверджений постановою КМУ № 172 від 19.03.1994). Тому радимо перед покупкою звертатися за консультацією — допоможемо обрати смак і формат, який точно підійде.</p>
<h2>Повернення коштів</h2>
<p>У випадках, передбачених законом, кошти повертаються тим самим способом, яким була здійснена оплата, протягом <b>7 робочих днів</b> після погодження повернення.</p>
<h2>Як звернутися</h2>
<ol><li>Напишіть на <a href="mailto:info@npromax.com.ua" style="color:var(--orange)">info@npromax.com.ua</a> або через <a href="kontakty.html" style="color:var(--orange)">форму зв'язку</a>: номер замовлення, опис проблеми, фото.</li>
<li>Менеджер відповість протягом робочого дня та узгодить заміну або повернення.</li></ol>
<p>Повні умови продажу — у <a href="oferta.html" style="color:var(--orange)">публічній оферті</a>.</p>'''
    W('povernennya.html', inject(simple_page('Повернення та обмін','Повернення та обмін',ret,'povernennya')))
    cont='''<p>Ми завжди на зв’язку й радо допоможемо обрати каву — напишіть нам, відповідаємо протягом робочого дня.</p>
<h2>Контакти</h2><ul>
<li>Email: <a href="mailto:info@npromax.com.ua" style="color:var(--orange)">info@npromax.com.ua</a></li>
<li>Графік: Пн–Пт 9:00–18:00 (Київський час)</li>
<li>Магазин на Prom.ua: <a href="https://npro.prom.ua" style="color:var(--orange)" rel="nofollow">npro.prom.ua</a></li></ul>
<h2>Напишіть нам</h2>
<form onsubmit="contactSend(event)" style="max-width:480px">
<div class="form-row"><label>Ім’я *</label><input name="name" required placeholder="Як до вас звертатися"></div>
<div class="form-row"><label>Email або телефон *</label><input name="email" required placeholder="Для відповіді"></div>
<div class="form-row"><label>Повідомлення *</label><textarea name="message" rows="4" required placeholder="Ваше запитання"></textarea></div>
<input type="text" name="_honey" style="display:none" tabindex="-1" autocomplete="off">
<button type="submit" class="btn">Надіслати</button>
<p style="font-size:11.5px;color:var(--muted);margin-top:8px">Надсилаючи, ви погоджуєтесь із <a href="privacy.html" style="color:var(--orange)">політикою конфіденційності</a>.</p>
</form>
<h2>Для бізнесу</h2><p>Оптові замовлення та поставки для офісів, кафе й HoReCa — залиште заявку на сторінці <a href="kava-dlya-biznesu.html" style="color:var(--orange)">Кава для бізнесу</a> — це найшвидший шлях отримати пропозицію.</p>'''
    W('kontakty.html', inject(simple_page('Контакти','Контакти',cont,'kontakty')))
    privacy='''<p>Ця Політика конфіденційності описує, які персональні дані збирає інтернет-магазин NPROMAX (npromax.com.ua), як вони використовуються та захищаються, відповідно до Закону України «Про захист персональних даних».</p>
<h2>1. Які дані ми збираємо</h2>
<ul><li>Дані, які ви залишаєте у формах замовлення та зворотного зв'язку: ім'я, телефон, email, місто, відділення Нової Пошти, коментар.</li>
<li>Технічні дані: файли cookie, знеособлена статистика відвідувань (використовується для роботи кошика та аналітики).</li></ul>
<h2>2. Для чого використовуємо</h2>
<ul><li>Обробка та доставка замовлень, зв'язок щодо замовлення.</li><li>Відповіді на звернення.</li><li>Покращення роботи сайту.</li></ul>
<p>Ми не передаємо ваші дані третім особам, окрім випадків, необхідних для виконання замовлення (служба доставки) або передбачених законом.</p>
<h2>3. Cookies</h2>
<p>Сайт використовує cookies для роботи кошика (збереження доданих товарів у вашому браузері) та базової аналітики. Ви можете вимкнути cookies у налаштуваннях браузера — кошик у такому разі не працюватиме.</p>
<h2>4. Зберігання і захист</h2>
<p>Дані замовлень зберігаються не довше, ніж потрібно для виконання зобов'язань та вимог законодавства. Доступ до даних має лише персонал магазину.</p>
<h2>5. Ваші права</h2>
<p>Ви маєте право отримати інформацію про свої дані, вимагати їх виправлення або видалення. Звертайтеся: <a href="mailto:info@npromax.com.ua" style="color:var(--orange)">info@npromax.com.ua</a>.</p>'''
    W('privacy.html', inject(simple_page('Політика конфіденційності','Політика конфіденційності',privacy,'privacy')))
    oferta='''<p>Цей документ є публічною пропозицією (офертою) інтернет-магазину NPROMAX (npromax.com.ua) укласти договір купівлі-продажу товарів дистанційним способом відповідно до ст. 633, 641 Цивільного кодексу України та Закону України «Про електронну комерцію».</p>
<h2>1. Загальні положення</h2>
<ul><li>Оформлення замовлення на сайті означає повне прийняття умов цієї оферти.</li>
<li>Продавець — суб'єкт господарювання, що здійснює продаж товарів під торговою маркою NPROMAX; реквізити продавця зазначаються у документах до замовлення та надаються за запитом на info@npromax.com.ua.</li></ul>
<h2>2. Товар і ціни</h2>
<ul><li>Ціни вказані в гривнях і оновлюються щодня. Актуальною є ціна на момент оформлення замовлення.</li>
<li>Зображення товарів можуть незначно відрізнятися від фактичного вигляду упаковки.</li>
<li>Nespresso® та Dolce Gusto® — торговельні марки їхніх власників; товари NPROMAX не є продукцією цих компаній, назви вживаються лише для позначення технічної сумісності.</li></ul>
<h2>3. Замовлення і доставка</h2>
<ul><li>Замовлення оформлюється через кошик, форму «Купити в 1 клік» або за листуванням.</li>
<li>Після оформлення менеджер підтверджує замовлення та строк відправлення.</li>
<li>Доставка — Новою Поштою за тарифами перевізника (деталі — на сторінці «Доставка і оплата»).</li></ul>
<h2>4. Оплата</h2>
<ul><li>Накладений платіж при отриманні або оплата за реквізитами за рахунком.</li></ul>
<h2>5. Повернення</h2>
<ul><li>Умови повернення та обміну описані на сторінці «Повернення та обмін» і відповідають Закону України «Про захист прав споживачів». Харчові продукти належної якості поверненню не підлягають.</li></ul>
<h2>6. Відповідальність і згода</h2>
<ul><li>Оформлюючи замовлення, покупець надає згоду на обробку персональних даних відповідно до Політики конфіденційності.</li>
<li>З усіх питань: <a href="mailto:info@npromax.com.ua" style="color:var(--orange)">info@npromax.com.ua</a>.</li></ul>'''
    W('oferta.html', inject(simple_page('Публічна оферта','Публічна оферта',oferta,'oferta')))
    terms='''<p>Ця Користувацька угода регулює використання сайту npromax.com.ua.</p>
<h2>1. Використання сайту</h2>
<ul><li>Сайт призначений для ознайомлення з асортиментом кави NPROMAX та оформлення замовлень.</li>
<li>Заборонено використовувати сайт у протиправних цілях, намагатися порушити його роботу чи отримати несанкціонований доступ.</li></ul>
<h2>2. Інтелектуальна власність</h2>
<ul><li>Тексти, фото та елементи дизайну сайту належать власнику ТМ NPROMAX. Використання матеріалів без згоди заборонене.</li>
<li>Згадки Nespresso® і Dolce Gusto® вживаються виключно для позначення технічної сумісності товарів.</li></ul>
<h2>3. Інформація на сайті</h2>
<ul><li>Ми дбаємо про точність описів і цін, але не гарантуємо відсутність технічних помилок; актуальні умови підтверджує менеджер при оформленні замовлення.</li></ul>
<h2>4. Контакти</h2>
<p><a href="mailto:info@npromax.com.ua" style="color:var(--orange)">info@npromax.com.ua</a></p>'''
    W('terms.html', inject(simple_page('Користувацька угода','Користувацька угода',terms,'terms')))
    W('academy.html', inject(academy_page()))
    for a in ARTICLES:
        W(f"academy-{a['slug']}.html", inject(article_page(a)))
    # 404: no canonical (would point to home), noindex
    W('404.html', inject(page404())
      .replace('<link rel="canonical" href="https://www.npromax.com.ua/">\n','')
      .replace('</head>','<meta name="robots" content="noindex,follow">\n</head>'))
    # --- sitemap.xml + robots.txt (production, www) ---
    BASE_URL='https://www.npromax.com.ua/'
    urls=['','catalog.html']
    urls+= [c[0]+'.html' for c in CATS]
    urls+= ['p-'+c['slug']+'.html' for c in cards]
    urls+= ['academy.html'] + ['academy-'+a['slug']+'.html' for a in ARTICLES]
    urls+= ['about.html','dostavka-i-oplata.html','povernennya.html','kontakty.html','privacy.html','oferta.html','terms.html',
            'orenda-kavomashyny.html','orenda-kavomashyny-polti-bila.html','orenda-kavomashyny-polti-chorna.html']
    sm=['<?xml version="1.0" encoding="UTF-8"?>','<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    import datetime
    today='2026-07-04'
    for u in urls:
        pr='1.0' if u=='' else ('0.8' if not u.startswith('p-') else '0.7')
        sm.append(f'<url><loc>{BASE_URL}{u}</loc><lastmod>{today}</lastmod><priority>{pr}</priority></url>')
    sm.append('</urlset>')
    open(os.path.join(SITE,'sitemap.xml'),'w',encoding='utf-8').write('\n'.join(sm))
    # NPX-014: Merchant-фід (генеруємо; у кабінет НЕ завантажуємо без «так» власника)
    open(os.path.join(SITE,'feed-merchant.xml'),'w',encoding='utf-8').write(merchant_feed(cards))
    open(os.path.join(SITE,'robots.txt'),'w',encoding='utf-8').write(
'''User-agent: *
Allow: /
Disallow: /cart.html
Disallow: /_generator/

Sitemap: https://www.npromax.com.ua/sitemap.xml
''')
    print("cards:",len(cards),"| files written to",SITE)
    print("counts:",counts)


# ---------- unique product descriptions (T4) ----------
FLAVORS={
 'Амаретто':('класичний італійський смак мигдалевого лікеру','солодкий мигдаль, марципан і легка гірчинка ядра абрикосової кісточки в теплому післясмаку'),
 'Ананас':('соковитий тропічний акцент у щільній кавовій основі','стиглий ананас, тропічні фрукти та легка карамельна солодкість'),
 'Баварський шоколад':('десертний смак густого гарячого шоколаду','темний шоколад, какао та вершкова солодкість у довгому післясмаку'),
 'Банан':('м\'який десертний смак стиглого банана','банан, вершки та ніжна карамель'),
 'Бейліс':('смак знаменитого вершкового лікеру','вершки, ірландський віскі, ваніль і карамель'),
 'Ваніль':('делікатний кондитерський аромат','мадагаскарська ваніль, вершки та солодка випічка'),
 'Вишня':('виразний ягідний характер','стигла вишня, легка мигдалева нотка та шоколадний фінал'),
 'Віскі':('благородний смак витриманого напою','димні дубові відтінки, карамель і сухофрукти'),
 'Кава':('подвійний кавовий характер — для тих, хто любить каву на максимум','смажені зерна, какао та щільна кавова гірчинка'),
 'Капучіно':('смак улюбленого молочного напою','молочна пінка, вершки та м\'яка кавова основа'),
 'Капучино':('смак улюбленого молочного напою','молочна пінка, вершки та м\'яка кавова основа'),
 'Карамель':('тепла кондитерська солодкість','вершкова карамель, ірис і легка ваніль'),
 'Кокос':('тропічна м\'якість','кокосова стружка, вершки та біла шоколадна нотка'),
 'Кориця':('затишний пряний характер','цейлонська кориця, випічка та мед'),
 'Крем-лікер Бейліс':('десертний смак вершкового лікеру','вершки, віскі, ваніль і карамельний фінал'),
 'Лісовий горіх':('улюблена горіхова класика','смажений фундук, праліне та молочний шоколад'),
 'Малина':('яскравий ягідний акцент','стигла малина, ягідний джем і легка солодкість'),
 'Мигдаль':('елегантний горіховий смак','смажений мигдаль, марципан і вершки'),
 'Мигдаль, Амаретто':('поєднання горіха та лікеру','мигдаль, амаретто й тепла солодкість марципана'),
 'Полуниця':('літній ягідний настрій','стигла полуниця, вершки та ягідна солодкість'),
 'Пряний шоколад':('шоколад із характером','темний шоколад, кориця, кардамон і легка перчинка'),
 'Ром':('карибський характер','темний ром, тростинний цукор і сухофрукти'),
 'Ром, ваніль':('м\'яке поєднання рому та ванілі','ром, ваніль і карамельна солодкість'),
 'Снікерс':('смак улюбленого батончика','арахіс, карамель, нуга та молочний шоколад'),
 'Трюфель':('вишуканий десертний профіль','шоколадний трюфель, какао та вершки'),
 'Тірамісу':('смак італійського десерту','маскарпоне, какао, бісквіт савоярді та кавова просочка'),
 'Тирамісу':('смак італійського десерту','маскарпоне, какао, бісквіт савоярді та кавова просочка'),
 'Ірландський крем':('м\'який смак ірландського вершкового лікеру','вершки, віскі, ваніль і горіхова нотка'),
}
ORIGINS={
 'Ефіопія':('батьківщина кави — високогірна арабіка з виразним характером','квіткові та ягідні відтінки, цитрусова кислинка й чайна легкість тіла'),
 'Бразилія':('класика м\'якої арабіки з найбільшого кавового регіону світу','горіх, какао та солодкість смаженого хліба з м\'якою, ненав\'язливою кислинкою'),
 'Колумбія':('збалансована високогірна арабіка','карамель, червоні фрукти та рівна, чиста чашка з приємною солодкістю'),
 'Кенія':('одна з найяскравіших арабік Африки','чорна смородина, ягідна соковитість і виразна винна кислинка'),
 'Коста-Ріка':('чиста та акуратна центральноамериканська арабіка','цитрус, мед і легка фруктова солодкість'),
 'Мексика':('м\'яка арабіка з делікатним характером','горіх, шоколад і легка карамель'),
 'Нікарагуа':('солодка збалансована арабіка','карамель, горіх і делікатна фруктова кислинка'),
 'Панама':('елегантна арабіка з тонкою ароматикою','квіткові відтінки, цитрус і мед'),
 'Перу':('м\'яка високогірна арабіка Південної Америки','молочний шоколад, легкі фрукти та горіхова солодкість'),
 'Руанда':('соковита арабіка Східної Африки','ягоди, цитрус і виразна, освіжаюча кислинка'),
 'Сальвадор':('округла та солодка центральноамериканська арабіка','карамель, горіх і збалансоване щільне тіло'),
 'Танзанія':('арабіка зі схилів Кіліманджаро','фруктова соковитість і характерна винна кислинка'),
 'Гватемала':('щільна арабіка з вулканічних ґрунтів','шоколад, спеції та димна глибина у довгому післясмаку'),
 'Гондурас':('солодка та м\'яка арабіка','карамель, горіх і відтінки стиглих фруктів'),
 'Бурунді':('яскрава африканська арабіка','ягоди, цитрус і жвава кислинка в легкому тілі'),
 'Індія':('щільна арабіка мусонного регіону','какао, спеції та низька кислотність — ідеально під еспресо з молоком'),
}
BLENDS={
 'Premium Blend':('збалансований купаж арабіки (80%) та робусти (20%)','округлий смак з какао та горіхом, щільна крема та впевнена, але акуратна міцність'),
 'Espresso Blend':('класичний еспресо-купаж арабіки та робусти 50/50','щільне тіло, шоколадна гірчинка та стійка горіхова крема'),
 'Robusta Blend':('міцний купаж на основі 100% робусти','інтенсивна гірчинка, темний шоколад і максимальний заряд бадьорості'),
 'Arabica Blend':('делікатний купаж зі 100% арабіки','м\'яка солодкість, фруктові відтінки та ніжна крема'),
 'Arabica blend':('делікатний купаж зі 100% арабіки','м\'яка солодкість, фруктові відтінки та ніжна крема'),
 'Intense Blend':('максимально міцний профіль зі 100% робусти','щільна гірчинка, какао та довгий насичений післясмак'),
 'Decaffeinato':('улюблений смак еспресо без кофеїну','м\'яке тіло, горіхово-шоколадні відтінки та чиста чашка — навіть увечері'),
 'Без кофеїну':('арабіка без кофеїну — смак без обмежень','м\'яка солодкість, горіх і делікатна кислинка'),
}
DRINKS={
 'Tea Lemon':('освіжаючий чорний чай із лимоном у зручній капсулі','цитрусова свіжість і тонізуючий чайний смак'),
 'Cappuccino':('капучино без цукру — кава з молочною пінкою одним натисканням','вершкова м\'якість, молочна пінка та делікатна кавова основа'),
 'Chocolate':('густий гарячий шоколад','насичене какао та вершкова солодкість'),
 'Milk':('молочна капсула для приготування напоїв з молоком','вершкова текстура для лате, капучино чи какао'),
 'Matcha':('зелений чай матча з молоком','трав\'яниста свіжість матчі та молочна м\'якість'),
}
BREW_TXT={
 'beans':'Найповніше цей смак розкриється в автоматичній кавомашині або ріжковій кавоварці. Для турки, гейзерної кавоварки чи френч-пресу змеліть зерна безпосередньо перед приготуванням — так аромат буде найяскравішим.',
 'ground':'Помел підібраний так, щоб кава зручно готувалася вдома: у турці, гейзерній кавоварці, френч-пресі або фільтрі. Заварюйте одразу після відкриття упаковки — свіжість аромату найвища в перші тижні.',
 'ncap':'Вставте капсулу в кавомашину, сумісну з системою Nespresso® Original, — і за пів хвилини отримаєте еспресо зі стійкою кремою. Жодного помелу, дозування та прибирання.',
 'dcap':'Капсула розрахована на кавомашини системи Dolce Gusto®: одне натискання — і напій готовий. Зручно вдома та в офісі.',
 'ese':'Монодоза стандарту E.S.E. (44 мм) — готова порція для еспресо-кавоварок із тримачем під чалди: стабільне дозування та щільна пінка без кавомолки.',
 'drink':'Використовуйте капсулу в сумісній кавомашині — напій готується одним натисканням, без порошків і мірних ложок.',
}
def _flavor_of(card):
    import re as _re
    m=_re.search(r'[«"]([^"»]+)[»"]', card['title'])
    return m.group(1).strip() if m else None
def _blend_of(card):
    for k in BLENDS:
        if k.lower() in card['title'].lower(): return k
    return None
def _drink_of(card):
    for k in DRINKS:
        if k.lower() in card['title'].lower(): return k
    return None
def desc_blocks(card):
    t=card['type']; ps=[]
    fmt={'beans':'кава в зернах','ground':'свіжомелена кава','ncap':'кава в капсулах','dcap':'кава в капсулах','ese':'кава в монодозах E.S.E.','drink':'напій у капсулах'}.get(t,'кава')
    fl=_flavor_of(card) if card['aroma'] else None
    if fl and fl in FLAVORS:
        d,n=FLAVORS[fl]
        ps.append(f'«{fl}» — це {d}. Ароматизована {fmt} NPROMAX на основі збалансованого купажу арабіки та робусти: кавова основа тримає характер, а аромат додає настрою кожній чашці.')
        ps.append(f'Смакові ноти: {n}. Аромат розкривається одразу після відкриття упаковки й підсилюється під час приготування.')
    elif (not card['aroma']) and card['country'] and card['country'] in ORIGINS and card['type'] in ('beans','ground'):
        d,n=ORIGINS[card['country']]
        ps.append(f'{card["country"]} — {d}. Це моносорт 100% арабіки: один регіон походження, чистий і впізнаваний характер чашки у форматі «{fmt}».')
        ps.append(f'Смакові ноти: {n}. Середнє обсмаження зберігає баланс солодкості та кислотності.')
    elif _blend_of(card):
        b=_blend_of(card); d,n=BLENDS[b]
        ps.append(f'{b} — {d}. {("Формат: "+fmt+".") if t!="beans" else ""}')
        ps.append(f'Смакові ноти: {n}.')
    elif t=='drink' and _drink_of(card):
        k=_drink_of(card); d,n=DRINKS[k]
        ps.append(f'{card["title"].split(",")[0]} — це {d}.')
        ps.append(f'У чашці: {n}. Зверніть увагу: це напій у капсулі, сумісній із капсульною системою, а не кава.')
    else:
        ps.append(desc_intro(card))
    ps.append(BREW_TXT.get(t,''))
    who={'beans':'Підійде для дому та офісу — всім, хто цінує свіжість зерна й аромат щойно змеленої кави.',
         'ground':'Зручний вибір для дому: жодної кавомолки — відкрили, заварили, насолоджуєтесь.',
         'ncap':'Для власників капсульних кавомашин удома та невеликих офісів — швидко, стабільно та без клопоту.',
         'dcap':'Для власників кавомашин Dolce Gusto® — стабільний смак без зайвих зусиль.',
         'ese':'Для кав\'ярень, офісів і дому — там, де цінують швидкість і стабільний результат еспресо.',
         'drink':'Гарне доповнення до кавового меню вдома чи в офісі — для тих, хто не пʼє каву або хоче різноманіття.'}.get(t,'')
    if card['decaf']: who+=' Без кофеїну — можна насолоджуватися навіть увечері.'
    ps.append(who)
    return '\n'.join(f'<p>{esc(x)}</p>' for x in ps if x)


# ---------- Академія смаку (blog) ----------
COVERS={'arabika-chy-robusta':'assets/img/cover-arabika.jpg','yak-obraty-pomel':'assets/img/cover-pomel.jpg',
 'espresso-vdoma':'assets/img/cover-espresso.jpg','kava-v-turtsi':'assets/img/cover-turka.jpg',
 'yak-zberihaty-kavu':'assets/img/cover-storage.jpg','nespresso-vs-dolce-gusto':'assets/img/cover-cozy.jpg'}
ARTICLES=[
 {'slug':'arabika-chy-robusta','icon':'mono','tag':'ВИБІР КАВИ','title':'Арабіка чи робуста: що обрати саме вам',
  'teaser':'Дві головні кавові культури світу — і зовсім різний характер чашки. Розбираємося без снобізму.',
  'body':'''
<p>Майже вся кава світу — це два види: арабіка та робуста. Від їхнього співвідношення в упаковці залежить смак, міцність і навіть висота пінки. Розберімося, чим вони відрізняються і що обрати під ваш смак.</p>
<h2>Арабіка: аромат і багатство смаку</h2>
<p>Арабіка росте високо в горах, дозріває повільно й накопичує складні ароматичні сполуки. У чашці це дає багатий аромат, приємну кислинку та відтінки — від ягід і цитрусів (Африка) до горіха й шоколаду (Південна Америка). Кофеїну в ній приблизно вдвічі менше, ніж у робусті.</p>
<p>Обирайте <a href="arabika-monosorty.html">моносорти 100% арабіки</a>, якщо любите мʼяку каву з характером і хочете відчувати різницю між Ефіопією та Бразилією.</p>
<h2>Робуста: міцність і щільність</h2>
<p>Робуста невибаглива, росте нижче й дає простіший, але значно міцніший смак: щільне тіло, виразна гірчинка, багато кофеїну. Саме робуста відповідає за стійку пінку-крему в еспресо.</p>
<h2>Купаж: найкраще з двох світів</h2>
<p>Більшість еспресо-блендів — це купаж: арабіка дає аромат, робуста — міцність і крему. Класика — 80/20 або 50/50. Якщо ви пʼєте каву з молоком, купаж — майже завжди правильний вибір: він «пробиває» молоко і не губиться в капучино.</p>
<div class="tip"><b>Порада NPROMAX:</b> любите чорну каву без цукру — починайте з арабіки (Бразилія Сантос чи Колумбія). Любите міцну ранкову чашку або каву з молоком — беріть купаж із робустою.</div>
<h2>Що обрати</h2>
<ul>
<li><b>Мʼякість і аромат:</b> <a href="arabika-monosorty.html">100% арабіка, моносорти</a>.</li>
<li><b>Міцність та крема:</b> купажі з робустою — <a href="kavovi-kupazhi.html">кавові купажі</a>.</li>
<li><b>Зручність:</b> <a href="kapsuly-nespresso.html">капсули</a> з тими самими блендами.</li>
</ul>'''},
 {'slug':'yak-obraty-pomel','icon':'ground','tag':'СВІЖОМЕЛЕНА','title':'Який помел обрати: від турки до френч-пресу',
  'teaser':'Занадто дрібний — гірчить, занадто грубий — водянисто. Просте правило, яке все пояснює.',
  'body':'''
<p>Помел — це головний інструмент смаку після самого зерна. Правило просте: <b>що довше кава контактує з водою, то грубішим має бути помел.</b> Порушите баланс — отримаєте гіркоту (перезаварювання) або «воду» (недозаварювання).</p>
<h2>Шпаргалка по способах приготування</h2>
<ul>
<li><b>Турка</b> — дуже дрібний, «в пил». Кава вариться прямо в чашці, дрібні частинки створюють щільне тіло та пінку.</li>
<li><b>Еспресо (ріжкова кавоварка)</b> — дрібний. Вода проходить крізь таблетку за 25–30 секунд.</li>
<li><b>Гейзерна кавоварка</b> — середньо-дрібний. Дрібніший забиває фільтр, грубіший дає порожній смак.</li>
<li><b>Фільтр-кава, крапельна кавоварка</b> — середній, як цукровий пісок.</li>
<li><b>Френч-прес</b> — грубий. Кава настоюється 4 хвилини, дрібний помел зробить чашку каламутною.</li>
<li><b>Холодне заварювання (cold brew)</b> — дуже грубий, настоюється 12–18 годин.</li>
</ul>
<div class="tip"><b>Порада NPROMAX:</b> якщо у вас немає кавомолки — обирайте <a href="svizhomelena-kava.html">свіжомелену каву</a> і вкажіть у коментарі до замовлення, як готуєте: підкажемо, чи підійде помел.</div>
<h2>Чому «свіжо» — важливо</h2>
<p>Мелена кава віддає аромат швидше за зернову: найяскравіші — перші тижні після відкриття упаковки. Тому купуйте мелену каву невеликими упаковками, зберігайте щільно закритою і заварюйте із задоволенням — саме так вона розкриває максимум смаку.</p>
<p>А якщо вдома є кавомолка — беріть <a href="kava-v-zernakh.html">зерно</a> й меліть безпосередньо перед приготуванням.</p>'''},
 {'slug':'espresso-vdoma','icon':'ncap','tag':'ПРИГОТУВАННЯ','title':'Як приготувати еспресо вдома: 5 кроків',
  'teaser':'Щільна крема і збалансований смак — реально й без професійної кавомашини.',
  'body':'''
<p>Еспресо — це 25–30 мл насиченого смаку за 25–30 секунд. Здається складно, але вдома його реально готувати стабільно смачним. Ось що важливо.</p>
<h2>1. Свіжа кава</h2>
<p>Основа — свіжообсмажене зерно середнього або темнішого обсмаження. Для класичного еспресо беріть <a href="kavovi-kupazhi.html">купаж арабіки з робустою</a> — саме він дає щільну крему.</p>
<h2>2. Правильне дозування</h2>
<p>Стандарт — 8–9 г кави на порцію (подвійна — 16–18 г). Забагато кави — гірчить, замало — кисне й тече швидко.</p>
<h2>3. Помел і трамбування</h2>
<p>Помел дрібний, трамбування впевнене та рівне. Якщо еспресо витікає швидше за 20 секунд — змеліть дрібніше; повільніше за 35 — грубіше.</p>
<h2>4. Вода</h2>
<p>93–95 °C, мʼяка. Жорстка вода вбиває смак і кавоварку.</p>
<h2>5. Пийте одразу</h2>
<p>Еспресо живе 1–2 хвилини — потім крема осідає й аромат тьмяніє.</p>
<div class="tip"><b>Без ріжкової кавоварки?</b> Найпростіший шлях до стабільного еспресо — <a href="kapsuly-nespresso.html">капсули, сумісні з Nespresso Original</a>, або <a href="monodozy-ese.html">монодози E.S.E. 44 мм</a>: доза, помел і трамбування вже ідеально відкалібровані.</div>'''},
 {'slug':'kava-v-turtsi','icon':'beans','tag':'ПРИГОТУВАННЯ','title':'Кава в турці: помел, пропорції, покрокова інструкція',
  'teaser':'Найдавніший спосіб заварювання — і досі один із найсмачніших. Головне — не кипʼятити.',
  'body':'''
<p>Кава по-східному — це густа, щільна чашка з пінкою і максимально прямий контакт зі смаком. Для турки важливі три речі: найдрібніший помел, холодна вода і терпіння.</p>
<h2>Пропорції</h2>
<p>Класика: 1 чайна ложка з гіркою (7–8 г) на 100 мл холодної води. Цукор і спеції (кардамон, кориця) — одразу в турку, до нагрівання.</p>
<h2>Покроково</h2>
<ol>
<li>Насипте каву «в пил» у суху турку, додайте цукор/спеції за смаком.</li>
<li>Залийте холодною водою до звуження шийки.</li>
<li>Поставте на найменший вогонь. Не заважайте й не відходьте.</li>
<li>Щойно пінка почне підійматися (це ~92 °C, не кипіння!) — зніміть з вогню.</li>
<li>За бажанням повторіть підйом пінки ще раз. Дайте 30 секунд відстоятися — і розливайте.</li>
</ol>
<div class="tip"><b>Головна помилка</b> — закипʼятити. Кипіння руйнує аромат і дає порожню гірку чашку. Пінка піднялася — знімайте.</div>
<h2>Яку каву брати</h2>
<p>Для турки чудово працюють моносорти арабіки з виразним характером — Ефіопія (ягідно-квіткова) чи Кенія (яскрава кислинка), а також <a href="svizhomelena-kava.html">свіжомелена кава NPROMAX</a>. Любите солодкуватий профіль — беріть Бразилію. Хочете десертного настрою — спробуйте <a href="kava-v-zernakh.html">ароматизовані зерна</a> «Кориця» чи «Ірландський крем» (наприкінці списку категорії).</p>'''},
 {'slug':'yak-zberihaty-kavu','icon':'decaf','tag':'КОРИСНО ЗНАТИ','title':'Як зберігати каву, щоб не втратити аромат',
  'teaser':'Чотири вороги кави: повітря, світло, волога і чужі запахи. Як захиститися — за 2 хвилини.',
  'body':'''
<p>Кава — продукт свіжості. Навіть найкраще зерно можна «вбити» неправильним зберіганням за тиждень. Ось прості правила, які реально працюють.</p>
<h2>Чого кава боїться</h2>
<ul>
<li><b>Кисень</b> — окислює олії, аромат вивітрюється. Головний ворог №1.</li>
<li><b>Світло</b> — прискорює старіння, особливо пряме сонце.</li>
<li><b>Волога</b> — зерно гігроскопічне: вбирає воду й запахи.</li>
<li><b>Сторонні запахи</b> — кава чудово «колекціонує» аромати холодильника чи спецій поруч.</li>
</ul>
<h2>Як правильно</h2>
<ul>
<li>Зберігайте у щільно закритій непрозорій ємності або в оригінальному пакеті з клапаном, добре притиснувши повітря.</li>
<li>Темна шафа подалі від плити — ідеальне місце. Не холодильник: там волога й запахи.</li>
<li>Мелену каву використовуйте протягом 2–4 тижнів після відкриття, зернову — до 2 місяців.</li>
<li>Не купуйте «про запас» на пів року — краще частіше й свіжіше.</li>
</ul>
<div class="tip"><b>Лайфхак:</b> велика упаковка вигідніша, але якщо пʼєте мало — пересипте частину в маленьку герметичну банку «на щодень», а основний пакет тримайте щільно закритим.</div>
<p>І памʼятайте: найкраще зберігання не замінить свіжого зерна. Обирайте <a href="kava-v-zernakh.html">каву в зернах</a> або <a href="svizhomelena-kava.html">свіжомелену</a> — і пийте її, поки вона в найкращій формі.</p>'''},
 {'slug':'nespresso-vs-dolce-gusto','icon':'dcap','tag':'КАПСУЛИ','title':'Nespresso Original і Dolce Gusto: у чому різниця',
  'teaser':'Дві найпопулярніші капсульні системи — але капсули між ними не взаємозамінні. Пояснюємо.',
  'body':'''
<p>Обидві системи створені для одного — смачна кава одним натисканням. Але це різні стандарти: капсула від однієї машини фізично не підійде до іншої. Перевірте свою кавомашину перед замовленням.</p>
<h2>Nespresso Original: класика еспресо</h2>
<p>Маленька алюмінієво-пластикова капсула, висока помпа (19 бар), порція 25–110 мл. Це система для тих, хто любить <b>класичний еспресо та лунго</b> — щільний, із кремою. Молочні напої готуються окремим спінювачем.</p>
<p>Дивіться: <a href="kapsuly-nespresso.html">капсули NPROMAX, сумісні з Nespresso Original</a> — бленди Premium, Espresso, Robusta та Decaffeinato.</p>
<h2>Dolce Gusto: різноманіття напоїв</h2>
<p>Більша капсула та більші порції. Сильна сторона системи — <b>різноманіття</b>: крім кави, є капучино, гарячий шоколад, чай і навіть матча. Зручно для родини, де кожен пʼє своє.</p>
<p>Дивіться: <a href="kapsuly-dolce-gusto.html">капсули, сумісні з Dolce Gusto</a> та <a href="napoyi-v-kapsulakh.html">напої в капсулах</a>.</p>
<h2>Коротке порівняння</h2>
<ul>
<li><b>Ви за чистий еспресо</b> → Nespresso Original.</li>
<li><b>Родина з різними смаками, любите молочні напої</b> → Dolce Gusto.</li>
<li><b>Ціна чашки</b> — порівнянна; ящики по 50–100 капсул суттєво вигідніші — дивіться <a href="kava-dlya-biznesu.html">формати для офісу</a>.</li>
</ul>
<div class="tip">Nespresso® та Dolce Gusto® — торговельні марки їхніх власників. Капсули NPROMAX не виробляються цими компаніями та не афілійовані з ними — назви вказують лише на технічну сумісність.</div>'''},
]

def article_page(a):
    others=[x for x in ARTICLES if x['slug']!=a['slug']][:3]
    oth=''.join(f'<a href="academy-{o["slug"]}.html" class="acad-card"><img src="{COVERS.get(o["slug"],"")}" alt="" loading="lazy"><div class="tag">{o["tag"]}</div><h3>{esc(o["title"])}</h3><p>{esc(o["teaser"])}</p><span class="more">Читати {ICON["arrow"]}</span></a>' for o in others)
    body=f'''
<div class="wrap"><div class="crumb"><a href="/">Головна</a><span>›</span><a href="academy.html">Академія смаку</a><span>›</span>{esc(a['title'])}</div></div>
<div class="wrap"><article class="art">
<div class="tag" style="font-size:11px;font-weight:700;letter-spacing:1.5px;color:var(--orange);margin-bottom:8px">{a['tag']}</div>
<h1>{esc(a['title'])}</h1>
<div class="art-meta">Академія смаку NPROMAX · корисно про каву</div>
{('<img class="art-cover" src="'+COVERS[a['slug']]+'" alt="" loading="lazy">') if a['slug'] in COVERS else ''}
{a['body']}
<div class="art-cta"><p><b style="color:#fff">Готові спробувати?</b> Обирайте каву NPROMAX — від моносортів арабіки до капсул.</p><a href="catalog.html" class="btn">До каталогу</a></div>
</article></div>
<div class="wrap" style="padding-bottom:50px"><h2 style="margin-bottom:18px">Читайте також</h2><div class="acad-grid">{oth}</div></div>
'''
    return layout(f"{a['title']} — Академія смаку NPROMAX", a['teaser'], body, canonical=f"academy-{a['slug']}.html")

def academy_page():
    cards=''.join(f'<a href="academy-{a["slug"]}.html" class="acad-card"><img src="{COVERS.get(a["slug"],"")}" alt="" loading="lazy"><div class="tag">{a["tag"]}</div><h3>{esc(a["title"])}</h3><p>{esc(a["teaser"])}</p><span class="more">Читати {ICON["arrow"]}</span></a>' for a in ARTICLES)
    body=f'''
<div class="wrap"><div class="crumb"><a href="/">Головна</a><span>›</span>Академія смаку</div></div>
{band_open("academy")}<div class="wrap cat-head"><h1>Академія смаку NPROMAX</h1><p class="lead">Корисно про каву без снобізму: як обирати, готувати та зберігати, щоб кожна чашка виходила смачною.</p></div></div>
<div class="wrap section"><div class="acad-grid">{cards}</div></div>
'''
    return layout('Академія смаку NPROMAX — корисно про каву','Як обрати каву, який помел для турки та френч-пресу, як приготувати еспресо вдома, чим відрізняються Nespresso і Dolce Gusto — Академія смаку NPROMAX.',body,canonical='academy.html')

if __name__=='__main__':
    build()
