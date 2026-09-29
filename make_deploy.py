#!/usr/bin/env python3
"""独自ドメイン公開用に、サイト（7ページ）を1フォルダにまとめる。

  python3 make_deploy.py        → v7 を _deploy/ に（既定）
  python3 make_deploy.py v6     → v6 を _deploy/ に

v7 は自己完結（style.css / site.js / img/ 同梱）なのでそのままコピー。
v6 は ../assets/（本体のCSS・JS・一部写真）を参照しているので、
必要なものだけ同梱してパスを書き換える。1枚LP（v5）は /lp/ に置く。
"""
import re, shutil, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).parent
VER = sys.argv[1] if len(sys.argv) > 1 else "v7"
SRC, OUT = ROOT / VER, ROOT / "_deploy"
shutil.rmtree(OUT, ignore_errors=True)

if VER == "v6":
    subprocess.run(["python3", str(SRC / "build_v6.py")], check=True, capture_output=True)
    (OUT / "assets" / "img").mkdir(parents=True)
    shutil.copytree(SRC / "img", OUT / "img", ignore=shutil.ignore_patterns("CREDITS.txt"))
    shutil.copy(SRC / "bright.css", OUT)
    for f in ("style.css", "site.js"):
        shutil.copy(ROOT / "assets" / f, OUT / "assets")
    used = set()
    for page in sorted(SRC.glob("*.html")):
        html = page.read_text(encoding="utf-8")
        used |= set(re.findall(r"\.\./assets/img/([\w.-]+)", html))
        (OUT / page.name).write_text(html.replace("../assets/", "assets/"), encoding="utf-8")
    for f in used:
        shutil.copy(ROOT / "assets" / "img" / f, OUT / "assets" / "img")
else:
    subprocess.run(["python3", str(SRC / "build.py")], check=True, capture_output=True)
    shutil.copytree(SRC, OUT, ignore=shutil.ignore_patterns("build.py", "CREDITS.txt", ".DS_Store", "__pycache__"))

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
print(f"  トップ=index.html（{VER}の7ページ）／1枚LP=/lp/")
