# トラブルシューティング

[README](../README.md) · [環境準備](setup.md) · [本編](handson.md)

コマンドは WSL2 Ubuntu の Bash で実行してください。

## コマンドが見つからない

```bash
pwd
command -v uv
command -v git
command -v gh
command -v node
```

Windows にだけインストールしたツールは、Ubuntu 内で別途準備が必要な場合があります。
uv 導入直後なら `source "$HOME/.local/bin/env"` を実行するか、ターミナルを開き直します。
プロジェクトが Windows のファイルシステム側にある場合は、`~/src` に Clone して進めてください。

## Clone・Push・Issue 取得で認証や権限のエラーになる

```bash
gh auth status
git remote -v
gh repo view
```

ログイン先と `origin` が自分のリポジトリであることを確認します。
認証できていなければ `gh auth login` と `gh auth setup-git` を実行します。
組織の認証や権限の制約がある場合は、研修用に許可されたリポジトリを使います。

`git push` が non-fast-forward で失敗した場合は、GitHub 側に手元にない変更があります。
まず `git fetch origin` と `git log --oneline --all --graph -12` で状況を確認し、講師に相談してください。
研修中に force push で上書きする必要はありません。

## uv sync が失敗する

リポジトリのルートに `pyproject.toml`、`.python-version`、`uv.lock` があることを確認します。

```bash
uv --version
uv python install
uv sync
```

- Python のダウンロード失敗：接続・プロキシ・社内証明書の設定を確認します。
- `uv.lock` がない：`uv sync` が自動生成します。教材には同梱されているので、ほかにもファイルが不足していないか確認します。
- 依存関係の解決に失敗する：`pyproject.toml` に意図しない編集がないか `git diff` で確認します。この演習では依存の変更は不要です。

`uv.lock` を手で編集したり、解決策として `pip install` へ切り替えたりしないでください。

## pytest の import が失敗する

```bash
pwd
uv run pytest
```

プロジェクトのルートから実行します。`calculator.py` のファイル名と、テストが import する関数名を確認してください。
TDD の最初に、未実装の `divide` の import が失敗するのは意図した失敗です。
実装後も同じエラーなら、実装場所と名前を確認します。

## Skills が候補に出ない・同名のものが複数ある

リポジトリのルートで導入したか、`--agent` に選択したツールを指定したか確認します。
インストーラーが出力する配置先を確認し、AI ツールを終了・再起動してください。
Claude Code は `/`、Codex は `$` を入力して候補から選びます。
プラグイン由来では名前に接頭辞が付く場合があるので、mattpocock/skills 由来の正式名を選びます。

Skills CLI とプラグインの両方で同じものを導入すると重複します。片方の方式に揃えてください。
組織でプラグイン利用が制限されている場合は、環境管理者に導入方法を確認します。

## AI が Issue を読めない・内部の Skill を呼べない

ターミナルで `gh issue view 実際の番号` を実行できることを確認します。
Issue 番号だけで曖昧になる場合は、自分のリポジトリの Issue URL を AI に渡します。

`implement` が `tdd` や `code-review` を呼び出せない場合は、受講者がそれぞれを明示的に呼び出します。
その場合も、最初のテスト失敗を見て停止する指示と、Commit・Push をしない指示を添えます。

## AI が先に Commit した

```bash
git log -3 --oneline
git show --stat HEAD
git show HEAD
```

差分が課題に対応していることを確認し、その Commit を使って Push・PR へ進めます。
変更が残っていなければ、空の Commit を作る必要はありません。
Commit の練習が必要なら、レビューで見つけた実際の改善を別 Commit にします。
履歴を戻してやり直す必要はありません。

## PR の差分が想定と違う・PR が見つからない

```bash
git branch --show-current
git status --short
git log --oneline origin/main..HEAD
git diff origin/main...HEAD
gh pr list
```

base が `main`、compare が自分の feature ブランチであることを確認します。
`gh` は現在のブランチから PR を推定します。main へ戻った後は PR 番号を明示してください。

ターミナルを開き直すと `ISSUE_NUMBER` は失われます。必要なら `ISSUE_NUMBER=実際の番号` を設定し直します。
Issue 番号と PR 番号は同じとは限りません。

## CI が実行されない・失敗する

PR の **Checks** またはリポジトリの **Actions** を開きます。
実行されない場合は、Actions の許可、PR の base が main であること、ワークフローが存在することを確認します。
本教材では main への Push と main 向け PR で実行します。feature への Push だけでは、PR 作成前の CI は動きません。

失敗した場合は、失敗ステップとログを読みます。
テスト失敗ならローカルで `uv run pytest` を実行し、同じブランチで修正・Commit・Push します。
ダウンロードやサービス側の一時障害なら、原因を確認してから再実行します。
CI を削除したりテストを無効化したりして成功扱いにしないでください。

## 自分の PR を Approve できない・マージできない

自分の PR を承認できないのは GitHub の仕様です。本編では Comment 形式のレビューを使います。
承認必須ルールがあるリポジトリでは一人で完了できないため、各自が管理する研修用リポジトリの設定を確認します。
組織が管理するルールは変更せず、講師に相談します。

Squash and merge が無効なら、自分の研修用リポジトリの Settings → General → Pull Requests で有効にするか、
許可された **Create a merge commit** を使います。どちらも main へ反映されます。

## マージしても Issue が閉じない

- PR の本文に `Closes #実際のIssue番号` があるか確認します。
- PR が main（既定ブランチ）へマージされたか確認します。
- Issue と PR が自分の同じリポジトリにあるか確認します。

記載漏れなら PR 本文を修正してリンクを記録し、すでにマージ済みの場合は Issue に完了した PR をコメントして手動で閉じます。
自動クローズの確認は、次の課題でマージ前にキーワードを記載して試します。
