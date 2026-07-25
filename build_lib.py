# -*- coding: utf-8 -*-
"""NPROMAX site generator — normalizer + data model. Corporate colors orange/black/white."""
import json, re, html, os

SITE = os.environ.get("NPROMAX_SITE", "/Users/bogdansokurenko/Library/Mobile Documents/com~apple~CloudDocs/Актуально/NPOMAX/FB/npromax-site")
SRC = os.environ.get("NPROMAX_SRC", "./site_products.json")

# ---------- transliteration (KMU-2010 simplified) ----------
_TR = {
 'а':'a','б':'b','в':'v','г':'h','ґ':'g','д':'d','е':'e','є':'ie','ж':'zh','з':'z',
 'и':'y','і':'i','ї':'i','й':'i','к':'k','л':'l','м':'m','н':'n','о':'o','п':'p',
 'р':'r','с':'s','т':'t','у':'u','ф':'f','х':'kh','ц':'ts','ч':'ch','ш':'sh','щ':'shch',
 'ь':'','ю':'iu','я':'ia','ё':'e','ъ':'','ы':'y','э':'e',
}
def translit(s):
    s = (s or '').lower()
    out = []
    for i,ch in enumerate(s):
        if ch in _TR:
            v = _TR[ch]
            if ch in ('й','ю','я','є','ї') and i>0 and s[i-1] not in _TR and False:
                pass
            out.append(v)
        elif ch.isalnum():
            out.append(ch)
        else:
            out.append('-')
    r = ''.join(out)
    r = re.sub(r'-+','-',r).strip('-')
    return r

def esc(s): return html.escape(s or '', quote=True)

# ---------- load ----------
def load(): return json.load(open(SRC, encoding='utf-8'))

# ---------- classification ----------
def low(p): return ((p['name_uk'] or '')+' '+(p.get('keywords_uk') or '')).lower()

def is_capsule(p): return 'капсул' in (p['name_uk'] or '').lower()
def is_ese(p): return bool(re.search(r'монодоз|e\.?s\.?e|44\s*мм', (p['name_uk'] or '').lower()))
def is_drink(p):
    # drinks in capsules only (aromatized beans named "шоколад"/"капучіно" are coffee, not drinks)
    return is_capsule(p) and bool(re.search(r'\bчаю\b|\bчай\b|шоколад|молок|молоко|капуч|матч|matcha|напій|напою|tea|milk|chocolate|cappuccino', (p['name_uk'] or '').lower()))
def is_ground(p):
    n=(p['name_uk'] or '').lower()
    return bool(re.match(r'\s*(ароматизована\s+)?мелена', n)) or ('мелена кава' in n and 'в зернах' not in n)
def is_beans(p): return 'в зернах' in (p['name_uk'] or '').lower()
def is_aroma(p): return 'ароматизован' in (p['name_uk'] or '').lower()
def is_decaf(p): return bool(re.search(r'декаф|без кофеїну|decaf|decaffeinato', low(p)))
def is_nespresso(p): return 'nespresso' in (p['name_uk'] or '').lower()
def is_dolce(p): return 'dolce' in (p['name_uk'] or '').lower()
def is_business(p): return 'ящик' in (p['name_uk'] or '').lower()
def is_monosort(p):
    return ('100% арабіка' in (p['name_uk'] or '').lower() or '100% арабика' in (p['name_uk'] or '').lower()) and not is_aroma(p)
def is_blend(p):
    return bool(re.search(r'blend|купаж', (p['name_uk'] or '').lower())) and not is_drink(p)

def ptype(p):
    if is_drink(p): return 'drink'
    if is_ese(p): return 'ese'
    if is_capsule(p) and is_nespresso(p): return 'ncap'
    if is_capsule(p) and is_dolce(p): return 'dcap'
    if is_capsule(p): return 'cap'
    if is_ground(p): return 'ground'
    if is_beans(p): return 'beans'
    return 'other'

COUNTRIES = ['Ефіопія','Бразилія','Колумбія','Гватемала','Гондурас','Індія','Перу','Уганда',"В'єтнам",
 'Кенія','Коста-Ріка','Коста-Рика','Мексика','Нікарагуа','Панама','Сальвадор','Танзанія','Руанда','Бурунді','Ethiopia']
def country_of(p):
    n = p['name_uk'] or ''
    for c in COUNTRIES:
        if c.lower() in n.lower():
            return 'Коста-Ріка' if c=='Коста-Рика' else ('Ефіопія' if c=='Ethiopia' else c)
    return None

def composition(p):
    n=(p['name_uk'] or '').lower()
    if is_aroma(p): return 'Купаж (арабіка/робуста)'
    if '100% арабіка' in n or '100% арабика' in n or 'arabica blend' in n:
        return '100% арабіка'
    if 'робуста 100' in n or 'robusta' in n and 'blend' in n: return 'Робуста'
    if 'blend' in n or 'купаж' in n: return 'Купаж (арабіка/робуста)'
    return None

def categories_of(p):
    cats=set(); t=ptype(p)
    if t=='beans': cats.add('kava-v-zernakh')
    if t=='ground': cats.add('svizhomelena-kava')
    if t=='ncap': cats.add('kapsuly-nespresso')
    if t=='dcap': cats.add('kapsuly-dolce-gusto')
    if t=='drink': cats.add('napoyi-v-kapsulakh')
    if t=='ese': cats.add('monodozy-ese')
    if is_monosort(p): cats.add('arabika-monosorty')
    if is_aroma(p): cats.add('aromatyzovana-kava')
    if is_blend(p) and t in ('ncap','dcap','ese','cap'): cats.add('kavovi-kupazhi')
    if is_decaf(p): cats.add('kava-bez-kofeinu')
    if is_business(p) or (t=='beans' and (p['params'].get('Вес')=='1000')):
        cats.add('kava-dlya-biznesu')
    return cats

PRIMARY_ORDER=['kava-v-zernakh','svizhomelena-kava','kapsuly-nespresso','kapsuly-dolce-gusto',
 'napoyi-v-kapsulakh','monodozy-ese','arabika-monosorty','aromatyzovana-kava','kavovi-kupazhi','kava-bez-kofeinu','kava-dlya-biznesu']

# ---------- packaging / variant label ----------
def pack_count(p):
    # Кількість чалдів у коробці для E.S.E.-монодоз. Джерело істини — параметр
    # «Количество в упаковке» (у назві може бути «50 х 7 г» без «шт» → regex не ловить).
    q=p['params'].get('Количество в упаковке (шт.)') or p['params'].get('Количество в упаковке')
    if q and str(q).strip().isdigit() and int(q)>0: return int(q)
    m=re.search(r'(\d+)\s*шт', p['name_uk'] or '')
    if m: return int(m.group(1))
    return None
def pack_label(p):
    n=p['name_uk'] or ''
    m=re.search(r'(\d+)\s*шт', n)
    if m: return f"{m.group(1)} шт"
    m=re.search(r'(\d+)\s*кг', n)
    if m: return f"{m.group(1)} кг"
    w=p['params'].get('Вес')
    if w=='1000': return '1 кг'
    if ptype(p)=='ese':                       # коробка «50 х 7 г» → «50 шт» з параметра
        q=pack_count(p)
        if q and q>1: return f"{q} шт"
    return None
def pack_sort(p):
    m=re.search(r'(\d+)\s*шт', p['name_uk'] or '')
    if m: return int(m.group(1))
    if ptype(p)=='ese':                       # менша коробка = представник (v0), ціна↔кількість з ОДНОГО варіанта
        q=pack_count(p)
        if q: return q
    return 999

def clean_title(name, t):
    s = name
    s = re.sub(r'\s*\(.*?\)\s*', ' ', s)          # drop parentheticals
    s = re.sub(r'\s*\d+\s*(кг|г|шт)\b.*$', '', s)  # drop weight/pack tails
    s = re.sub(r'^\s*Ящик\s+', '', s)              # box → drop leading "Ящик"
    s = re.sub(r',\s*$', '', s).strip()
    s = re.sub(r'\s+', ' ', s).strip(' ,')
    # capitalize leading word after removing "Ящик"
    if s[:1].islower():
        s = s[0].upper()+s[1:]
    return s


# ---------- local studio photos (assets/photos) ----------
PHOTO_KEYS=[
 ('"мигдаль, амаретто"','mygdal-amaretto'),('"крем-лікер бейліс"','krem-liker-beilis'),
 ('"ром, ваніль"','rom-vanil'),('"баварський шоколад"','bavarskyi-shokolad'),
 ('"пряний шоколад"','pryanyi-shokolad'),('"ірландський крем"','irlandskyi-krem'),
 ('"лісовий горіх"','lisovyi-horikh'),('"кава"','kava-smak'),
 ('"капучіно"','kapuchyno'),('"капучино"','kapuchyno'),
 ('"тірамісу"','tiramisu'),('"тирамісу"','tiramisu'),
 ('"амаретто"','amaretto'),('"ананас"','ananas'),('"банан"','banan'),('"бейліс"','beilis'),
 ('"ваніль"','vanil'),('"вишня"','vyshnya'),('"віскі"','viski'),('"карамель"','karamel'),
 ('"кокос"','kokos'),('"кориця"','korytsya'),('"малина"','malyna'),('"мигдаль"','mygdal'),
 ('"полуниця"','polunytsya'),('"ром"','rom'),('"снікерс"','snikers'),('"трюфель"','tryufel'),
 ('сідамо fwa','sidamo-fwa'),('сідамо','sidamo'),('теппі','teppi'),('джимма','dzhymma'),
 ('limu','limu'),('ліму','limu'),('жовтий бурбон','zhovtyi-burbon'),('карнавал','karnaval'),
 ('маджано','madzhano'),('черрадо','cherrado'),('сантос','santos'),('бурунді','burundi'),
 ('уеуетенанго','ueuetenango'),('гондурас','honduras'),('кенія','keniya'),('кения','keniya'),
 ('декаф','kolumbiya-dekaf'),('папаян','kolumbiya-papayan'),('медельїн','kolumbiya-medelin'),('колумбія супремо','kolumbiya-papayan'),
 ('коста','kosta-rika'),('мексика','meksyka'),('марагоджип','maragodzhyp'),('нікарагуа','nikaragua'),
 ('панама','panama'),('перу','peru'),('руанда','ruanda'),('сальвадор','salvador'),
 ('танзанія','tanzaniya'),('індія','indiya'),
]
def local_photo(title):
    tl=(title or '').lower()
    for k,fn in PHOTO_KEYS:
        if k in tl:
            p=os.path.join(SITE,'assets','photos',fn+'.jpg')
            if os.path.exists(p):
                return 'assets/photos/'+fn+'.jpg'
    return None

# ---------- build cards ----------
def build_cards():
    prods = load()
    from collections import defaultdict
    groups=defaultdict(list); solo=[]
    for p in prods:
        (groups[p['group_id']].append(p) if p['group_id'] else solo.append(p))
    cards=[]
    def make_card(variants, forced_type=None):
        vs0=sorted(variants, key=pack_sort)
        v0=vs0[0]   # smallest retail pack is the representative (not the "Ящик" box)
        t=forced_type or ptype(v0)
        # E.S.E.: на Prom кожен NPROMAX-товар = ОДНА роздрібна коробка (50 шт). У експорт-фіді
        # лишається фантомна групована «150 шт» (SKU -1, ×3 ціна) — на сторінці/у пошуку Prom її НЕМАЄ.
        # Прибираємо її, лишаємо найменшу коробку (нічний ре-sync знову підтягне фід — тому фільтр тут).
        if t=='ese':
            packs=[pc for pc in (pack_count(x) for x in variants) if pc]
            mn=min(packs) if packs else None
            if mn is not None:
                variants=[x for x in variants if pack_count(x)==mn] or variants
                vs0=sorted(variants, key=pack_sort); v0=vs0[0]
        title=clean_title(v0['name_uk'], t)
        slug=translit(title)[:70].strip('-')
        # display-нормалізація мови (ПІСЛЯ slug — URL стабільні)
        for a,b in [('Арабика','Арабіка'),('Ethiopia Limu','Ефіопія Ліму'),('Коста-Рика','Коста-Ріка'),('Тирамісу','Тірамісу'),('Капучино','Капучіно')]:
            title=title.replace(a,b)
        # main image: local studio photo if mapped, else feed image
        lp=local_photo(title) if t in ('beans','ground') else None
        if not lp:
            pp=os.path.join(SITE,'assets','photos','p',slug+'.jpg')
            if os.path.exists(pp): lp='assets/photos/p/'+slug+'.jpg'
        img=lp or (v0['images'][0] if v0['images'] else '')
        gallery=[lp] if lp else v0['images'][:5]
        prices=[x['price'] for x in variants if x['price']]
        cats=set()
        for x in variants: cats|=categories_of(x)
        primary=next((c for c in PRIMARY_ORDER if c in cats), 'kava-v-zernakh')
        # variants sorted
        vs=sorted(variants, key=pack_sort)
        card={
            'slug':slug,'title':title,'type':t,'primary':primary,'cats':cats,
            'image':img,'images':gallery,
            'price_min':min(prices) if prices else 0,'price_max':max(prices) if prices else 0,
            'available':any(x['available'] for x in variants),
            'oldprice':v0.get('oldprice'),
            'country':country_of(v0),'composition':composition(v0),
            'decaf':is_decaf(v0),'aroma':is_aroma(v0),'monosort':is_monosort(v0),
            'business':any(is_business(x) for x in variants) or t in ('beans','ground'),
            'desc':v0.get('desc_uk') or '','vendor_code':v0.get('vendor_code'),
            'params':v0.get('params',{}),
            'variants':[{'label':pack_label(x) or 'упаковка','price':x['price'],'sku':x['vendor_code'],'q':x['quantity'],
                         'pack':(pack_count(x) if t=='ese' else None)} for x in vs],
            'roast':v0['params'].get('Степень обжарки'),
            'caffeine':v0['params'].get('Кофеин'),
        }
        # грн/чашка для E.S.E.: ціна коробки ÷ к-сть чалдів у ТІЙ САМІЙ коробці (усі варіанти дають однакову цифру)
        cups=[v['price']/v['pack'] for v in card['variants'] if v.get('pack') and v.get('price')]
        card['per_cup']=min(cups) if cups else None
        return card
    seen_slugs={}
    def dedupe(card):
        s=card['slug'];
        if s in seen_slugs:
            seen_slugs[s]+=1; card['slug']=f"{s}-{seen_slugs[s]}"
        else: seen_slugs[s]=0
        return card
    for gid,items in groups.items():
        if any(is_capsule(i) or is_ese(i) for i in items):
            cards.append(dedupe(make_card(items)))
        else:
            beans=[i for i in items if not is_ground(i)]
            ground=[i for i in items if is_ground(i)]
            if beans: cards.append(dedupe(make_card(beans,'beans')))
            if ground: cards.append(dedupe(make_card(ground,'ground')))
    for p in solo:
        cards.append(dedupe(make_card([p])))
    # format siblings link (beans<->ground same base)
    return cards

if __name__=='__main__':
    cards=build_cards()
    from collections import Counter
    print("cards:",len(cards))
    print("by type:",Counter(c['type'] for c in cards))
    catc=Counter()
    for c in cards:
        for cat in c['cats']: catc[cat]+=1
    print("by category:",dict(catc))
    print("sample slugs:")
    for c in cards[:6]: print("  ",c['slug'],'|',c['title'][:50],'|',c['price_min'])
