#!/bin/bash
# =============================================================================
# watcher.sh — GitHub Issue を監視して Claude Code で自動処理するデーモン
#
# Usage:
#   ./watcher.sh --repo OWNER/REPO [--interval 300] [--max-turns 30]
#
# 事前準備:
#   1. gh auth login
#   2. リポジトリに以下のラベルを作成:
#      - claude-task    (新規タスク: ユーザーが付ける)
#      - claude-working (処理中: スクリプトが付ける)
#      - claude-done    (完了: スクリプトが付ける)
#      - claude-failed  (失敗: スクリプトが付ける)
#
# 推奨起動方法:
#   tmux new-session -d -s claude-runner './watcher.sh --repo OWNER/REPO'
# =============================================================================
set -euo pipefail

# --- デフォルト値 ---
REPO=""
INTERVAL=300     # 5分
MAX_TURNS=30
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
STATE_DIR="${HOME}/.claude-runner"

# --- 引数パース ---
while [[ $# -gt 0 ]]; do
  case $1 in
    --repo)       REPO="$2";       shift 2 ;;
    --interval)   INTERVAL="$2";   shift 2 ;;
    --max-turns)  MAX_TURNS="$2";  shift 2 ;;
    *) echo "Unknown option: $1"; exit 1 ;;
  esac
done

if [[ -z "$REPO" ]]; then
  echo "Usage: $0 --repo OWNER/REPO [--interval SECONDS] [--max-turns N]"
  exit 1
fi

mkdir -p "$STATE_DIR"
PROCESSED_FILE="${STATE_DIR}/processed-${REPO//\//-}.txt"
touch "$PROCESSED_FILE"

# --- ログ関数 ---
log() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*"; }

# --- ラベル初期化 ---
ensure_labels() {
  log "ラベルの存在を確認中..."
  for label in claude-task claude-working claude-done claude-failed; do
    gh label create "$label" --repo "$REPO" --force 2>/dev/null || true
  done
  log "ラベル確認完了"
}

# --- 処理済みかチェック ---
is_processed() {
  grep -qx "$1" "$PROCESSED_FILE" 2>/dev/null
}

mark_processed() {
  echo "$1" >> "$PROCESSED_FILE"
}

# --- メインループ ---
main() {
  log "=========================================="
  log "Claude Runner 起動"
  log "  リポジトリ: ${REPO}"
  log "  監視間隔:   ${INTERVAL}秒"
  log "  Max turns:  ${MAX_TURNS}"
  log "=========================================="

  ensure_labels

  while true; do
    log "--- Issue をチェック中 (label: claude-task) ---"

    # claude-task ラベルが付いた open Issue を取得
    ISSUES=$(gh issue list \
      --repo "$REPO" \
      --label "claude-task" \
      --state open \
      --json number,title \
      --limit 10 2>/dev/null || echo "[]")

    COUNT=$(echo "$ISSUES" | jq 'length')

    if [[ "$COUNT" -eq 0 ]]; then
      log "タスクなし。${INTERVAL}秒後に再チェック..."
    else
      log "${COUNT} 件のタスクを検出"

      # 1件ずつ処理（並列にはしない — レート制限対策）
      while read -r issue; do
        ISSUE_NUM=$(echo "$issue" | jq -r '.number')
        ISSUE_TITLE=$(echo "$issue" | jq -r '.title')

        if is_processed "$ISSUE_NUM"; then
          log "  #${ISSUE_NUM} はスキップ (処理済み)"
          continue
        fi

        log "  #${ISSUE_NUM}: ${ISSUE_TITLE} — 処理開始"

        # run-task.sh を実行
        if "${SCRIPT_DIR}/run-task.sh" \
            --repo "$REPO" \
            --issue "$ISSUE_NUM" \
            --max-turns "$MAX_TURNS"; then
          log "  #${ISSUE_NUM}: 成功"
        else
          log "  #${ISSUE_NUM}: 失敗 (exit code: $?)"
        fi

        mark_processed "$ISSUE_NUM"

        # タスク間に少し間を空ける（レート制限対策）
        log "  次のタスクまで60秒待機..."
        sleep 60
      done < <(echo "$ISSUES" | jq -c '.[]')
    fi

    sleep "$INTERVAL"
  done
}

# --- シグナルハンドリング ---
cleanup() {
  log "シャットダウン中..."
  exit 0
}
trap cleanup SIGINT SIGTERM

main
