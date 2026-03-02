# Claude Runner

GitHub Issue を Claude Code で自動処理する開発自動化ツール。

Issue を作れば Claude が読んで修正し、PR を出す。さらに `analyze.sh` を使えば、Claude 自身がコードを分析して Issue を作り、自分で解く——完全自律の改善ループが回る。

## 仕組み

```
┌─────────────┐     Issue (claude-task)     ┌─────────────┐
│ analyze.sh  │ ──────────────────────────>  │   GitHub    │
│ コード分析  │                              │   Issues    │
└─────────────┘                              └──────┬──────┘
                                                    │
                                             検出   │
                                                    v
┌─────────────┐     PR (claude-done)        ┌──────────────┐
│   GitHub    │ <────────────────────────── │ run-task.sh  │
│   Pull Req  │                             │ 修正 & PR    │
└─────────────┘                             └──────────────┘
```

| スクリプト | 役割 |
|-----------|------|
| `analyze.sh` | リポジトリを分析して改善 Issue を自動作成 |
| `run-task.sh` | 1つの Issue を Claude Code で解決し PR を作成 |
| `watcher.sh` | `claude-task` ラベルの Issue を監視して自動処理 |
| `setup.sh` | 初回セットアップ（ラベル作成・前提チェック） |

## 必要なもの

- [GitHub CLI (`gh`)](https://cli.github.com/)
- [Claude Code (`claude`)](https://docs.anthropic.com/en/docs/claude-code)
- `jq`, `git`

## クイックスタート

```bash
# 1. セットアップ（ラベル作成）
./setup.sh --repo OWNER/REPO

# 2. Issue を手動で作って Claude に解かせる
gh issue create --repo OWNER/REPO \
  --title "hello.py に goodbye 関数を追加" \
  --body "goodbye(name) 関数を追加。Goodbye, {name}! を返す。" \
  --label "claude-task"

./run-task.sh --repo OWNER/REPO --issue 1

# 3. または Claude 自身にコードを分析させて Issue を作る
./analyze.sh --repo OWNER/REPO --max-issues 3

# 4. 常駐モード（バックグラウンドで監視）
tmux new-session -d -s claude-runner \
  './watcher.sh --repo OWNER/REPO --interval 300'
```

## 使い方

### 手動で Issue を解かせる

```bash
./run-task.sh --repo OWNER/REPO --issue 42 --max-turns 30
```

Claude Code が Issue を読み、コードを修正し、テストを実行し、PR を作成する。

### コード分析 → Issue 自動作成

```bash
# 対話モード（作成する Issue を選択できる）
./analyze.sh --repo OWNER/REPO --max-issues 3

# 全件自動作成
./analyze.sh --repo OWNER/REPO --max-issues 3 --yes
```

Claude がコードベースを読んで改善点を洗い出し、GitHub Issue として起票する。

### 自律ループ（分析 → 修正 → 分析 → ...）

```bash
# analyze.sh + watcher.sh（または run-task.sh）を繰り返す
while true; do
  ./analyze.sh --repo OWNER/REPO --max-issues 2 --yes
  # watcher が claude-task を検出して自動処理
  sleep 300
done
```

## オプション一覧

### run-task.sh

| オプション | デフォルト | 説明 |
|-----------|-----------|------|
| `--repo` | (必須) | 対象リポジトリ (OWNER/REPO) |
| `--issue` | (必須) | Issue 番号 |
| `--max-turns` | 30 | Claude Code の最大ターン数 |

### analyze.sh

| オプション | デフォルト | 説明 |
|-----------|-----------|------|
| `--repo` | (必須) | 対象リポジトリ (OWNER/REPO) |
| `--max-issues` | 3 | 提案する Issue の上限 |
| `--max-turns` | 15 | Claude Code の最大ターン数 |
| `--yes` | false | 確認なしで全件作成 |

### watcher.sh

| オプション | デフォルト | 説明 |
|-----------|-----------|------|
| `--repo` | (必須) | 監視するリポジトリ (OWNER/REPO) |
| `--interval` | 300 | チェック間隔（秒） |
| `--max-turns` | 30 | Claude Code の最大ターン数 |

## ラベル

| ラベル | 意味 | 付与タイミング |
|--------|------|---------------|
| `claude-task` | 処理対象 | ユーザーまたは analyze.sh |
| `claude-working` | 処理中 | run-task.sh が自動付与 |
| `claude-done` | 完了（PR作成済み） | run-task.sh が自動付与 |
| `claude-failed` | 失敗 | run-task.sh がエラー時に付与 |

## 安全策

- main への直接 push はしない（必ず PR 経由）
- `--max-turns` で Claude の実行回数を制限
- Issue 間に 60 秒のクールダウン（API レート制限対策）
- ログは `~/.claude-runner/logs/` に全て保存
- PR のマージは人間が判断する

## 自律運用テストの結果

45分間の無人運転テストで以下の結果を得た:

- **10サイクル**: Issue 20件作成、PR 17件作成、**失敗 0件**
- Claude は目標なしでも「バグ修正 → テスト追加 → リファクタ → ツール自体の改善」と体系的に動いた
- 詳細: [REPORT-autonomous-analysis.md](REPORT-autonomous-analysis.md)

## ファイル構成

```
claude-runner/
├── README.md                        # このファイル
├── SETUP.md                         # 詳細セットアップ手順
├── REPORT-autonomous-analysis.md    # 自律運用テストレポート
├── setup.sh                         # 初回セットアップ
├── analyze.sh                       # コード分析 → Issue 作成
├── run-task.sh                      # Issue → Claude Code → PR
└── watcher.sh                       # Issue 監視デーモン
```

## ライセンス

MIT
