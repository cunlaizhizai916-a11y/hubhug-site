#!/usr/bin/env python3
"""独自ドメイン公開用に、v6（明るい版・7ページ）を1フォルダにまとめる。

  python3 make_deploy.py      → _deploy/ を作り直す

v6 は ../assets/（本体のCSS・JS・一部写真）を参照しているので、
必要なものだけ _deploy/ に同梱してパスを書き換える。
1枚LP（v5）は /lp/ に置く。
"""
import re, shutil, subprocess
from pathlib import Path

ROOT = Path(__file__).parent
V6, OUT = ROOT / "v6", ROOT / "_deploy"

subprocess.run(["python3", str(V6 / "build_v6.py")], check=True, capture_output=True)

shutil.rmtree(OUT, ignore_errors=True)
(OUT / "assets" / "img").mkdir(parents=True)
shutil.copytree(V6 / "img", OUT / "img", ignore=shutil.ignore_patterns("CREDITS.txt"))
shutil.copy(V6 / "bright.css", OUT)
for f in ("style.css", "site.js"):
    shutil.copy(ROOT / "assets" / f, OUT / "assets")

used = set()
for page in sorted(V6.glob("*.html")):
    html = page.read_text(encoding="utf-8")
    used |= set(re.findall(r"\.\./assets/img/([\w.-]+)", html))
    (OUT / page.name).write_text(html.replace("../assets/", "assets/"), encoding="utf-8")
for f in used:
    shutil.copy(ROOT / "assets" / "img" / f, OUT / "assets" / "img")

(OUT / "lp").mkdir()
shutil.copy(ROOT / "v5" / "index.html", OUT / "lp" / "index.html")

# 検査：外に出ていく相対参照が残っていないこと・参照先が全部あること
bad = []
for page in OUT.rglob("*.html"):
    html = page.read_text(encoding="utf-8")
    if "../" in html:
        bad.append(f"{page.relative_to(OUT)}: ../ が残っている")
    for ref in re.findall(r'(?:src|href)="([^"#?:]+\.(?:css|js|jpg|png|html))"', html) + \
               re.findall(r"url\(([^)#:]+\.jpg)\)", html):
        if not (page.parent / ref).exists():
            bad.append(f"{page.relative_to(OUT)}: {ref} が無い")
if bad:
    raise SystemExit("✗ " + "\n✗ ".join(bad))

files = [p for p in OUT.rglob("*") if p.is_file()]
mb = sum(p.stat().st_size for p in files) / 1024 / 1024
print(f"✓ _deploy/ に {len(files)} ファイル（{mb:.1f}MB）")
print("  トップ=index.html（v6の7ページ）／1枚LP=/lp/")
