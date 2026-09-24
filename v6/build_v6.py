#!/usr/bin/env python3
# v6 = 明るい版。本体の build.py を読み込み、出力先・CSS・画像だけ差し替えて v6/ に書き出す。
# 文言は本体 build.py と共通（本体を直して python3 v6/build_v6.py で両方に反映できる）。
import os
V6 = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(V6)
src = open(os.path.join(ROOT, 'build.py'), encoding='utf-8').read()

# 夜・シャッター街など暗い写真は使わない（明るい写真が入るまでは白地＋イラスト）
USE = {'portrait.jpg', 'card-chef.jpg', 'chefs.jpg', 'svc1.jpg', 'band-flow.jpg', 'service.jpg', 'contact.jpg', 'svc2.jpg', 'landlord.jpg'}
BRIGHT = os.path.join(V6, 'img')  # v6/img に同名ファイルを置けばそちらが優先される

rep = [
    ("HERE = os.path.dirname(os.path.abspath(__file__))", f"HERE = {V6!r}"),
    ("<link rel=\"stylesheet\" href=\"assets/style.css\">",
     "<link rel=\"stylesheet\" href=\"../assets/style.css\"><link rel=\"stylesheet\" href=\"bright.css\">"),
    ("<script src=\"assets/site.js\"></script>", "<script src=\"../assets/site.js\"></script>"),
    ('<meta name="theme-color" content="#091730">', '<meta name="theme-color" content="#ffffff">'),
    ("ARCH = arch('night')", "ARCH = arch('day')"),
    ('<div class="gtx">HubHug</div>', '<div class="gtx">HubHug</div><div class="heroart" aria-hidden="true">{arch("day")}<span class="sun"></span></div>'),
    ("""        if os.path.exists(os.path.join(HERE, 'assets/img', f)):
            return 'class="ph%s has" style="background-image:url(assets/img/%s)"' % (extra, f)""",
     """        if os.path.exists(os.path.join(HERE, 'img', f)):
            return 'class="ph%s has" style="background-image:url(img/%s)"' % (extra, f)
        if f in USE:
            return 'class="ph%s has" style="background-image:url(../assets/img/%s)"' % (extra, f)"""),
]
for a, b in rep:
    assert a in src, a[:60]
    src = src.replace(a, b)
exec(compile(src, 'build.py(v6)', 'exec'), {'USE': USE, '__file__': os.path.join(ROOT, 'build.py'), '__name__': '__main__'})
