#!/usr/bin/env python3
"""HubHug v7 — デジタル庁 × Apple HIG × Material 3 を参考に作り直した版。

  python3 v7/build.py      → v7/*.html（7ページ）を書き出す

v6 を複製して作り直したもの。v7 は本体の assets/ を参照しない（style.css / site.js / img/ を同梱）。
文言は本体 build.py から複製。v7 の文言はこのファイルで直す。
見出しの "|" は文節の区切り（<span class="np">。スマホで文節の途中で折れない）、"/" は改行。
"""
import hashlib, os, re
HERE = os.path.dirname(os.path.abspath(__file__))
try:
    from PIL import Image
except ImportError:
    Image = None


def np(s):
    return ''.join('<br>' if p == '/' else f'<span class="np">{p}</span>' for p in re.split(r'\||(/)', s) if p)


def ph(s):
    """"|" だけで文節に分ける（"/" を改行にしない。RE/MAX など）"""
    return ''.join(f'<span class="np">{p}</span>' for p in s.split('|'))


# 線のアイコン（24px グリッド・Material Symbols Rounded に寄せた太さ）
ICONS = {
    'arrow': '<path d="M5 12h14M13 6l6 6-6 6"/>',
    'down': '<path d="M12 5v14M6 13l6 6 6-6"/>',
    'menu': '<path d="M4 7h16M4 12h16M4 17h16"/>',
    'close': '<path d="M6 6l12 12M18 6 6 18"/>',
    'check': '<path d="m5 12.5 4.5 4.5L19 7.5"/>',
    'x': '<path d="M7 7l10 10M17 7 7 17"/>',
    'chat': '<path d="M20 11.5a7.5 7.5 0 0 1-10.9 6.7L4 19.5l1.3-4.6A7.5 7.5 0 1 1 20 11.5z"/><path d="M8.5 11.5h.01M12 11.5h.01M15.5 11.5h.01"/>',
    'home': '<path d="M4 10.5 12 4l8 6.5V20h-5v-6H9v6H4z"/>',
    'info': '<circle cx="12" cy="12" r="9"/><path d="M12 11v5.5M12 7.8v.2"/>',
    'grid': '<rect x="4" y="4" width="7" height="7" rx="1.5"/><rect x="13" y="4" width="7" height="7" rx="1.5"/><rect x="4" y="13" width="7" height="7" rx="1.5"/><rect x="13" y="13" width="7" height="7" rx="1.5"/>',
    'shield': '<path d="M12 3 5 6v5.5c0 4.4 3 8 7 9.5 4-1.5 7-5.1 7-9.5V6z"/><path d="m9 12 2.2 2.2L15.5 10"/>',
    'chef': '<path d="M7.5 20h9M7.5 16.5h9M7.5 20v-6A4 4 0 0 1 8 6.1a4.5 4.5 0 0 1 8 0 4 4 0 0 1 .5 7.9v6"/>',
    'store': '<path d="M4 9.5 5.5 5h13L20 9.5M4 9.5h16M4 9.5a2.7 2.7 0 0 0 5.3 0 2.7 2.7 0 0 0 5.4 0 2.7 2.7 0 0 0 5.3 0M5.5 12.5V20h13v-7.5M10 20v-4.5h4V20"/>',
    'bldg': '<path d="M5 20V4h9v16M14 9h5v11M3 20h18M8.5 8h2M8.5 12h2M8.5 16h2"/>',
    'mail': '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m4 7 8 6 8-6"/>',
    'sunrise': '<path d="M3 18h18M7 18a5 5 0 0 1 10 0M12 6v4M5.3 10.3l1.4 1.4M18.7 10.3l-1.4 1.4M9 21h6"/>',
    'sun': '<circle cx="12" cy="12" r="4"/><path d="M12 2.5v2M12 19.5v2M2.5 12h2M19.5 12h2M5.3 5.3l1.4 1.4M17.3 17.3l1.4 1.4M5.3 18.7l1.4-1.4M17.3 6.7l1.4-1.4"/>',
    'moon': '<path d="M19.5 14.5A7.5 7.5 0 0 1 9.5 4.5a7.5 7.5 0 1 0 10 10z"/>',
    'alert': '<path d="M12 4 2.8 19.5h18.4z"/><path d="M12 10v4M12 16.8v.2"/>',
    'coin': '<circle cx="12" cy="12" r="8.5"/><path d="M9 8l3 4 3-4M12 12v5M9.5 13.5h5"/>',
    'chart': '<path d="M3 20h18M6.5 16v-4M11.5 16V8M16.5 16v-6"/>',
    'users': '<circle cx="9" cy="8" r="3"/><path d="M3.5 19a5.5 5.5 0 0 1 11 0M16 5.2a3 3 0 0 1 0 5.6M17.5 13.6A5.5 5.5 0 0 1 20.5 19"/>',
    'trend': '<path d="M3 17l6-6 4 4 8-8M15 7h6v6"/>',
    'clock': '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3.2 2"/>',
    'list': '<path d="M10 6h10M10 12h10M10 18h10M4 6l1 1 2-2M4 12l1 1 2-2M4 18l1 1 2-2"/>',
    'doc': '<path d="M7 3h7l4 4v14H7z"/><path d="M14 3v4h4M10 12h5M10 16h5"/>',
    'exit': '<path d="M14 4H6v16h8M10 12h10M17 9l3 3-3 3"/>',
}


def ic(name):
    return f'<svg class="i" viewBox="0 0 24 24" aria-hidden="true">{ICONS[name]}</svg>'


def arrow_link(href, text):
    return f'<a class="alink" href="{href}">{text}{ic("arrow")}</a>'


def img(f, alt='', eager=False):
    wh = ''
    if Image:
        try:
            w, h = Image.open(os.path.join(HERE, 'img', f)).size
            wh = f' width="{w}" height="{h}"'
        except OSError:
            pass
    load = 'fetchpriority="high"' if eager else 'loading="lazy"'
    return f'<img src="img/{f}" alt="{alt}"{wh} {load} decoding="async">'


NAV = [('about.html', '私たちについて', 'info'), ('service.html', 'サービス', 'grid'),
       ('scheme.html', '家主公認スキーム', 'shield'), ('chefs.html', '開業したい方へ', 'chef'),
       ('owners.html', '店舗オーナー・家主の方へ', 'store')]

LOGO = '''<svg viewBox="0 0 30 36" fill="none" stroke-width="2.2" stroke-linecap="round" aria-hidden="true">
<path d="M3 34V15a12 12 0 0 1 24 0v19" stroke="#2451c6"/><path d="M10 34V17a5 5 0 0 1 10 0v17" stroke="#c0622a"/><path d="M1 34h28" stroke="#191c22"/></svg>'''


LOGO_W = '''<svg class="lw" viewBox="0 0 30 36" fill="none" stroke-width="2.4" stroke-linecap="round" aria-hidden="true">
<path d="M3 34V15a12 12 0 0 1 24 0v19" stroke="#fff"/><path d="M10 34V17a5 5 0 0 1 10 0v17" stroke="#ffc9a6"/><path d="M1 34h28" stroke="#fff"/></svg>'''


def brand():
    return f'<a class="brand" href="index.html" aria-label="HubHug トップへ">{LOGO}<span><b>HubHug</b><small>SHARE &amp; RESTART</small></span></a>'


def cur(h, fn):
    return ' aria-current="page"' if h == fn else ''


def header(fn):
    links = ''.join(f'<a href="{h}"{cur(h, fn)}>{t}</a>' for h, t, _ in NAV)
    items = [('index.html', 'ホーム', 'home')] + NAV + [('contact.html', 'お問い合わせ', 'mail')]
    dlinks = ''.join(f'<a href="{h}"{cur(h, fn)}>{ic(i)}{t}</a>' for h, t, i in items)
    return f'''<a class="skip" href="#main">本文へスキップ</a>
<header class="hd" id="hd"><div class="wrap hd-in">{brand()}
<nav class="gnav" aria-label="メインメニュー">{links}</nav>
<a class="btn filled sm hd-cta" href="contact.html">お問い合わせ</a>
<button class="menu-btn" id="menu-btn" type="button" aria-label="メニューを開く" aria-expanded="false" aria-controls="drawer">{ic('menu')}<span>メニュー</span></button>
</div></header>
<div class="scrim" id="scrim"></div>
<aside class="drawer" id="drawer" aria-label="メニュー" aria-hidden="true">
<div class="drawer-hd"><p>メニュー</p><button class="icon-btn" id="drawer-close" type="button" aria-label="メニューを閉じる">{ic('close')}</button></div>
<nav aria-label="サイト内のページ">{dlinks}</nav>
<a class="btn filled" href="contact.html">{ic('chat')}無料で相談する</a>
</aside>'''


FOOTER = f'''<footer class="ft"><div class="wrap">
<div class="ft-top"><div>{brand()}<p class="tagline">飲食業を好きで始めた人が、<br>最後まで好きでいられる社会へ。</p></div>
<nav class="ft-nav" aria-label="フッターメニュー">
<div><p class="fh">会社について</p><a href="about.html">私たちについて</a><a href="about.html#message">代表メッセージ</a><a href="about.html#partners">連携・支援体制</a><a href="about.html#company">会社概要</a></div>
<div><p class="fh">サービス</p><a href="service.html">サービス一覧</a><a href="scheme.html">家主公認スキーム</a><a href="service.html#fee">料金について</a></div>
<div><p class="fh">あなたの立場から</p><a href="chefs.html">開業したい方へ</a><a href="owners.html">店舗オーナー・家主の方へ</a><a href="contact.html">お問い合わせ</a></div>
</nav></div>
<div class="ft-btm"><span>株式会社HubHug（2026年11月設立予定）／大阪市</span><span>掲載写真はイメージです（代表写真を除く）。</span><span>&copy; 2026 HubHug Inc.</span></div>
</div></footer>'''


def sh(ov, h, p='', center=False, link=None):
    cls = 'sh center' if center else 'sh'
    ov_html = f'<p class="ov">{ov}</p>' if ov else ''
    p_html = f'<p>{p}</p>' if p else ''
    lk = arrow_link(*link) if link else ''
    return f'<div class="{cls}">{ov_html}<h2>{np(h)}</h2>{p_html}{lk}</div>'


def phead(crumb, h1, lead, image=None, alt='', toc=()):
    toc_html = ''
    if toc:
        chips = ''.join(f'<a class="chip" href="#{i}">{ic("down")}{t}</a>' for i, t in toc)
        toc_html = f'<nav class="toc" aria-label="このページの内容"><span class="toc-lb">このページの内容</span>{chips}</nav>'
    fig = f'<figure class="phead-media">{img(image, alt, eager=True)}</figure>' if image else ''
    return f'''<section class="phead"><div class="wrap">
<nav class="crumb" aria-label="パンくずリスト"><span>現在位置：</span><ol><li><a href="index.html">ホーム</a></li><li aria-current="page">{crumb}</li></ol></nav>
<h1>{np(h1)}</h1><p class="lead">{lead}</p>{toc_html}{fig}
</div></section>'''


def cta(h='まずは、|お話を|聞かせてください。',
        p='間借りで始めたい方も、空き時間を活かしたい店舗オーナー様も、物件をお持ちの家主様も。ご相談は無料です。', q=''):
    return f'''<section class="sec"><div class="wrap"><div class="cta-box">
<div><h2>{np(h)}</h2><p>{p}</p></div>
<div class="btns"><a class="btn inverse" href="contact.html{q}">{ic('chat')}無料で相談する</a><a class="btn inverse-o" href="service.html">サービスを見る</a></div>
</div></div></section>'''


def cards(items, cls='cards c3', card='card'):
    """items: (番号, アイコン, 見出し, 本文)"""
    out = ''.join(f'<li class="{card}"><div class="card-top"><span class="ic">{ic(i)}</span><span class="num">{no}</span></div>'
                  f'<h3>{np(h)}</h3><p>{p}</p></li>' for no, i, h, p in items)
    return f'<ul class="{cls}">{out}</ul>'


def steps(items):
    """items: (番号, ラベル, 見出し, 本文)"""
    out = ''.join(f'<li class="step"><span class="no">{no}</span><span class="k">{k}</span><h3>{h}</h3><p>{p}</p></li>'
                  for no, k, h, p in items)
    return f'<ol class="steps">{out}</ol>'


def checks(items, icon='check'):
    return '<ul class="checks">' + ''.join(f'<li>{ic(icon)}<span class="t">{t}</span></li>' for t in items) + '</ul>'


def ver(f):
    """style.css / site.js の中身が変わるたびに ?v= が変わる（スマホのキャッシュ対策）"""
    with open(os.path.join(HERE, f), 'rb') as fh:
        return hashlib.md5(fh.read()).hexdigest()[:8]


def page(fn, title, desc, body):
    fab = '' if fn == 'contact.html' else f'<a class="fab" id="fab" href="contact.html">{ic("chat")}無料で相談する</a>'
    html = f'''<!DOCTYPE html>
<html lang="ja"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{title}</title><meta name="description" content="{desc}">
<meta property="og:title" content="{title}"><meta property="og:description" content="{desc}"><meta property="og:type" content="website">
<meta name="theme-color" content="#ffffff">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' rx='8' fill='%232451c6'/%3E%3Cpath d='M9 26V15a7 7 0 0 1 14 0v11' fill='none' stroke='%23fff' stroke-width='2.4' stroke-linecap='round'/%3E%3C/svg%3E">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;500;700&display=swap" rel="stylesheet">
<link href="https://fonts.googleapis.com/css2?family=Shippori+Mincho+B1:wght@500;700&display=swap&text=0123456789,.%25" rel="stylesheet">
<link rel="stylesheet" href="style.css?v={ver('style.css')}">
</head><body>
{header(fn)}
<main id="main">
{body}
</main>
{FOOTER}
{fab}
<script src="site.js?v={ver('site.js')}"></script>
</body></html>
'''
    with open(os.path.join(HERE, fn), 'w', encoding='utf-8') as f:
        f.write(html)
    print(fn, '%.1fKB' % (len(html.encode()) / 1024))


# =========================================================== index
# 設立前の会社なので、信頼の根拠は「代表の顔と実績」「家主公認の仕組み」「数字の開示」。
# 1画面目で「何の会社か（朝・昼・夜で店を分け合う）」「誰がやるか（代表の顔）」「次の一歩（相談）」を出す。
def aud(href, q, image, alt, icon, tag, h, num, items, act):
    return f'''<article class="aud-card"><figure>{img(image, alt)}<span class="tag">{ic(icon)}{tag}</span></figure>
<div class="aud-body"><h3>{np(h)}</h3>{num}{checks(items)}
<div class="aud-act"><a class="btn filled" href="contact.html{q}">{ic('chat')}{act}</a>{arrow_link(href, '詳しく見る')}</div></div></article>'''


def hx_photo(image, alt, icon, label, cap, pos='center'):
    return f'''<li><figure>{img(image, alt, True).replace('<img ', f'<img style="object-position:{pos}" ', 1)}
<figcaption><span class="tchip">{ic(icon)}{label}</span><span class="cap">{cap}</span></figcaption></figure></li>'''


def journey(no, k, image, alt, h, p):
    return f'''<li><figure>{img(image, alt)}</figure><div class="jb"><div class="jh"><span class="no">{no}</span><span class="k">{k}</span></div>
<h3>{h}</h3><p>{p}</p></div></li>'''


FAQ = [
    ('構想段階でも|相談できますか？', 'はい。業態・希望エリア・時間帯・ご予算が決まっていない段階でも歓迎です。ご相談は無料で、しつこい営業はいたしません。'),
    ('家主の承諾は、|本当に|取れるのですか？', '当社が家主・管理会社様へ事前にご説明し、承諾と契約の形を整えます。承諾をいただいた物件だけで運用します。代表は累計350店舗以上の家主公認店舗をプロデュースしてきました。'),
    ('費用は|どのように|かかりますか？', '間借りシェアは、契約成立時の成約手数料（貸し手様より月額間借り料の1か月分）と、毎月の間借り料を現店舗オーナー様と当社で50%ずつ分けるレベニューシェアです。金額は設立準備中の予定であり、変更となる場合があります。'),
    ('設備の破損や|近隣トラブルが|起きたら？', '清掃、設備、ゴミ、光熱費などのルールと責任の範囲を、あらかじめ契約で明確にします。問題が起きたときは当社が間に立ちます。'),
    ('やむを得ず|撤退することに|なったら？', '造作・設備の価値を査定し、造作譲渡（居抜き売却）で譲渡先を探します。原状回復費用を抑え、手元に資金を残して次の挑戦へ進めるよう支援します。'),
    ('問い合わせたあとの|流れは？', '内容を確認のうえ、3営業日以内に担当者よりご連絡します。やりたい業態や貸し出せる時間帯などを伺い、実現できる形をご提案します。'),
]

faq_html = ''.join(f'<details><summary><span class="q">Q</span><span class="t">{ph(q)}</span></summary><p class="a">{a}</p></details>' for q, a in FAQ)

index = f'''
<section class="hx"><div class="wrap hx-grid">
<div class="hx-head">
<p class="hero-chip"><i></i><span class="t">大阪発｜家主公認の間借り開業</span></p>
<h1 class="display"><span class="np">一つの店を、</span><br><span class="np">時間で</span><span class="np">分け合う。</span></h1>
</div>
<div class="hx-side">
<p class="lead">家主の承諾を得た「間借り」で、初期投資を抑えて開業。営業していない時間を貸す店舗オーナー様には、家賃の補填を。出店から退店まで、一気通貫で伴走します。</p>
<div class="btns"><a class="btn filled" href="contact.html">{ic('chat')}無料で相談する</a><a class="btn tonal" href="service.html">サービスを見る</a></div>
<a class="person" href="about.html#message">{img('portrait.jpg', '代表 青枝 実樹', True)}<span><b>代表　青枝 実樹</b><small>家主公認の店舗 350店舗以上</small></span>{ic('arrow')}</a>
</div>
<ul class="hx-photos">
{hx_photo('am.jpg', '朝：カフェでコーヒーを淹れるスタッフ', 'sunrise', '朝', 'モーニング・コーヒースタンド', '28% center')}
{hx_photo('noon.jpg', '昼：笑顔で調理する料理人', 'sun', '昼', 'ランチ営業・定食・弁当')}
{hx_photo('night.jpg', '夜：焼き鳥を焼く料理人', 'moon', '夜・定休日', 'バー営業・一日店長')}
</ul>
</div></section>

<section class="trust"><div class="wrap"><div class="trust-card">
<p class="trust-lb">代表 青枝が、現場で積み上げてきた実績</p>
<ul class="kpis">
<li><div class="v"><b>350</b><small>店舗以上</small></div><span class="t">{ph("家主公認の|適法店舗・|共同出店の|プロデュース累計")}</span></li>
<li><div class="v"><small>約</small><b>180</b><small>店舗</small></div><span class="t">{ph("大手飲食グループ|大阪支店の|立ち上げから|約2年で展開")}</span></li>
<li><div class="v"><b>10</b><small>年以上</small></div><span class="t">{ph("店舗開発・|飲食特化の|財務・不動産の|実務経験")}</span></li>
<li><div class="v"><small>約</small><b>3</b><small>年</small></div><span class="t">{ph("飲食店支援サイトの|関西代理店として、|造作譲渡の|相談・面談を受託")}</span></li>
</ul>
<div class="allies"><p class="trust-lb">開業後も、専門家と一緒に支えます</p><ul><li><span class="role">財務・税務</span>飲食特化の税理士法人グループ</li><li><span class="role">バックオフィス</span>経理代行パートナー</li><li><span class="role">不動産</span>RE/MAX NOW</li><li><span class="role">物件・顧客情報</span>飲食店支援プラットフォーム</li><li><span class="role">コミュニティ</span>外食虎塾大阪</li></ul>{arrow_link('about.html#partners', '連携・支援体制を見る')}</div>
<p class="note">※実績は代表 青枝の前職・現職を含むキャリア全体での数値です。</p>
</div></div></section>

<section class="sec"><div class="wrap">
{sh('立場から選ぶ', 'あなたの立場で、|何が変わるか。', '借りたい方・貸したい方・物件を持つ方。三者それぞれに、具体的なメリットがあります。')}
<div class="aud">
{aud('chefs.html', '?type=chef', 'card-chef.jpg', '厨房で働く若いスタッフ', 'chef', '開業したい方', '初期投資を抑えて、/自分の店を。',
     '<div class="aud-num"><small>月商30万円の場合の試算</small><strong>手残り 約<b>8</b>万円 / 月</strong><span class="fn">間借り料 月10万円・食材原価30%で試算。収益を保証するものではありません。</span></div>',
     ['内装・厨房は、すでにある店舗を使う', '家主公認だから、突然の退去の心配がない', '実績ができたら、実店舗への独立まで支援'], '開業の相談をする')}
{aud('owners.html', '?type=owner', 'card-owner.jpg', 'カウンターの職人', 'store', '店舗オーナー', '空いている時間で、/家賃を|軽くする。',
     '<div class="aud-num"><small>間借り料 月10万円の場合</small><strong>オーナー様の取り分 <b>5</b>万円 / 月</strong><span class="fn">年間60万円。家賃の大きな補填になります。</span></div>',
     ['借り手の募集から毎月の回収まで、当社が行う', '清掃・設備・ゴミのルールを契約で明確に', '移転・撤退の際は、造作譲渡で支援'], '空き時間の相談をする')}
{aud('owners.html#landlord', '?type=landlord', 'bldg.jpg', '小さな店が入った角地の建物', 'bldg', '家主・管理会社', '承諾のうえで、/物件の価値を|守る。',
     '<div class="aud-num"><small>運用するのは</small><strong class="txt">事前に承諾をいただいた物件だけ</strong><span class="fn">知らないうちに又貸しされる状態をなくします。</span></div>',
     ['利用者・利用時間・責任範囲を契約で把握できる', 'テナントの家賃負担が軽くなり、退去リスクが下がる', '間借りで実績を出した事業者が、次のテナント候補に'], '物件の相談をする')}
</div></div></section>

<section class="sec tint"><div class="wrap">
{sh('サービスの全体像', '入り口から出口まで、|一本の線で|伴走する。', '間借りで始め、実績をつくり、自分の店へ。万が一のときも、手元に資金を残して再起できるように。', link=('service.html', 'サービスの詳細と料金を見る'))}
<ol class="journey">
{journey('01', '入り口', 'svc1.jpg', '厨房で調理する料理人', '間借りシェア「HubHug」', '既存店舗の朝・昼・夜の空き時間で、初期投資をかけずに開業。テスト販売とファンづくりの場に。')}
{journey('02', '成長', 'svc2.jpg', 'ベーカリーの店先', '実店舗への出店サポート', '飲食店舗に特化した物件探し、融資・補助金の獲得支援、内装・厨房・仕入れ業者のご紹介まで。')}
{journey('03', '出口', 'exit.jpg', '設備が残ったままの食堂', '再起型の退店サポート', 'スピーディーな造作譲渡（居抜き売却）で原状回復費用を抑え、手元に資金を残して次の挑戦へ。')}
</ol></div></section>

<section class="sec"><div class="wrap hubwrap">
<div>{sh('家主公認', '「無断転貸」の壁を、|正面から|越える。')}
<div class="prose"><p>店舗の賃貸借契約の多くは、無断での転貸（又貸し）を禁じています。家主に知らせないままの間借りは、発覚すれば即時退去のリスクと隣り合わせです。</p>
<p>HubHugは、家主・現店舗オーナー・間借り出店者の三者で、公式な承諾と契約を結びます。</p></div>
{checks(['業務委託または転貸承諾を、家主から公式に取得', '責任の範囲を、契約で明確化', '間借り料は、デポジットと自動振替で当社が管理'])}
{arrow_link('scheme.html', '家主公認スキームを見る')}</div>
<div class="triad" role="img" aria-label="HubHugが家主・現店舗オーナー・間借り出店者の三者をつなぐ図">
<svg class="lines" viewBox="0 0 100 130" aria-hidden="true"><path d="M50 60 50 12M50 60 21 96M50 60 79 96"/></svg>
<div class="nd n1"><span class="ph">{img('bldg.jpg')}</span><b>家主・管理会社</b><small>活用を承諾</small></div>
<div class="nd core"><span class="ph">{LOGO_W}<b>HubHug</b></span><small>交渉・契約・決済を担う</small></div>
<div class="nd n2"><span class="ph">{img('card-owner.jpg')}</span><b>現店舗オーナー</b><small>空き時間を貸す</small></div>
<div class="nd n3"><span class="ph">{img('card-chef.jpg')}</span><b>間借り出店者</b><small>初期投資を抑えて開業</small></div>
</div>
</div></section>

<section class="sec tint"><div class="wrap"><div class="msg">
<figure class="pf">{img('portrait.jpg', '株式会社HubHug 代表 青枝 実樹')}</figure>
<div>{sh('代表メッセージ', '飲食業を|好きで始めた人が、/最後まで|好きでいられる|社会を。')}
<div class="prose"><p>祖父と父は、たこ焼き・お好み焼きの店を営んでいました。飲食業の厳しさは、身をもって知っています。</p>
<p>店舗開発の現場で、腕と志のある料理人が資金の問題だけで立ち上がれなくなるのを、数多く見てきました。だからこそ、入り口と出口の両方を軽くする仕組みを、自分の手でつくります。</p></div>
<p class="sig">株式会社HubHug　代表<b>青枝 実樹</b></p>
<ol class="path">
<li><span class="y">2015</span><span class="t">店舗流通ネット（東証プライム上場グループ）で飲食店舗開発</span></li>
<li><span class="y">2020</span><span class="t">飲食特化の税理士法人グループで財務・融資を支援</span></li>
<li><span class="y">2023</span><span class="t">RE/MAX NOW エージェントとして活動開始</span></li>
<li><span class="y">2024</span><span class="t">大手飲食グループ 大阪支店の立ち上げに参画</span></li>
<li><span class="y">2025</span><span class="t">飲食経営塾「外食虎塾大阪」の事務局</span></li>
</ol>
{arrow_link('about.html#message', '代表メッセージと経歴を読む')}</div>
</div></div></section>

<section class="sec"><div class="wrap">
{sh('よくあるご質問', 'ご相談の前に、|よく聞かれること。', '', True)}
<div class="faq">{faq_html}</div>
</div></section>

<section class="sec pt0"><div class="wrap"><div class="cta2">
<figure>{img('tenjinbashi.jpg', '大阪・天神橋筋商店街')}</figure>
<div class="body"><p class="ov">まずは大阪市内から</p><h2>{np('まずは、|お話を|聞かせてください。')}</h2>
<p>間借りで始めたい方も、空き時間を活かしたい店舗オーナー様も、物件をお持ちの家主様も。</p>
<ul class="assure2">
<li>{ic('check')}<span class="t">ご相談は無料です</span></li>
<li>{ic('check')}<span class="t">3営業日以内にご返信します</span></li>
<li>{ic('check')}<span class="t">しつこい営業はいたしません</span></li>
</ul>
<div class="btns"><a class="btn inverse" href="contact.html">{ic('chat')}無料で相談する</a><a class="btn inverse-o" href="service.html">サービスを見る</a></div>
</div></div></div></section>
'''

# =========================================================== about
about = phead('私たちについて', '私たちについて', '食で関西を盛り上げたい。飲食店開業のハードルを下げ、成功確率を高める。それがHubHugの出発点です。',
              'about.jpg', '大衆酒場の店先とお客様',
              [('name', '社名の由来'), ('message', '代表メッセージ'), ('career', '代表の歩み'), ('partners', '連携・支援体制'), ('roadmap', 'ロードマップ'), ('company', '会社概要')]) + f'''
<section class="sec" id="name"><div class="wrap split">
<div>{sh('社名の由来', '「Hub」で|つなぎ、/「Hug」で|支える。')}</div>
<div><div class="hubhug">
<div class="card"><p class="word">Hub<small>つなぐ</small></p><p>借りたい料理人、貸したい店舗、物件を持つ家主。三者をつなぐ結節点になること。</p></div>
<div class="card"><p class="word">Hug<small>支える</small></p><p>手数料だけを受け取って放置するのではなく、契約・財務・経営まで、抱きしめるように伴走すること。</p></div>
</div>
<div class="prose" style="margin-top:24px"><p>情報を仲介するだけの仕組みではなく、人が間に立つ「温かいプラットフォーム」でありたい。社名にはその意思を込めました。</p></div></div>
</div></section>

<section class="sec tint" id="message"><div class="wrap"><div class="msg">
<figure class="pf">{img('portrait.jpg', '株式会社HubHug 代表 青枝 実樹')}</figure>
<div>{sh('代表メッセージ', '大切な店が、|ある日突然|なくなる。/その喪失を、|減らしたい。')}
<div class="prose"><p>祖父と父は、かつてたこ焼き・お好み焼きの店を営んでいました。飲食業の厳しさは、身をもって知っています。</p>
<p>店舗開発の仕事に就いてからは、志と確かな腕を持ちながら、初期の資金ショートや高額な家賃、撤退時の原状回復費用で多額の負債を背負い、二度と立ち上がれなくなる料理人や経営者を、数多く目の当たりにしてきました。</p>
<p>通っていたお気に入りの店が、ある日突然閉店したこともあります。もし、営業時間をシェアできる仕組みや、傷口を広げずに撤退・再起できるセーフティネットがあれば、あの店は消えずに済んだのではないか。そう強く思いました。</p>
<p>飲食業が好きで、飲食業を始めた方が、最後まで飲食業を好きでいられる社会を創る。これは、私の生涯をかけたミッションです。</p></div>
<p class="sig">株式会社HubHug　代表<b>青枝 実樹</b></p></div>
</div></div></section>

<section class="sec" id="career"><div class="wrap read">
{sh('経歴', '代表の歩み')}
<ol class="tl">
<li><span class="y">2015</span><div><h3>{ph("店舗流通ネット株式会社|（東証プライム上場グループ）|入社")}</h3><p>飲食店舗開発の基礎を学び、造作譲渡（居抜き）のノウハウと家主交渉の実務を修得。</p></div></li>
<li><span class="y">2020</span><div><h3>{ph("飲食特化の|税理士法人グループ会社へ")}</h3><p>財務・融資・出退店スキームのコンサルティング業務に従事。</p></div></li>
<li><span class="y">2023</span><div><h3>{ph("RE/MAX NOW|エージェントとして|活動開始")}</h3><p>世界最大級の不動産ネットワークに登録。飲食開業希望者への提案力を強化。</p></div></li>
<li><span class="y">2024</span><div><h3>{ph("大手飲食グループ|大阪支店の|立ち上げに参画")}</h3><p>業務委託契約やサブリースによる出店スキームを自ら構築。ビルオーナー・管理会社との合意形成を先導し、約2年で関西圏約180店舗の展開に貢献。</p></div></li>
<li><span class="y">2025</span><div><h3>{ph("レンタルスペース共同経営／|飲食経営塾の|事務局に")}</h3><p>大阪・十三でレンタルスペース「Tipi」の共同経営を開始。飲食経営塾「外食虎塾大阪」の事務局を務める。</p></div></li>
<li><span class="y">2026</span><div><h3>{ph("株式会社HubHug|設立準備")}</h3><p>出店から退店までをトータルで支える新会社の設立へ。</p></div></li>
</ol></div></section>

<section class="sec tint" id="partners"><div class="wrap">
{sh('連携', '連携・支援体制', '代表がキャリアを通じて築いてきた専門家・組織との連携を軸に、事業を展開します。')}
<ul class="cards c3">
<li class="card"><span class="role">物件・顧客情報</span><h3>飲食店支援プラットフォーム</h3><p>国内最大級の飲食店支援サイトの関西代理店として、造作譲渡を希望する店舗オーナーの相談・面談業務を約3年継続して受託。</p></li>
<li class="card"><span class="role">不動産ネットワーク</span><h3>RE/MAX NOW</h3><p>世界110か国以上で展開する不動産ネットワーク。関西圏の店舗物件・ビルオーナーの情報網を活用します。</p></li>
<li class="card"><span class="role">財務・税務</span><h3>飲食特化の税理士法人グループ</h3><p>創業融資のための事業計画策定から、税務・財務コンサルティングまでを連携して提供。</p></li>
<li class="card"><span class="role">バックオフィス</span><h3>経理代行パートナー</h3><p>開業者が最も不安を抱える経理・バックオフィス業務をまるごとカバーする体制を構築。</p></li>
<li class="card"><span class="role">教育・コミュニティ</span><h3>外食虎塾大阪</h3><p>関西を代表する飲食チェーン経営者が集う経営塾。事務局として、貸し手店舗の開拓と独立志望者への接点を持ちます。</p></li>
<li class="card"><span class="role">実務アライアンス</span><h3>大手飲食グループ</h3><p>グループ内の既存店舗や開発物件を、モデル店舗として優先的に提供・シェアいただく協力体制。</p></li>
</ul></div></section>

<section class="sec" id="roadmap"><div class="wrap">
{sh('ロードマップ', '大阪から、|関西へ。|そして全国へ。', '大阪は日本屈指の飲食店激戦区。空き時間を活用できている店舗は、まだごくわずかです。')}
{steps([('1', '大阪', '大阪モデルの確立・検証', '大阪市内で、家主公認の間借りモデルを確立します。'),
        ('2', '関西圏', '関西圏への展開', '大阪・兵庫・京都・奈良・滋賀・和歌山へ。'),
        ('3', '全国', '全国展開・プラットフォーム化', '主要都市へ拡大し、全国の眠れる空き時間をつなぎます。')])}
</div></section>

<section class="sec tint" id="company"><div class="wrap read">
{sh('会社情報', '会社概要')}
<div class="dl-card"><dl class="dl">
<div><dt>会社名</dt><dd>株式会社HubHug（ハブハグ）</dd></div>
<div><dt>設立</dt><dd>2026年11月（予定）</dd></div>
<div><dt>代表者</dt><dd>青枝 実樹</dd></div>
<div><dt>所在地</dt><dd>大阪府大阪市（予定）</dd></div>
<div><dt>事業内容</dt><dd>間借りシェアサービス「HubHug」の運営／飲食店舗の出店サポート（不動産仲介・融資支援）／退店サポート（造作譲渡）</dd></div>
</dl></div></div></section>
''' + cta()


# =========================================================== service
def svc(no, k, image, alt, h, p, items, link='', rev=False):
    return f'''<article class="svc{' rev' if rev else ''}"><figure class="fig">{img(image, alt)}</figure>
<div class="body"><p class="label-chip"><span class="n">{no}</span>{k}</p><h3>{np(h)}</h3><p>{p}</p>{checks(items)}{link}</div></article>'''


def times(items):
    out = ''.join(f'<li class="card"><div class="card-top"><span class="ic">{ic(i)}</span></div><h3>{h}</h3><p>{p}</p></li>' for i, h, p in items)
    return f'<ul class="cards times">{out}</ul>'


service = phead('サービス', 'サービス', '入り口の「間借り」から、成長の「実店舗出店」、出口の「造作譲渡」まで。飲食店のライフサイクルすべてに伴走します。',
                'hero.jpg', '客で賑わう居酒屋のカウンター',
                [('services', '三つのサービス'), ('timeshare', '時間で分け合う'), ('fee', '料金について'), ('comparison', '他の選択肢との違い')]) + f'''
<section class="sec" id="services"><div class="wrap">
{sh('三つのサービス', '飲食店の一生に、|三つの支えを。')}
{svc('01', '入り口', 'svc1.jpg', '窓辺の厨房で調理する料理人', '間借りシェアサービス|「HubHug」',
     '既存飲食店の営業していない時間帯を、開業したい料理人へ。家主の承諾を得たうえで、貸し手と借り手をつなぎ、契約から毎月の決済管理までを担います。',
     ['内装投資ゼロで、すぐに営業を開始', '家主・貸し手・借り手の三者合意で、退去リスクなし', '間借り料の回収は、デポジットと自動振替で管理', '原価管理や集客のご相談にも伴走'],
     arrow_link('scheme.html', '家主公認スキームについて'))}
{svc('02', '成長', 'svc2.jpg', 'ベーカリーの店先', '実店舗への|出店サポート',
     '間借りで実績と自己資金をつくった次の一歩を支えます。飲食店舗に特化した不動産仲介と、融資獲得のための財務サポートをワンストップで。',
     ['飲食店舗特化の物件探し・内覧時のチェックポイント支援', '融資・補助金の獲得支援（事業計画、収支シミュレーション）', '内装・厨房設備・仕入れ業者のご紹介', '経理・バックオフィスの支援体制'], rev=True)}
{svc('03', '出口', 'svc3.jpg', '明るい空き区画', '再起型の|退店サポート',
     'やむを得ず撤退する際も、傷口を広げない退店を。造作・設備の価値を査定し、水面下でスピーディーに譲渡先を見つけます。',
     ['造作・設備の価値を査定', '水面下でのスピード売却・譲渡仲介', 'スケルトン戻しの原状回復費用を抑える', '手元に資金を残し、次の挑戦へ'])}
</div></section>

<section class="sec tint" id="timeshare"><div class="wrap">
{sh('時間で分け合う', '一つの店を、|時間で|分け合う。', '夜だけ営業する店の昼。昼だけのカフェの夜。定休日。眠っている時間が、誰かの最初の一歩になります。')}
{times([('sunrise', '朝', 'モーニング、ベーカリー、コーヒースタンド、仕込み利用など。'),
        ('sun', '昼', '居酒屋・バーの昼間を使ったランチ営業。カレー、定食、弁当販売など。'),
        ('moon', '夜・定休日', 'カフェの夜を使ったバー営業、定休日の一日店長など。')])}
</div></section>

<section class="sec" id="fee"><div class="wrap">
{sh('料金', '料金について', '各プロセスで、わかりやすい手数料設計にしています。金額は設立準備中の予定であり、変更となる場合があります。')}
<div class="fee">
<div class="card"><h3>間借りシェア「HubHug」</h3><dl>
<div><dt>成約手数料</dt><dd>契約成立時に、貸し手様より月額間借り料の1か月分</dd></div>
<div class="hl"><dt>月額利用・管理料</dt><dd>毎月の間借り料を、現店舗オーナー様と当社で50%ずつのレベニューシェア。<br>例）間借り料10万円の場合、オーナー様5万円・当社5万円。当社分には、家主交渉、契約の適法性維持、毎月の決済管理が含まれます。</dd></div>
</dl></div>
<div class="card"><h3>実店舗への出店サポート</h3><dl>
<div><dt>不動産仲介手数料</dt><dd>法令で定められた上限（成約賃料の1か月分）</dd></div>
<div><dt>財務・融資サポート</dt><dd>融資・補助金の獲得額に応じた成功報酬</dd></div>
</dl></div>
<div class="card"><h3>退店サポート</h3><dl>
<div><dt>造作譲渡手数料</dt><dd>成約時に30万円（税別）、または譲渡金額の10%（成功報酬）</dd></div>
</dl></div>
</div></div></section>

<section class="sec tint" id="comparison"><div class="wrap">
{sh('比較', '他の選択肢との|違い')}
<div class="tbl-wrap"><table class="cmp">
<thead><tr><th scope="col"><span class="sr">比較項目</span></th><th scope="col" class="us">HubHug</th><th scope="col">マッチング特化型の間借りサービス</th><th scope="col">居抜きでの単独出店</th></tr></thead>
<tbody>
''' + ''.join(f'<tr><th scope="row">{k}</th><td class="us" data-label="HubHug"><span class="t">{a}</span></td><td data-label="マッチング型"><span class="t">{b}</span></td><td data-label="単独出店"><span class="t">{c}</span></td></tr>\n' for k, a, b, c in [
    ('初期投資', 'ほぼ不要', 'ほぼ不要', '数百万〜数千万円規模'),
    ('家主の承諾', '当社が事前に交渉し、公式に取得', '当事者任せになりやすい', '賃貸借契約で締結'),
    ('現場トラブルへの対応', '責任の所在を契約で明確化し、当社が間に立つ', '当事者間での解決が中心', '自己責任'),
    ('経営・財務の支援', '原価管理・集客・融資まで伴走', '対象外のことが多い', '別途、専門家を探す必要'),
    ('独立・撤退時の支援', '出店仲介から造作譲渡まで一貫', '対象外', '別途、業者を探す必要')]) + f'''</tbody></table></div>
<p class="note">※一般的な傾向を整理したもので、個別のサービス内容を示すものではありません。</p>
</div></section>
''' + cta()

# =========================================================== scheme
scheme = phead('家主公認スキーム', '家主公認スキーム', '間借りが広がりきらなかった理由は、法的なリスクにあります。HubHugは、その壁を正面から越えます。',
               'scheme-hero.jpg', '角地の建物と青空',
               [('problem', '間借りの課題'), ('solution', '解決の考え方'), ('structure', '契約の仕組み'), ('strength', 'HubHugの強み')]) + f'''
<section class="sec" id="problem"><div class="wrap">
{sh('間借りの課題', 'なぜ、間借りは|普及しきって|いないのか。', '間借り営業という形は以前からあります。しかし、家主に無断のまま行われる「野良間借り」には、三つの構造的な問題があります。')}
{cards([('01', 'alert', '無断転貸による|契約違反と|即時退去リスク', '多くの賃貸借契約は無断転貸を禁じています（民法612条）。発覚すれば、契約解除・即時退去を求められるおそれがあります。'),
        ('02', 'alert', '責任の所在が|曖昧で、|トラブルが起きやすい', '設備の破損、ゴミ、近隣クレーム、売上管理。問題が起きても誰が責任を負うのかが決まっていません。'),
        ('03', 'alert', '明日、|営業できなくなる|かもしれない', '出店者は常に不安と隣り合わせ。腰を据えたブランドづくりやファンづくりに集中できません。')], card='card warn')}
</div></section>

<section class="sec tint" id="solution"><div class="wrap">
{sh('解決の考え方', '三者が合意した|契約だけを、|扱います。')}
<div class="vs">
<div class="card bad"><span class="role">従来の「野良間借り」</span><h3>{np('家主に|知らせないまま、|当事者だけで|貸し借り')}</h3>
{checks(['無断転貸にあたり、契約違反となるおそれ', '発覚すれば、貸し手の店舗ごと退去のリスク', 'トラブル時の責任の所在が不明確', '金銭のやり取りが当事者任せ'], 'x')}</div>
<div class="card good"><span class="role">HubHugの家主公認スキーム</span><h3>{np('家主・貸し手・借り手の|三者で、|公式に合意')}</h3>
{checks(['業務委託または転貸承諾を、家主から公式に取得', '物件ごとの契約条件に応じて、最適な形を設計', '責任の範囲を契約で明確化', '間借り料はデポジットと自動振替で当社が管理'])}</div>
</div></div></section>

<section class="sec" id="structure"><div class="wrap">
{sh('契約の仕組み', '契約の間に、|当社が入ります。', '当社が契約の間に直接入り、公式な転貸・業務委託として適法な運用を担保します。')}
<div class="tri">
<div class="node"><span class="r">LANDLORD</span><h3>家主・管理会社</h3><p>空き時間の活用を承諾。物件は適法・クリーンに運用されます。</p></div>
<div class="link"><span>承諾・契約</span></div>
<div class="node core"><span class="r">HUBHUG</span><h3>当社</h3><p>家主交渉、契約設計、決済管理、運営のフォローまでを担います。</p></div>
<div class="link"><span>業務委託・転貸</span></div>
<div class="node"><span class="r">OWNER &amp; CHEF</span><h3><span class="np">現店舗オーナー ／</span> <span class="np">間借り出店者</span></h3><p>貸し手は家賃負担を軽減。借り手は初期投資なしで開業。</p></div>
</div></div></section>

<section class="sec tint" id="strength"><div class="wrap">
{sh('HubHugの強み', 'なぜ、|HubHugなら|できるのか。')}
{cards([('01', 'users', '家主交渉の実務経験', '代表は累計350店舗以上の家主公認店舗をプロデュース。ビルオーナーや管理会社と対面で合意を形成してきました。'),
        ('02', 'doc', '契約スキームの構築力', '業務委託、サブリース（転貸借）。物件ごとに異なる条件に合わせ、適法な形を設計します。'),
        ('03', 'coin', '飲食特化の財務知見', '財務・融資の実務経験と、税理士法人との連携により、開業後の経営まで支えます。')])}
<p class="note">※契約形態は物件・契約条件により異なります。個別の法的判断が必要な場合は、連携する専門家とともに対応します。</p>
</div></section>
''' + cta('その物件で、|間借りは|できるのか。/まずは|ご相談ください。', '賃貸借契約の内容や家主様との関係を伺い、実現できる形をご提案します。')


# =========================================================== chefs
def sim(st, h, sales, cost, util, left, memo):
    return f'''<div class="sim"><span class="label-chip">{st}</span><h3>{h}</h3><div class="sales"><b>{sales}</b><small>万円 / 月商</small></div>
<dl><div><dt>食材原価（約30%）</dt><dd>{cost}万円</dd></div><div><dt>間借り料</dt><dd>10万円</dd></div><div><dt>光熱費・雑費（按分）</dt><dd>約{util}万円</dd></div></dl>
<div class="left"><span>手残りの目安</span><p>約<b>{left}</b><small>万円</small></p></div><p class="memo">{memo}</p></div>'''


chefs = phead('開業したい方へ', '開業したい方へ', '数千万円の借金を背負わなくても、自分の店は始められます。まずは間借りで、小さく確かな一歩を。',
              'chefs.jpg', '活気ある厨房で働く料理人',
              [('merit', '間借り開業でできること'), ('simulation', '収支イメージ'), ('flow', 'ご利用の流れ')]) + f'''
<section class="sec" id="merit"><div class="wrap">
{sh('メリット', '間借り開業で、|できること。')}
{cards([('01', 'store', '初期投資ゼロで開業', '内装も厨房設備も、すでにある店舗を使います。物件契約や大きな借入は必要ありません。'),
        ('02', 'coin', '固定費を大幅に抑える', '使う時間帯の分だけの間借り料。売上が読めない開業初期の資金繰りを守ります。'),
        ('03', 'chart', 'テストマーケティング', 'メニュー、価格、立地。実際のお客様で試し、ファンをつくってから次の段階へ進めます。'),
        ('04', 'shield', '家主公認の安心', '家主の承諾を得た契約だから、突然営業できなくなる心配がありません。'),
        ('05', 'users', '数字の不安に伴走', '原価管理や集客の相談、経理・バックオフィスの支援体制をご用意します。'),
        ('06', 'trend', '独立までの道筋', '実績と自己資金ができたら、実店舗へ。物件探しから融資まで続けて支援します。')])}
</div></section>

<section class="sec tint" id="simulation"><div class="wrap">
{sh('シミュレーション', '月商別の|収支イメージ', '間借り料の総額を月10万円とした場合の試算です。実際の金額は店舗・時間帯・営業日数により異なります。')}
<div class="sims">
{sim('STAGE 1', '副業・週末起業から始める', '30', '9', '3', '8', '週2〜3日のランチ営業でも届くライン。固定費の赤字リスクを抑えながら、自分のブランドで商売を始められます。')}
{sim('STAGE 2', '本業として軌道に乗せる', '50', '15', '4', '21', '営業日数を増やし、ファンが定着してきた段階。生活費と次への貯蓄を確保し、実店舗への準備が進みます。')}
{sim('STAGE 3', '人気店として独立直前へ', '90', '27', '6', '47', '連日満席に近い状態。資金を蓄え、万全の状態で自分の店舗のオープンへ。')}
</div>
<p class="note">※上記は一定の前提にもとづく試算であり、収益を保証するものではありません。人件費はご本人の営業を前提に含めていません。</p>
</div></section>

<section class="sec" id="flow"><div class="wrap">
{sh('ご利用の流れ', 'ご利用の流れ')}
{steps([('01', 'STEP 1', '無料相談', 'やりたい業態、希望エリア、時間帯、ご予算を伺います。'),
        ('02', 'STEP 2', '店舗のご提案・内覧', '家主承諾の見込める店舗をご提案。設備や動線を一緒に確認します。'),
        ('03', 'STEP 3', '三者合意・契約・開業', '家主・貸し手・あなたの三者で合意し契約。営業許可の確認を経て開業です。')])}
</div></section>
''' + cta('最初の一歩を、|軽くする。', 'まだ構想段階でもかまいません。お気軽にご相談ください。', '?type=chef')

# =========================================================== owners
owners = phead('店舗オーナー・家主の方へ', '店舗オーナー・|家主の方へ', '店が閉まっている時間も、家賃はかかり続けます。その時間を、無理なく収益に変える仕組みです。',
               'owners.jpg', 'カウンター越しに話す店主とお客様',
               [('owner', '店舗オーナー様へ'), ('timeshare', '貸し出せる時間帯'), ('landlord', '家主・管理会社様へ'), ('flow', 'ご利用の流れ')]) + f'''
<section class="sec" id="owner"><div class="wrap">
{sh('店舗オーナー様へ', '空いている時間が、|家賃を|軽くする。', '物価高と固定費の負担が続くなか、完全撤退の前にできることがあります。')}
{cards([('01', 'coin', '毎月の固定収入', '間借り料10万円の場合、オーナー様の取り分は月5万円（年間60万円）。家賃の大きな補填になります。'),
        ('02', 'clock', '手間がかからない', '借り手の募集、家主への交渉、契約、毎月の回収まで当社が行います。'),
        ('03', 'shield', '契約違反の心配がない', '家主の承諾を得たうえで進めるため、無断転貸にはなりません。'),
        ('04', 'list', 'トラブルを未然に防ぐ', '清掃、設備、ゴミ、光熱費。ルールと責任の範囲を契約で明確にします。'),
        ('05', 'doc', '金銭トラブルを防ぐ', '間借り料はデポジットと自動振替で当社が回収。未払いの不安を減らします。'),
        ('06', 'exit', 'いざという時の出口', '移転・撤退の際は、造作譲渡で原状回復費用を抑え、手元に資金を残す退店を支援します。')])}
</div></section>

<section class="sec tint" id="timeshare"><div class="wrap">
{sh('時間で分け合う', '貸し出せる|時間帯の例')}
{times([('sunrise', '朝', '開店前の時間を、モーニングやコーヒースタンドに。'),
        ('sun', '昼', '夜営業の店舗の昼間を、ランチ営業に。'),
        ('moon', '夜・定休日', '昼営業の店舗の夜や、定休日の終日利用に。')])}
</div></section>

<section class="sec" id="landlord"><div class="wrap media-split">
<figure class="fig">{img('landlord.jpg', '青空のビル街')}</figure>
<div>{sh('家主・管理会社様へ', '物件の価値を、|守りながら|高める。')}
<div class="prose"><p>知らないうちに又貸しされている。そうした状態は、家主様にとってもリスクです。HubHugは必ず事前にご相談し、承諾をいただいた物件だけで運用します。</p></div>
{checks(['テナントの家賃負担が軽くなり、空室・退去リスクが下がる', '利用者・利用時間・責任範囲を契約で把握できる', '間借りで実績を出した事業者が、次のテナント候補になる', '「公認間借り推奨ビル」として、物件の魅力づくりに'])}</div>
</div></section>

<section class="sec tint" id="flow"><div class="wrap">
{sh('ご利用の流れ', 'ご利用の流れ')}
{steps([('01', 'STEP 1', '無料相談・現地確認', '貸し出せる時間帯、設備、賃貸借契約の内容を確認します。'),
        ('02', 'STEP 2', '家主様との合意形成', '当社が家主・管理会社様へご説明し、承諾と契約の形を整えます。'),
        ('03', 'STEP 3', '借り手のご紹介・運用開始', '相性の良い出店者をご紹介。毎月の回収と運営のフォローを続けます。')])}
</div></section>
''' + cta('空いている時間を、|教えてください。', '「うちの店でもできるのか」という段階からご相談いただけます。', '?type=owner')

# =========================================================== contact
contact = phead('お問い合わせ', 'お問い合わせ', 'ご相談は無料です。内容を確認のうえ、担当者よりご連絡いたします。') + f'''
<section class="sec" style="padding-top:40px"><div class="wrap cgrid">
<div><h2 class="h2">{np('お気軽に|ご相談ください。')}</h2>
<ul class="assure">
<li>{ic('check')}<span class="t">ご相談は無料です</span></li>
<li>{ic('check')}<span class="t">3営業日以内にご返信します</span></li>
<li>{ic('check')}<span class="t">しつこい営業はいたしません</span></li>
<li>{ic('check')}<span class="t">構想段階・情報収集の段階でも歓迎です</span></li>
</ul></div>
<div>
<form class="form-card" id="cform" novalidate data-endpoint="" data-mailto="">
<fieldset class="field" style="border:0;padding:0;margin:0 0 26px"><legend class="lb">お立場<span class="opt">任意</span></legend><div class="chips">
<label><input type="radio" name="立場" value="開業したい" data-k="chef"><span>開業したい</span></label>
<label><input type="radio" name="立場" value="店舗オーナー" data-k="owner"><span>店舗オーナー</span></label>
<label><input type="radio" name="立場" value="家主・管理会社" data-k="landlord"><span>家主・管理会社</span></label>
<label><input type="radio" name="立場" value="その他" data-k="other"><span>その他</span></label></div></fieldset>
<div class="field" data-f><label for="f-name">お名前<span class="req">※必須</span></label><input id="f-name" type="text" name="お名前" autocomplete="name" required aria-describedby="e-name"><p class="err" id="e-name">{ic('alert')}<span class="t">お名前をご入力ください。</span></p></div>
<div class="field" data-f><label for="f-mail">メールアドレス<span class="req">※必須</span></label><input id="f-mail" type="email" name="メール" autocomplete="email" inputmode="email" required aria-describedby="e-mail"><p class="err" id="e-mail">{ic('alert')}<span class="t">メールアドレスを正しくご入力ください。</span></p></div>
<div class="field"><label for="f-tel">電話番号<span class="opt">任意</span></label><input id="f-tel" type="tel" name="電話" autocomplete="tel" inputmode="tel"></div>
<div class="field"><label for="f-shop">店舗名・会社名<span class="opt">任意</span></label><input id="f-shop" type="text" name="店舗・会社名" autocomplete="organization"></div>
<div class="field"><label for="f-msg">ご相談内容<span class="opt">任意</span></label><textarea id="f-msg" name="内容" placeholder="例）大阪市内でランチ営業できる店舗を探しています。"></textarea></div>
<button class="btn filled submit" type="submit">送信する</button>
<p class="note">ご入力いただいた個人情報は、お問い合わせへの対応のみに使用します。</p>
</form>
<div class="done" id="cdone" hidden><span class="ok">{ic('check')}</span><h3>送信ありがとうございます。</h3><p>内容を確認のうえ、3営業日以内に担当者よりご連絡いたします。</p>{arrow_link('index.html', 'トップへ戻る')}</div>
</div></div></section>
'''

T = '｜HubHug（ハブハグ）'
page('index.html', 'HubHug（ハブハグ）｜家主公認の間借り開業と、出退店の一気通貫サポート', '家主公認の間借り開業から、実店舗への独立、退店時の造作譲渡まで。飲食店の出店と退店に一気通貫で伴走するプラットフォーム。', index)
page('about.html', '私たちについて' + T, 'HubHugのミッション、代表メッセージ、連携・支援体制、会社概要。', about)
page('service.html', 'サービス' + T, '間借りシェア、実店舗への出店サポート、再起型の退店サポート。料金と他の選択肢との違い。', service)
page('scheme.html', '家主公認スキーム' + T, '無断転貸のリスクをなくす、家主・貸し手・借り手の三者合意による間借りの仕組み。', scheme)
page('chefs.html', '開業したい方へ' + T, '初期投資ゼロで始める間借り開業。月商別の収支イメージとご利用の流れ。', chefs)
page('owners.html', '店舗オーナー・家主の方へ' + T, '空き時間の貸し出しで家賃負担を軽減。家主・管理会社様のメリットも。', owners)
page('contact.html', 'お問い合わせ' + T, 'HubHugへのご相談・お問い合わせはこちらから。ご相談は無料です。', contact)
