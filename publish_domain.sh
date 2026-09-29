#!/usr/bin/env bash
# HubHug を、なおきさんのCloudflareで買ったドメインに公開する（招待を承認したあとに実行）
#
#   ./publish_domain.sh hubhug.com          → hubhug.com と www.hubhug.com で公開
#
# 中身：make_deploy.py で _deploy/ を作り直し → domain-kit/publish.sh に渡すだけ。
# 文言や写真を直したあとも、同じコマンドを打てば上書き更新される。
set -euo pipefail
cd "$(dirname "$0")"
[[ $# -ge 1 ]] || { echo "使い方: ./publish_domain.sh <ドメイン>"; exit 1; }
python3 make_deploy.py
exec "../AI受託事業/domain-kit/publish.sh" "_deploy" "$1" --www "${@:2}"
