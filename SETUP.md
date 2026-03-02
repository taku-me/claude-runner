# Claude Runner セットアップ手順

GitHub Issue を Claude Code で自動処理し、PR を作成するツール。

## 前提条件

| ツール | 確認コマンド |
|--------|-------------|
| gh (GitHub CLI) | `gh --version` |
| claude (Claude Code CLI) | `claude --version` |
| jq | `jq --version` |
| git | `git --version` |
| tmux | `tmux -V` |

## 1. 初回セットアップ

```bash
cd /Volumes/HIKSEMI*/projects/claude-runner

# 対象リポジトリにラベルを作成 & 動作確認
./setup.sh --repo OWNER/REPO
```

作成されるラベル:
- `claude-task` — 処理対象（ユーザーが付ける）
- `claude-working` — 処理中（自動）
- `claude-done` — 完了（自動）
- `claude-failed` — 失敗（自動）

## 2. テスト実行（単発）

```bash
# テスト用 Issue を作成
gh issue create --repo OWNER/REPO \
  --title "テスト: hello.py に goodbye 関数を追加" \
  --body "goodbye(name) 関数を追加。Goodbye, {name}! を返す。" \
  --label "claude-task"

# 単発実行（Issue 番号を指定）
./run-task.sh --repo OWNER/REPO --issue 1 --max-turns 10
```

## 3. 常駐モード（watcher）

```bash
# tmux セッションで watcher を起動
tmux new-session -d -s claude-runner \
  '/Volumes/HIKSEMI*/projects/claude-runner/watcher.sh --repo OWNER/REPO'

# ログを確認
tmux attach -t claude-runner

# デタッチ: Ctrl+B → D
```

### watcher のオプション

| オプション | デフォルト | 説明 |
|-----------|-----------|------|
| `--repo` | (必須) | 監視するリポジトリ (OWNER/REPO) |
| `--interval` | 300 | チェック間隔（秒） |
| `--max-turns` | 30 | Claude Code の最大ターン数 |

## 4. 運用フロー

```
朝（出勤前）:
  1. tmux で watcher を起動
  2. SSH 切断して出勤

日中（スマホから）:
  3. GitHub で Issue を作成、ラベル claude-task を付ける
  4. Claude が 5 分以内に検知 → 自動処理 → PR 作成

帰宅後:
  5. tmux attach で状況確認
  6. gh pr list で PR をレビュー & マージ
```

## 5. ファイル構成

```
claude-runner/
├── setup.sh       # 初回セットアップ（ラベル作成・前提チェック）
├── watcher.sh     # メインループ（Issue 監視デーモン）
├── run-task.sh    # 単体実行（1 Issue → Claude Code → PR）
└── SETUP.md       # この手順書
```

## 6. 安全策

- `--max-turns` でループ回数制限（デフォルト 30）
- main への直接 push はしない（必ず PR 経由）
- Issue 間に 60 秒のクールダウン
- ログ: `~/.claude-runner/logs/` に全て保存
- watcher 停止: `tmux kill-session -t claude-runner`

## 7. トラブルシューティング

### Claude Code がネスト実行エラー

Claude Code セッション内から run-task.sh を実行した場合に発生。
スクリプト内で `unset CLAUDECODE` 済みだが、解消しない場合は
ターミナルから直接実行する。

### gh の認証切れ

```bash
gh auth login
```

### テスト用リポジトリの削除

```bash
gh repo delete taku-me/claude-runner-test --yes
```
