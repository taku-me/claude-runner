# Claude Runner

GitHub Issue を Claude Code で自動処理し、PR を作成するツール。

## 前提条件

- [gh (GitHub CLI)](https://cli.github.com/)
- [Claude Code CLI](https://docs.anthropic.com/en/docs/claude-code)
- jq
- git
- tmux
- Python 3 / pytest（テスト実行用）

## 使い方

### セットアップ

```bash
./setup.sh --repo OWNER/REPO
```

### 単発実行

```bash
./run-task.sh --repo OWNER/REPO --issue <ISSUE_NUMBER> --max-turns 10
```

### 常駐モード（watcher）

```bash
tmux new-session -d -s claude-runner \
  './watcher.sh --repo OWNER/REPO'
```

詳細は [SETUP.md](SETUP.md) を参照してください。

## ライセンス

MIT
