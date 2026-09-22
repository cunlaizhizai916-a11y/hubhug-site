#!/usr/bin/env python3
# HubHug portal builder: python3 build.py  → writes *.html next to this file.
# 見出しの "|" は文節の区切り（<span class="np">に変換。スマホで文節の途中で折れない）
import io, os, re
HERE = os.path.dirname(os.path.abspath(__file__))

def np(s):
    return ''.join('<br>' if p == '/' else f'<span class="np">{p}</span>' for p in re.split(r'\||(/)', s) if p)

NAV = [('about.html', '私たちについて', 'About'), ('service.html', 'サービス', 'Service'),
       ('scheme.html', '家主公認スキーム', 'Scheme'), ('chefs.html', '開業したい方へ', 'For Chefs'),
       ('owners.html', '店舗オーナー・家主の方へ', 'For Owners')]

LOGO = '''<svg viewBox="0 0 30 36" fill="none" stroke="currentColor" stroke-width="1.4" aria-hidden="true">
<path d="M2 35V15a13 13 0 0 1 26 0v20"/><path d="M9 35V17a6 6 0 0 1 12 0v18" stroke="#d2b57c"/><path d="M0 35h30"/></svg>'''

def brand():
    return f'<a class="brand" href="index.html" aria-label="HubHug トップへ">{LOGO}<span><b>HubHug</b><small>SHARE &amp; RESTART</small></span></a>'

def header(cur):
    links = ''.join(f'<a href="{h}"{" class=cur" if h == cur else ""}>{t}</a>' for h, t, _ in NAV)
    dr = '<a href="index.html">ホーム<small>Home</small></a>' + ''.join(f'<a href="{h}">{t}<small>{e}</small></a>' for h, t, e in NAV)
    return f'''<header class="hd" id="hd">{brand()}
<nav class="gnav" aria-label="メインナビゲーション">{links}<a class="cta" href="contact.html">お問い合わせ</a></nav>
<button class="hamb" id="hamb" aria-label="メニューを開く" aria-expanded="false" aria-controls="drawer"><i></i><i></i></button>
</header>
<div class="drawer" id="drawer">{dr}<a href="contact.html">お問い合わせ<small>Contact</small></a></div>'''

FOOTER = f'''<footer class="ft"><div class="wrap">
<div class="top"><div>{brand()}<p class="tag">飲食業を好きで始めた人が、<br>最後まで好きでいられる社会へ。</p></div>
<nav aria-label="フッターナビゲーション">
<div><h5>COMPANY</h5><a href="about.html">私たちについて</a><a href="about.html#message">代表メッセージ</a><a href="about.html#partners">連携・支援体制</a><a href="about.html#company">会社概要</a></div>
<div><h5>SERVICE</h5><a href="service.html">サービス一覧</a><a href="scheme.html">家主公認スキーム</a><a href="service.html#fee">料金について</a></div>
<div><h5>FOR YOU</h5><a href="chefs.html">開業したい方へ</a><a href="owners.html">店舗オーナー・家主の方へ</a><a href="contact.html">お問い合わせ</a></div>
</nav></div>
<div class="btm"><span>株式会社HubHug（2026年11月設立予定）／大阪市</span><span>&copy; 2026 HubHug Inc.</span></div>
</div></footer>
<div class="spbar" id="spbar"><a class="a" href="service.html">サービスを見る</a><a class="b" href="contact.html">無料で相談する</a></div>'''

def cta(h='まずは、お話を聞かせてください。', p='間借りで始めたい方も、空き時間を活かしたい店舗オーナー様も、物件をお持ちの家主様も。ご相談は無料です。'):
    return f'''<section class="cta"><div class="wrap rv"><h2>{np(h)}</h2><p>{p}</p>
<div class="btns"><a class="btn" href="contact.html">無料で相談する</a><a class="btn ghost" href="service.html">サービスを見る</a></div></div></section>'''

def shead(en, h, p='', center=False):
    return f'<div class="shead rv{" center" if center else ""}"><div class="en">{en}</div><h2>{np(h)}</h2>{f"<p>{p}</p>" if p else ""}</div>'

def phero(en, h, p, ghost, img, crumb):
    return f'''<section class="phero"><div class="bg"></div><div class="ph" data-img="{img}"></div><div class="gtx">{ghost}</div>
<div class="wrap"><div class="eyebrow">{en}</div><h1>{np(h)}</h1><p>{p}</p>
<div class="crumb"><a href="index.html">HOME</a>　/　{crumb}</div></div></section>'''

# 朝・昼・夜で一つの店を分け合う、を表すアーチ図
def arch(v='night'):
    sky = {'night': ('#0b1c3b', '#1d4486', '#c98f6a', '#f0d3a4'),
           'day':   ('#2f62a8', '#7fa5d8', '#cfe0f0', '#f3efe5'),
           'dawn':  ('#1d4486', '#8a7fa6', '#e3a582', '#f6dcae')}[v]
    stars = '<g fill="#fff"><circle cx="60" cy="70" r="1.2"/><circle cx="110" cy="40" r="1"/><circle cx="200" cy="58" r="1.3"/><circle cx="240" cy="110" r="1"/><circle cx="150" cy="96" r=".9"/><circle cx="85" cy="130" r="1"/></g><path d="M214 92a22 22 0 1 0 14 38a17 17 0 0 1-14-38z" fill="#f3efe5" opacity=".92"/>'
    orb = {'night': stars + '<circle cx="150" cy="330" r="46" fill="#f6dcae" opacity=".55"/><circle cx="150" cy="330" r="28" fill="#fbecc9" opacity=".85"/>',
           'day': '<circle cx="212" cy="104" r="50" fill="#fff" opacity=".25"/><circle cx="212" cy="104" r="28" fill="#fffaf0"/><g fill="#fff" opacity=".8"><rect x="40" y="150" width="70" height="10" rx="5"/><rect x="62" y="166" width="80" height="10" rx="5"/><rect x="170" y="214" width="64" height="9" rx="4.5"/></g>',
           'dawn': '<circle cx="150" cy="352" r="70" fill="#fbecc9" opacity=".4"/><circle cx="150" cy="352" r="40" fill="#fff3d6" opacity=".9"/><g fill="#fff" opacity=".7"><circle cx="70" cy="60" r="1"/><circle cx="230" cy="84" r="1.1"/></g>'}[v]
    win = '#f6dcae' if v != 'day' else '#1d4486'
    return f"""<svg class="fallback" viewBox="0 0 300 430" preserveAspectRatio="xMidYMid slice" aria-hidden="true">
<defs><linearGradient id="g-{v}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{sky[0]}"/><stop offset=".42" stop-color="{sky[1]}"/>
<stop offset=".72" stop-color="{sky[2]}"/><stop offset="1" stop-color="{sky[3]}"/></linearGradient></defs>
<rect width="300" height="430" fill="url(#g-{v})"/>{orb}
<g fill="#091730"><path d="M0 430V352h38v-30h44v46h30v-72h52v58h34v-34h46v50h56v80z" opacity="{'.55' if v != 'day' else '.28'}"/>
<path d="M70 430V368h160v62z"/><path d="M60 368l12-30h156l12 30z" fill="#b08d4f"/></g>
<g fill="{win}"><rect x="88" y="384" width="34" height="46"/><rect x="134" y="384" width="32" height="28"/><rect x="178" y="384" width="34" height="28"/></g>
</svg>"""

ARCH = arch('night')

ICON = {
 'chef': '<svg viewBox="0 0 84 84" fill="none" stroke="#fff" stroke-width="1.3"><path d="M26 50V38a12 12 0 1 1 6-22 12 12 0 0 1 20 0 12 12 0 1 1 6 22v12z"/><path d="M26 58h32M26 50v16h32V50"/></svg>',
 'shop': '<svg viewBox="0 0 84 84" fill="none" stroke="#fff" stroke-width="1.3"><path d="M14 34l6-16h44l6 16z"/><path d="M14 34a7 7 0 0 0 14 0 7 7 0 0 0 14 0 7 7 0 0 0 14 0 7 7 0 0 0 14 0"/><path d="M19 42v26h46V42M34 68V52h16v16"/></svg>',
 'bldg': '<svg viewBox="0 0 84 84" fill="none" stroke="#fff" stroke-width="1.3"><path d="M22 70V16h30v54M52 34h12v36M14 70h58"/><path d="M30 26h4M40 26h4M30 36h4M40 36h4M30 46h4M40 46h4M30 56h4M40 56h4"/></svg>',
}

def page(fn, title, desc, body):
    html = f'''<!DOCTYPE html>
<html lang="ja"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{title}</title><meta name="description" content="{desc}">
<meta property="og:title" content="{title}"><meta property="og:description" content="{desc}"><meta property="og:type" content="website">
<meta name="theme-color" content="#091730">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' fill='%23091730'/%3E%3Cpath d='M8 27V14a8 8 0 0 1 16 0v13' fill='none' stroke='%23d2b57c' stroke-width='2'/%3E%3C/svg%3E">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;500&family=Shippori+Mincho:wght@500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/style.css">
</head><body>
{header(fn)}
<main>
{body}
</main>
{FOOTER}
<script src="assets/site.js"></script>
</body></html>
'''
    def img(m):
        extra, f = (m.group(1) or ''), m.group(2)
        if os.path.exists(os.path.join(HERE, 'assets/img', f)):
            return 'class="ph%s has" style="background-image:url(assets/img/%s)"' % (extra, f)
        return 'class="ph%s"' % extra
    html = re.sub(r'class="ph( [a-z]+)?" data-img="([^"]+)"', img, html)
    io.open(os.path.join(HERE, fn), 'w', encoding='utf-8').write(html)
    print(fn, '%.1fKB' % (len(html.encode()) / 1024))

# =========================================================== index
index = f'''
<section class="hero"><div class="bg"></div><div class="ph" data-img="hero.jpg"></div>
<div class="gtx">HubHug</div>
<div class="in"><div class="eyebrow">Share &amp; Restart Platform</div>
<h1>{np('飲食業を|好きで始めた人が、/最後まで|好きでいられる|社会へ。')}</h1>
<p class="sub">HubHug（ハブハグ）は、家主公認の「間借り開業」から、実店舗への独立、万が一の退店までを一気通貫で伴走する、飲食店のためのプラットフォームです。</p>
<div class="btns"><a class="btn" href="service.html">サービスを見る</a><a class="btn ghost" href="contact.html">無料で相談する</a></div></div>
<div class="scrollcue">SCROLL</div></section>

<section class="sec"><div class="wrap statement">
<div class="rv"><div class="shead" style="margin-bottom:28px"><div class="en">Our Mission</div></div>
<p class="big">{np('出店の|「重さ」と、/退店の|「怖さ」を、')}<br><em>{np('どちらも|軽くする。')}</em></p></div>
<div class="body rv"><p class="lead">飲食店は、開業3年で約7割が廃業するとも言われます。最大の壁は、出店時の莫大な初期投資と、重くのしかかる固定費。そして退店時の原状回復費用です。</p>
<p class="lead">腕と志のある料理人が、資金の問題だけで二度と立ち上がれなくなる。私たちはその現場を数多く見てきました。</p>
<p class="lead">入り口は「間借り」で軽く。出口は「造作譲渡」で安全に。HubHugは、挑戦者が何度でも立ち上がれる仕組みをつくります。</p>
<a class="more" href="about.html">私たちについて</a></div>
</div></section>

<section class="sec ivory"><div class="wrap">
{shead('Portal', 'あなたの立場から、|お選びください。', 'HubHugは、借りたい方・貸したい方・物件を持つ方の三者をつなぎます。', True)}
<div class="portal">
<a class="pcard rv" href="chefs.html"><div class="top"><div class="ph" data-img="card-chef.jpg"></div>{ICON['chef']}<span class="no">01</span></div>
<div class="bd"><span class="who">FOR CHEFS</span><h3>{np('自分の店を|持ちたい方へ')}</h3><p>内装投資ゼロ。既存店舗の空き時間を借りて、すぐに営業を始められます。</p><span class="more">間借り開業を知る</span></div></a>
<a class="pcard rv" href="owners.html"><div class="top"><div class="ph" data-img="card-owner.jpg"></div>{ICON['shop']}<span class="no">02</span></div>
<div class="bd"><span class="who">FOR RESTAURANT OWNERS</span><h3>{np('空き時間を|活かしたい|店舗オーナー様へ')}</h3><p>営業していない時間帯を貸し出し、毎月の家賃負担を軽くします。手間はかかりません。</p><span class="more">間貸しの仕組みを知る</span></div></a>
<a class="pcard rv" href="owners.html#landlord"><div class="top"><div class="ph" data-img="card-bldg.jpg"></div>{ICON['bldg']}<span class="no">03</span></div>
<div class="bd"><span class="who">FOR LANDLORDS</span><h3>{np('物件を|お持ちの|家主・管理会社様へ')}</h3><p>無断転貸ではなく、家主様の承諾を前提とした適法な運用。物件の価値を守ります。</p><span class="more">家主様のメリットを知る</span></div></a>
</div></div></section>

<section class="sec navy hasph"><div class="ph secph" data-img="band-flow.jpg"></div><div class="wrap">
{shead('One-Stop Support', '入り口から出口まで、|一本の線で|伴走する。', '間借りで始め、実績をつくり、自分の店へ。万が一のときも、手元に資金を残して再起できるように。')}
<div class="flow rv">
<div><span class="k">STEP 01 — ENTRANCE</span><h3>間借りシェア「HubHug」</h3><p>既存店舗の朝・昼・夜の空き時間で、初期投資をかけずに開業。テスト販売とファンづくりの場に。</p></div>
<div><span class="k">STEP 02 — GROWTH</span><h3>実店舗への出店サポート</h3><p>飲食店舗に特化した物件探し、融資・補助金の獲得支援、内装・厨房・仕入れ業者のご紹介まで。</p></div>
<div><span class="k">STEP 03 — EXIT</span><h3>再起型の退店サポート</h3><p>スピーディーな造作譲渡（居抜き売却）で原状回復費用を抑え、手元に資金を残して次の挑戦へ。</p></div>
</div>
<div class="rv" style="margin-top:44px"><a class="more" href="service.html">サービスの詳細を見る</a></div>
</div></section>

<section class="sec"><div class="wrap statement">
<div class="figframe rv"><div class="archfig"><div class="ph" data-img="scheme.jpg"></div>{arch("dawn")}</div></div>
<div class="rv">{shead('Why HubHug', '「無断転貸」の壁を、|正面から|越える。')}
<div class="body"><p class="lead">店舗の賃貸借契約の多くは、無断での転貸（又貸し）を禁じています。家主に知らせないままの間借りは、発覚すれば即時退去のリスクと隣り合わせです。</p>
<p class="lead">HubHugは、家主・現店舗オーナー・間借り出店者の三者で、公式な承諾と契約を結びます。だから、安心して営業に集中できます。</p></div>
<a class="more" href="scheme.html">家主公認スキームを見る</a></div>
</div></section>

<section class="sec ivory"><div class="wrap msg">
<div class="figframe rv"><div class="archfig portrait"><div class="ph" data-img="portrait.jpg"></div>{ARCH}</div></div>
<div class="rv">{shead('Message', '飲食業を|好きで始めた人が、/最後まで|好きでいられる|社会を。')}
<div class="body"><p class="lead">祖父と父は、たこ焼き・お好み焼きの店を営んでいました。飲食業の厳しさは、身をもって知っています。</p>
<p class="lead">店舗開発の現場で、腕と志のある料理人が資金の問題だけで立ち上がれなくなるのを、数多く見てきました。だからこそ、入り口と出口の両方を軽くする仕組みを、自分の手でつくります。</p></div>
<p class="sig">株式会社HubHug　代表<b>青枝 実樹</b></p>
<div style="margin-top:26px"><a class="more" href="about.html#message">代表メッセージの全文を読む</a></div></div>
</div></section>

<section class="sec deep hasph"><div class="ph secph" data-img="band-record.jpg"></div><div class="wrap">
{shead('Track Record', '代表が|現場で|積み上げてきた|実績。')}
<div class="nums rv">
<div><div class="n">350<small>店舗以上</small></div><p class="t">家主公認の適法店舗・共同出店のプロデュース累計</p></div>
<div><div class="n">180<small>店舗</small></div><p class="t">大手飲食グループ大阪支店の立ち上げから約2年で展開</p></div>
<div><div class="n">10<small>年以上</small></div><p class="t">店舗開発・飲食特化の財務・不動産の実務経験</p></div>
<div><div class="n">3<small>者合意</small></div><p class="t">家主・貸し手・借り手の全員が承諾した契約のみ</p></div>
</div>
<p class="srcnote">※実績は代表 青枝の前職・現職を含むキャリア全体での数値です。</p>
<div class="rv" style="margin-top:40px"><a class="more" href="about.html#message">代表メッセージを読む</a></div>
</div></section>
{cta()}
'''

# =========================================================== about
about = phero('About Us', '私たちについて', '食で関西を盛り上げたい。飲食店開業のハードルを下げ、成功確率を高める。それがHubHugの出発点です。', 'About', 'about.jpg', '私たちについて') + f'''
<section class="sec"><div class="wrap statement">
<div class="rv">{shead('Name', '「Hub」で|つなぎ、/「Hug」で|支える。')}</div>
<div class="body rv"><p class="lead">Hub ── 借りたい料理人、貸したい店舗、物件を持つ家主。三者をつなぐ結節点になること。</p>
<p class="lead">Hug ── 手数料だけを受け取って放置するのではなく、契約・財務・経営まで、抱きしめるように伴走すること。</p>
<p class="lead">情報を仲介するだけの仕組みではなく、人が間に立つ「温かいプラットフォーム」でありたい。社名にはその意思を込めました。</p></div>
</div></section>

<section class="sec ivory" id="message"><div class="wrap msg">
<div class="figframe rv"><div class="archfig portrait"><div class="ph" data-img="portrait.jpg"></div>{arch("dawn")}</div></div>
<div class="rv">{shead('Message', '大切な店が、|ある日突然|なくなる。/その喪失を、|減らしたい。')}
<div class="body"><p>祖父と父は、かつてたこ焼き・お好み焼きの店を営んでいました。飲食業の厳しさは、身をもって知っています。</p>
<p>店舗開発の仕事に就いてからは、志と確かな腕を持ちながら、初期の資金ショートや高額な家賃、撤退時の原状回復費用で多額の負債を背負い、二度と立ち上がれなくなる料理人や経営者を、数多く目の当たりにしてきました。</p>
<p>通っていたお気に入りの店が、ある日突然閉店したこともあります。もし、営業時間をシェアできる仕組みや、傷口を広げずに撤退・再起できるセーフティネットがあれば、あの店は消えずに済んだのではないか。そう強く思いました。</p>
<p>飲食業が好きで、飲食業を始めた方が、最後まで飲食業を好きでいられる社会を創る。これは、私の生涯をかけたミッションです。</p></div>
<p class="sig">株式会社HubHug　代表<b>青枝 実樹</b></p></div>
</div></section>

<section class="sec"><div class="narrow">
{shead('Career', '代表の歩み')}
<div class="tl rv">
<div><span class="y">2015</span><h4>店舗流通ネット株式会社（東証プライム上場グループ）入社</h4><p>飲食店舗開発の基礎を学び、造作譲渡（居抜き）のノウハウと家主交渉の実務を修得。</p></div>
<div><span class="y">2020</span><h4>飲食特化の税理士法人グループ会社へ</h4><p>財務・融資・出退店スキームのコンサルティング業務に従事。</p></div>
<div><span class="y">2023</span><h4>RE/MAX NOW エージェントとして活動開始</h4><p>世界最大級の不動産ネットワークに登録。飲食開業希望者への提案力を強化。</p></div>
<div><span class="y">2024</span><h4>大手飲食グループ 大阪支店の立ち上げに参画</h4><p>業務委託契約やサブリースによる出店スキームを自ら構築。ビルオーナー・管理会社との合意形成を先導し、約2年で関西圏約180店舗の展開に貢献。</p></div>
<div><span class="y">2025</span><h4>レンタルスペース共同経営／飲食経営塾の事務局に</h4><p>大阪・十三でレンタルスペース「Tipi」の共同経営を開始。飲食経営塾「外食虎塾大阪」の事務局を務める。</p></div>
<div><span class="y">2026</span><h4>株式会社HubHug 設立準備</h4><p>出店から退店までをトータルで支える新会社の設立へ。</p></div>
</div></div></section>

<section class="sec ivory" id="partners"><div class="wrap">
{shead('Alliance', '連携・支援体制', '代表がキャリアを通じて築いてきた専門家・組織との連携を軸に、事業を展開します。')}
<div class="pts rv">
<div><span class="r">物件・顧客情報</span><h4>飲食店支援プラットフォーム</h4><p>国内最大級の飲食店支援サイトの関西代理店として、造作譲渡を希望する店舗オーナーの相談・面談業務を約3年継続して受託。</p></div>
<div><span class="r">不動産ネットワーク</span><h4>RE/MAX NOW</h4><p>世界110か国以上で展開する不動産ネットワーク。関西圏の店舗物件・ビルオーナーの情報網を活用します。</p></div>
<div><span class="r">財務・税務</span><h4>飲食特化の税理士法人グループ</h4><p>創業融資のための事業計画策定から、税務・財務コンサルティングまでを連携して提供。</p></div>
<div><span class="r">バックオフィス</span><h4>経理代行パートナー</h4><p>開業者が最も不安を抱える経理・バックオフィス業務をまるごとカバーする体制を構築。</p></div>
<div><span class="r">教育・コミュニティ</span><h4>外食虎塾大阪</h4><p>関西を代表する飲食チェーン経営者が集う経営塾。事務局として、貸し手店舗の開拓と独立志望者への接点を持ちます。</p></div>
<div><span class="r">実務アライアンス</span><h4>大手飲食グループ</h4><p>グループ内の既存店舗や開発物件を、モデル店舗として優先的に提供・シェアいただく協力体制。</p></div>
</div></div></section>

<section class="sec navy"><div class="wrap">
{shead('Roadmap', '大阪から、|関西へ。|そして全国へ。', '大阪は日本屈指の飲食店激戦区。空き時間を活用できている店舗は、まだごくわずかです。')}
<div class="road rv">
<div><span class="k">STEP 1</span><h4>大阪モデルの確立・検証</h4><p>大阪市内で、家主公認の間借りモデルを確立します。</p></div>
<div><span class="k">STEP 2</span><h4>関西圏への展開</h4><p>大阪・兵庫・京都・奈良・滋賀・和歌山へ。</p></div>
<div><span class="k">STEP 3</span><h4>全国展開・プラットフォーム化</h4><p>主要都市へ拡大し、全国の眠れる空き時間をつなぎます。</p></div>
</div></div></section>

<section class="sec" id="company"><div class="narrow">
{shead('Company', '会社概要')}
<dl class="dl rv">
<div><dt>会社名</dt><dd>株式会社HubHug（ハブハグ）</dd></div>
<div><dt>設立</dt><dd>2026年11月（予定）</dd></div>
<div><dt>代表者</dt><dd>青枝 実樹</dd></div>
<div><dt>所在地</dt><dd>大阪府大阪市（予定）</dd></div>
<div><dt>事業内容</dt><dd>間借りシェアサービス「HubHug」の運営／飲食店舗の出店サポート（不動産仲介・融資支援）／退店サポート（造作譲渡）</dd></div>
</dl></div></section>
''' + cta()

# =========================================================== service
service = phero('Service', 'サービス', '入り口の「間借り」から、成長の「実店舗出店」、出口の「造作譲渡」まで。飲食店のライフサイクルすべてに伴走します。', 'Service', 'service.jpg', 'サービス') + f'''
<section class="sec"><div class="wrap">
{shead('Three Services', '飲食店の一生に、|三つの支えを。')}
<div class="svc"><div class="vis rv"><div class="figframe"><div class="archfig"><div class="ph" data-img="svc1.jpg"></div>{arch("day")}</div></div></div>
<div class="rv"><span class="k">01 — ENTRANCE</span><h3>{np('間借りシェアサービス|「HubHug」')}</h3>
<p>既存飲食店の営業していない時間帯を、開業したい料理人へ。家主の承諾を得たうえで、貸し手と借り手をつなぎ、契約から毎月の決済管理までを担います。</p>
<ul class="ticks"><li>内装投資ゼロで、すぐに営業を開始</li><li>家主・貸し手・借り手の三者合意で、退去リスクなし</li><li>間借り料の回収は、デポジットと自動振替で管理</li><li>原価管理や集客のご相談にも伴走</li></ul>
<a class="more" href="scheme.html">家主公認スキームについて</a></div></div>

<div class="svc rev"><div class="vis rv"><div class="figframe"><div class="archfig"><div class="ph" data-img="svc2.jpg"></div>{arch("dawn")}</div></div></div>
<div class="rv"><span class="k">02 — GROWTH</span><h3>{np('実店舗への|出店サポート')}</h3>
<p>間借りで実績と自己資金をつくった次の一歩を支えます。飲食店舗に特化した不動産仲介と、融資獲得のための財務サポートをワンストップで。</p>
<ul class="ticks"><li>飲食店舗特化の物件探し・内覧時のチェックポイント支援</li><li>融資・補助金の獲得支援（事業計画、収支シミュレーション）</li><li>内装・厨房設備・仕入れ業者のご紹介</li><li>経理・バックオフィスの支援体制</li></ul></div></div>

<div class="svc"><div class="vis rv"><div class="figframe"><div class="archfig"><div class="ph" data-img="svc3.jpg"></div>{ARCH}</div></div></div>
<div class="rv"><span class="k">03 — EXIT</span><h3>{np('再起型の|退店サポート')}</h3>
<p>やむを得ず撤退する際も、傷口を広げない退店を。造作・設備の価値を査定し、水面下でスピーディーに譲渡先を見つけます。</p>
<ul class="ticks"><li>造作・設備の価値を査定</li><li>水面下でのスピード売却・譲渡仲介</li><li>スケルトン戻しの原状回復費用を抑える</li><li>手元に資金を残し、次の挑戦へ</li></ul></div></div>
</div></section>

<section class="sec ivory"><div class="wrap">
{shead('Time Share', '一つの店を、|時間で|分け合う。', '夜だけ営業する店の昼。昼だけのカフェの夜。定休日。眠っている時間が、誰かの最初の一歩になります。', True)}
<div class="timeband rv">
<div class="t1"><div class="bar"></div><span class="h">MORNING</span><h4>朝</h4><p>モーニング、ベーカリー、コーヒースタンド、仕込み利用など。</p></div>
<div class="t2"><div class="bar"></div><span class="h">DAYTIME</span><h4>昼</h4><p>居酒屋・バーの昼間を使ったランチ営業。カレー、定食、弁当販売など。</p></div>
<div class="t3"><div class="bar"></div><span class="h">NIGHT</span><h4>夜・定休日</h4><p>カフェの夜を使ったバー営業、定休日の一日店長など。</p></div>
</div></div></section>

<section class="sec" id="fee"><div class="wrap">
{shead('Fee', '料金について', '各プロセスで、わかりやすい手数料設計にしています。金額は設立準備中の予定であり、変更となる場合があります。')}
<div class="tblwrap rv"><table class="tbl">
<thead><tr><th>サービス</th><th>費用の種類</th><th>内容</th></tr></thead>
<tbody>
<tr><th rowspan="2">間借りシェア<br>「HubHug」</th><td>成約手数料</td><td>契約成立時に、貸し手様より月額間借り料の1か月分</td></tr>
<tr><td class="hl">月額利用・管理料</td><td class="hl">毎月の間借り料を、現店舗オーナー様と当社で50%ずつのレベニューシェア。<br>例）間借り料10万円の場合、オーナー様5万円・当社5万円。当社分には、家主交渉、契約の適法性維持、毎月の決済管理が含まれます。</td></tr>
<tr><th rowspan="2">実店舗への<br>出店サポート</th><td>不動産仲介手数料</td><td>法令で定められた上限（成約賃料の1か月分）</td></tr>
<tr><td>財務・融資サポート</td><td>融資・補助金の獲得額に応じた成功報酬</td></tr>
<tr><th>退店サポート</th><td>造作譲渡手数料</td><td>成約時に30万円（税別）、または譲渡金額の10%（成功報酬）</td></tr>
</tbody></table></div>
</div></section>

<section class="sec ivory"><div class="wrap">
{shead('Comparison', '他の選択肢との|違い')}
<div class="tblwrap rv"><table class="tbl">
<thead><tr><th></th><th>HubHug</th><th>マッチング特化型の間借りサービス</th><th>居抜きでの単独出店</th></tr></thead>
<tbody>
<tr><th>初期投資</th><td class="hl">ほぼ不要</td><td>ほぼ不要</td><td>数百万〜数千万円規模</td></tr>
<tr><th>家主の承諾</th><td class="hl">当社が事前に交渉し、公式に取得</td><td>当事者任せになりやすい</td><td>賃貸借契約で締結</td></tr>
<tr><th>現場トラブルへの対応</th><td class="hl">責任の所在を契約で明確化し、当社が間に立つ</td><td>当事者間での解決が中心</td><td>自己責任</td></tr>
<tr><th>経営・財務の支援</th><td class="hl">原価管理・集客・融資まで伴走</td><td>対象外のことが多い</td><td>別途、専門家を探す必要</td></tr>
<tr><th>独立・撤退時の支援</th><td class="hl">出店仲介から造作譲渡まで一貫</td><td>対象外</td><td>別途、業者を探す必要</td></tr>
</tbody></table></div>
<p class="fnote">※一般的な傾向を整理したもので、個別のサービス内容を示すものではありません。</p>
</div></section>
''' + cta()

# =========================================================== scheme
scheme = phero('Scheme', '家主公認スキーム', '間借りが広がりきらなかった理由は、法的なリスクにあります。HubHugは、その壁を正面から越えます。', 'Scheme', 'scheme-hero.jpg', '家主公認スキーム') + f'''
<section class="sec"><div class="wrap">
{shead('Problem', 'なぜ、間借りは|普及しきって|いないのか。', '間借り営業という形は以前からあります。しかし、家主に無断のまま行われる「野良間借り」には、三つの構造的な問題があります。')}
<div class="feats rv">
<div><span class="k">01</span><h3>{np('無断転貸による|契約違反と|即時退去リスク')}</h3><p>多くの賃貸借契約は無断転貸を禁じています（民法612条）。発覚すれば、契約解除・即時退去を求められるおそれがあります。</p></div>
<div><span class="k">02</span><h3>{np('責任の所在が|曖昧で、|トラブルが起きやすい')}</h3><p>設備の破損、ゴミ、近隣クレーム、売上管理。問題が起きても誰が責任を負うのかが決まっていません。</p></div>
<div><span class="k">03</span><h3>{np('明日、|営業できなくなる|かもしれない')}</h3><p>出店者は常に不安と隣り合わせ。腰を据えたブランドづくりやファンづくりに集中できません。</p></div>
</div></div></section>

<section class="sec ivory"><div class="wrap">
{shead('Solution', '三者が合意した|契約だけを、|扱います。', '', True)}
<div class="cmp rv">
<div class="bad"><span class="tag">従来の「野良間借り」</span><h3>家主に知らせないまま、当事者だけで貸し借り</h3>
<ul><li>無断転貸にあたり、契約違反となるおそれ</li><li>発覚すれば、貸し手の店舗ごと退去のリスク</li><li>トラブル時の責任の所在が不明確</li><li>金銭のやり取りが当事者任せ</li></ul></div>
<div class="good"><span class="tag">HubHugの家主公認スキーム</span><h3>家主・貸し手・借り手の三者で、公式に合意</h3>
<ul><li>業務委託または転貸承諾を、家主から公式に取得</li><li>物件ごとの契約条件に応じて、最適な形を設計</li><li>責任の範囲を契約で明確化</li><li>間借り料はデポジットと自動振替で当社が管理</li></ul></div>
</div></div></section>

<section class="sec"><div class="wrap">
{shead('Structure', '契約の間に、|当社が入ります。', '当社が契約の間に直接入り、公式な転貸・業務委託として適法な運用を担保します。')}
<div class="tri rv">
<div class="p"><span class="r">LANDLORD</span><h4>家主・管理会社</h4><p>空き時間の活用を承諾。物件は適法・クリーンに運用されます。</p></div>
<div class="c">承諾・契約</div>
<div class="p core"><span class="r">HUBHUG</span><h4>当社</h4><p>家主交渉、契約設計、決済管理、運営のフォローまでを担います。</p></div>
<div class="c">業務委託・転貸</div>
<div class="p"><span class="r">OWNER &amp; CHEF</span><h4><span class="np">現店舗オーナー ／</span> <span class="np">間借り出店者</span></h4><p>貸し手は家賃負担を軽減。借り手は初期投資なしで開業。</p></div>
</div></div></section>

<section class="sec navy"><div class="wrap">
{shead('Our Strength', 'なぜ、|HubHugなら|できるのか。')}
<div class="flow rv">
<div><span class="k">NEGOTIATION</span><h3>家主交渉の実務経験</h3><p>代表は累計350店舗以上の家主公認店舗をプロデュース。ビルオーナーや管理会社と対面で合意を形成してきました。</p></div>
<div><span class="k">CONTRACT</span><h3>契約スキームの構築力</h3><p>業務委託、サブリース（転貸借）。物件ごとに異なる条件に合わせ、適法な形を設計します。</p></div>
<div><span class="k">FINANCE</span><h3>飲食特化の財務知見</h3><p>財務・融資の実務経験と、税理士法人との連携により、開業後の経営まで支えます。</p></div>
</div>
<p class="srcnote">※契約形態は物件・契約条件により異なります。個別の法的判断が必要な場合は、連携する専門家とともに対応します。</p>
</div></section>
''' + cta('その物件で、|間借りはできるのか。/まずは|ご相談ください。', '賃貸借契約の内容や家主様との関係を伺い、実現できる形をご提案します。')

# =========================================================== chefs
def sim(st, h, sales, cost, util, left, memo):
    return f'''<div class="sim rv"><span class="st">{st}</span><h3>{h}</h3><div class="sales">{sales}<small>万円 / 月商</small></div>
<dl><div><dt>食材原価（約30%）</dt><dd>{cost}万円</dd></div><div><dt>間借り料</dt><dd>10万円</dd></div><div><dt>光熱費・雑費（按分）</dt><dd>約{util}万円</dd></div></dl>
<div class="left"><span>手残りの目安</span><b>約{left}<small>万円</small></b></div><p class="memo">{memo}</p></div>'''

chefs = phero('For Chefs', '開業したい方へ', '数千万円の借金を背負わなくても、自分の店は始められます。まずは間借りで、小さく確かな一歩を。', 'Chefs', 'chefs.jpg', '開業したい方へ') + f'''
<section class="sec"><div class="wrap">
{shead('Merit', '間借り開業で、|できること。')}
<div class="feats rv">
<div><span class="k">01</span><h3>初期投資ゼロで開業</h3><p>内装も厨房設備も、すでにある店舗を使います。物件契約や大きな借入は必要ありません。</p></div>
<div><span class="k">02</span><h3>固定費を大幅に抑える</h3><p>使う時間帯の分だけの間借り料。売上が読めない開業初期の資金繰りを守ります。</p></div>
<div><span class="k">03</span><h3>テストマーケティング</h3><p>メニュー、価格、立地。実際のお客様で試し、ファンをつくってから次の段階へ進めます。</p></div>
<div><span class="k">04</span><h3>家主公認の安心</h3><p>家主の承諾を得た契約だから、突然営業できなくなる心配がありません。</p></div>
<div><span class="k">05</span><h3>数字の不安に伴走</h3><p>原価管理や集客の相談、経理・バックオフィスの支援体制をご用意します。</p></div>
<div><span class="k">06</span><h3>独立までの道筋</h3><p>実績と自己資金ができたら、実店舗へ。物件探しから融資まで続けて支援します。</p></div>
</div></div></section>

<section class="sec ivory"><div class="wrap">
{shead('Simulation', '月商別の|収支イメージ', '間借り料の総額を月10万円とした場合の試算です。実際の金額は店舗・時間帯・営業日数により異なります。')}
<div class="sims">
{sim('STAGE 1', '副業・週末起業から始める', '30', '9', '3', '8', '週2〜3日のランチ営業でも届くライン。固定費の赤字リスクを抑えながら、自分のブランドで商売を始められます。')}
{sim('STAGE 2', '本業として軌道に乗せる', '50', '15', '4', '21', '営業日数を増やし、ファンが定着してきた段階。生活費と次への貯蓄を確保し、実店舗への準備が進みます。')}
{sim('STAGE 3', '人気店として独立直前へ', '90', '27', '6', '47', '連日満席に近い状態。資金を蓄え、万全の状態で自分の店舗のオープンへ。')}
</div>
<p class="fnote">※上記は一定の前提にもとづく試算であり、収益を保証するものではありません。人件費はご本人の営業を前提に含めていません。</p>
</div></section>

<section class="sec navy"><div class="wrap">
{shead('Flow', 'ご利用の流れ')}
<div class="flow rv">
<div><span class="k">01</span><h3>無料相談</h3><p>やりたい業態、希望エリア、時間帯、ご予算を伺います。</p></div>
<div><span class="k">02</span><h3>店舗のご提案・内覧</h3><p>家主承諾の見込める店舗をご提案。設備や動線を一緒に確認します。</p></div>
<div><span class="k">03</span><h3>三者合意・契約・開業</h3><p>家主・貸し手・あなたの三者で合意し契約。営業許可の確認を経て開業です。</p></div>
</div></div></section>
''' + cta('最初の一歩を、|軽くする。', 'まだ構想段階でもかまいません。お気軽にご相談ください。').replace('href="contact.html">無料', 'href="contact.html?type=chef">無料')

# =========================================================== owners
owners = phero('For Owners', '店舗オーナー・家主の方へ', '店が閉まっている時間も、家賃はかかり続けます。その時間を、無理なく収益に変える仕組みです。', 'Owners', 'owners.jpg', '店舗オーナー・家主の方へ') + f'''
<section class="sec"><div class="wrap">
{shead('For Restaurant Owners', '店舗オーナー様へ。/空いている時間が、|家賃を|軽くする。', '物価高と固定費の負担が続くなか、完全撤退の前にできることがあります。')}
<div class="feats rv">
<div><span class="k">01</span><h3>毎月の固定収入</h3><p>間借り料10万円の場合、オーナー様の取り分は月5万円（年間60万円）。家賃の大きな補填になります。</p></div>
<div><span class="k">02</span><h3>手間がかからない</h3><p>借り手の募集、家主への交渉、契約、毎月の回収まで当社が行います。</p></div>
<div><span class="k">03</span><h3>契約違反の心配がない</h3><p>家主の承諾を得たうえで進めるため、無断転貸にはなりません。</p></div>
<div><span class="k">04</span><h3>トラブルを未然に防ぐ</h3><p>清掃、設備、ゴミ、光熱費。ルールと責任の範囲を契約で明確にします。</p></div>
<div><span class="k">05</span><h3>金銭トラブルを防ぐ</h3><p>間借り料はデポジットと自動振替で当社が回収。未払いの不安を減らします。</p></div>
<div><span class="k">06</span><h3>いざという時の出口</h3><p>移転・撤退の際は、造作譲渡で原状回復費用を抑え、手元に資金を残す退店を支援します。</p></div>
</div></div></section>

<section class="sec ivory"><div class="wrap">
{shead('Time Share', '貸し出せる|時間帯の例', '', True)}
<div class="timeband rv">
<div class="t1"><div class="bar"></div><span class="h">MORNING</span><h4>朝</h4><p>開店前の時間を、モーニングやコーヒースタンドに。</p></div>
<div class="t2"><div class="bar"></div><span class="h">DAYTIME</span><h4>昼</h4><p>夜営業の店舗の昼間を、ランチ営業に。</p></div>
<div class="t3"><div class="bar"></div><span class="h">NIGHT / HOLIDAY</span><h4>夜・定休日</h4><p>昼営業の店舗の夜や、定休日の終日利用に。</p></div>
</div></div></section>

<section class="sec" id="landlord"><div class="wrap statement">
<div class="figframe rv"><div class="archfig"><div class="ph" data-img="landlord.jpg"></div>{arch("day")}</div></div>
<div class="rv">{shead('For Landlords', '家主・管理会社様へ。/物件の価値を、|守りながら|高める。')}
<div class="body"><p class="lead">知らないうちに又貸しされている。そうした状態は、家主様にとってもリスクです。HubHugは必ず事前にご相談し、承諾をいただいた物件だけで運用します。</p></div>
<ul class="ticks"><li>テナントの家賃負担が軽くなり、空室・退去リスクが下がる</li><li>利用者・利用時間・責任範囲を契約で把握できる</li><li>間借りで実績を出した事業者が、次のテナント候補になる</li><li>「公認間借り推奨ビル」として、物件の魅力づくりに</li></ul></div>
</div></section>

<section class="sec navy"><div class="wrap">
{shead('Flow', 'ご利用の流れ')}
<div class="flow rv">
<div><span class="k">01</span><h3>無料相談・現地確認</h3><p>貸し出せる時間帯、設備、賃貸借契約の内容を確認します。</p></div>
<div><span class="k">02</span><h3>家主様との合意形成</h3><p>当社が家主・管理会社様へご説明し、承諾と契約の形を整えます。</p></div>
<div><span class="k">03</span><h3>借り手のご紹介・運用開始</h3><p>相性の良い出店者をご紹介。毎月の回収と運営のフォローを続けます。</p></div>
</div></div></section>
''' + cta('空いている時間を、|教えてください。', '「うちの店でもできるのか」という段階からご相談いただけます。').replace('href="contact.html">無料', 'href="contact.html?type=owner">無料')

# =========================================================== contact
contact = phero('Contact', 'お問い合わせ', 'ご相談は無料です。内容を確認のうえ、担当者よりご連絡いたします。', 'Contact', 'contact.jpg', 'お問い合わせ') + '''
<section class="sec"><div class="wrap cgrid">
<div class="rv"><div class="shead" style="margin-bottom:30px"><div class="en">Free Consultation</div><h2><span class="np">お気軽に</span><span class="np">ご相談ください。</span></h2></div>
<ul class="assure"><li>ご相談は無料です</li><li>3営業日以内にご返信します</li><li>しつこい営業はいたしません</li><li>構想段階・情報収集の段階でも歓迎です</li></ul></div>
<div class="rv">
<form class="cf" id="cform" novalidate data-endpoint="" data-mailto="">
<div class="field"><span class="lb">お立場<span class="opt">任意</span></span><div class="chips">
<label><input type="radio" name="立場" value="開業したい" data-k="chef"><span>開業したい</span></label>
<label><input type="radio" name="立場" value="店舗オーナー" data-k="owner"><span>店舗オーナー</span></label>
<label><input type="radio" name="立場" value="家主・管理会社" data-k="landlord"><span>家主・管理会社</span></label>
<label><input type="radio" name="立場" value="その他" data-k="other"><span>その他</span></label></div></div>
<div class="field" data-f><label for="f-name">お名前<span class="req">必須</span></label><input id="f-name" type="text" name="お名前" autocomplete="name" required><p class="err">お名前をご入力ください。</p></div>
<div class="field" data-f><label for="f-mail">メールアドレス<span class="req">必須</span></label><input id="f-mail" type="email" name="メール" autocomplete="email" inputmode="email" required><p class="err">メールアドレスを正しくご入力ください。</p></div>
<div class="field"><label for="f-tel">電話番号<span class="opt">任意</span></label><input id="f-tel" type="tel" name="電話" autocomplete="tel" inputmode="tel"></div>
<div class="field"><label for="f-shop">店舗名・会社名<span class="opt">任意</span></label><input id="f-shop" type="text" name="店舗・会社名" autocomplete="organization"></div>
<div class="field"><label for="f-msg">ご相談内容<span class="opt">任意</span></label><textarea id="f-msg" name="内容" placeholder="例）大阪市内でランチ営業できる店舗を探しています。"></textarea></div>
<button class="submit" type="submit">送信する</button>
<p class="fnote">ご入力いただいた個人情報は、お問い合わせへの対応のみに使用します。</p>
</form>
<div class="done" id="cdone" hidden><h3>送信ありがとうございます。</h3><p>内容を確認のうえ、3営業日以内に担当者よりご連絡いたします。</p><a class="more" href="index.html" style="justify-content:center">トップへ戻る</a></div>
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
