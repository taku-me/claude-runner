#!/bin/bash
# =============================================================================
# setup.sh — Claude Runner の初期セットアップ
# 指定リポジトリに必要なラベルを作成し、動作確認を行う
#
# Usage: ./setup.sh --repo OWNER/REPO
# =============================================================================
set -euo pipefail

REPO=""

while [[ $# -gt 0 ]]; do
  case $1 in
    --repo) REPO="$2"; shift 2 ;;
    *)      echo "Unknown: $1"; exit 1 ;;
  esac
done

if [[ -z "$REPO" ]]; then
  echo "Usage: $0 --repo OWNER/REPO"
  exit 1
fi

echo "=== Claude Runner セットアップ ==="
echo ""

# 1. 前提チェック
echo "[1/4] 前提ツールの確認..."
for cmd in gh claude jq git; do
  if command -v "$cmd" &>/dev/null; then
    echo "  ✓ $cmd"
  else
    echo "  ✗ $cmd が見つかりません。インストールしてください。"
    exit 1
  fi
done

# 2. GitHub 認証チェック
echo ""
echo "[2/4] GitHub 認証の確認..."
if gh auth status &>/dev/null; then
  echo "  ✓ gh 認証済み"
else
  echo "  ✗ gh auth login を実行してください"
  exit 1
fi

# 3. ラベル作成
echo ""
echo "[3/4] ラベルの作成..."

gh label create "claude-task" \
  --repo "$REPO" \
  --description "Claude Runner に処理させるタスク" \
  --color "7057ff" \
  --force 2>/dev/null && echo "  ✓ claude-task" || echo "  ✓ claude-task (既存)"

gh label create "claude-working" \
  --repo "$REPO" \
  --description "Claude Runner が処理中" \
  --color "fbca04" \
  --force 2>/dev/null && echo "  ✓ claude-working" || echo "  ✓ claude-working (既存)"

gh label create "claude-done" \
  --repo "$REPO" \
  --description "Claude Runner の処理完了" \
  --color "0e8a16" \
  --force 2>/dev/null && echo "  ✓ claude-done" || echo "  ✓ claude-done (既存)"

gh label create "claude-failed" \
  --repo "$REPO" \
  --description "Claude Runner の処理失敗" \
  --color "d73a4a" \
  --force 2>/dev/null && echo "  ✓ claude-failed" || echo "  ✓ claude-failed (既存)"

# 4. 状態ディレクトリ
echo ""
echo "[4/4] 状態ディレクトリの作成..."
mkdir -p "${HOME}/.claude-runner/logs"
echo "  ✓ ${HOME}/.claude-runner/"

echo ""
echo "=== セットアップ完了 ==="
echo ""
echo "使い方:"
echo "  1. リポジトリで Issue を作成し、ラベル 'claude-task' を付ける"
echo "  2. 以下のコマンドで watcher を起動:"
echo ""
echo "     tmux new-session -d -s claude-runner \\"
echo "       '$(cd "$(dirname "$0")" && pwd)/watcher.sh --repo ${REPO}'"
echo ""
echo "  3. tmux attach -t claude-runner で状況を確認"
echo ""
