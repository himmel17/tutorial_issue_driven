# 環境準備：WSL2 Ubuntu

[README に戻る](../README.md) · 準備後は[本編](handson.md)へ

## 1. Ubuntu のターミナルを開く

WSL2 と Ubuntu が利用できる状態を前提にします。未導入の場合は
[Microsoft の WSL 導入手順](https://learn.microsoft.com/ja-jp/windows/wsl/install)で先に準備してください。
以降は Windows の PowerShell ではなく **WSL2 Ubuntu の Bash** で実行します。
ブラウザーの GitHub 操作は Windows 側で構いません。

作業場所は Ubuntu 内の `~/src` にします。

```bash
mkdir -p ~/src
cd ~/src
sudo apt update
sudo apt install -y git curl gh
```

GitHub アカウント、インターネット接続、Claude Code または Codex を利用できる契約・認証も必要です。
会社の利用ルールがある場合は、その環境と認証方法を使用してください。

## 2. uv と Git を準備する

[uv の公式インストーラー](https://docs.astral.sh/uv/getting-started/installation/)を使います。
既に uv がある場合はインストールを省略できます。

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
source "$HOME/.local/bin/env"
uv --version
git --version
gh --version
```

この教材の CI は uv 0.8.22 を使用します。それ以降の uv で進められます。
Python 本体は後で `uv python install` により導入するので、Ubuntu のシステム Python を変更する必要はありません。

Git の作者情報を確認します。

```bash
git config --global --get user.name
git config --global --get user.email
```

未設定の場合だけ、自分の情報に置き換えて設定します。
メールアドレスには GitHub の Settings → Emails に表示される自分の noreply アドレスも使えます。

```bash
git config --global user.name "あなたの名前"
git config --global user.email "あなたのメールアドレス"
```

GitHub CLI を認証します。GitHub.com、HTTPS、ブラウザーでのログインを選び、表示されたコードをブラウザーで入力します。
Git の認証にも使用するか聞かれたら Yes を選びます。

```bash
gh auth login
gh auth setup-git
gh auth status
```

## 3. 自分のリポジトリを作る

1. GitHub にログインし、右上の `+` → **Import repository** を開きます。
2. Source repository URL に `https://github.com/himmel17/tutorial_issue_driven.git` を入力します。
3. Owner は自分、Repository name は `issue-driven-handson` にします。公開範囲は自分の環境に合わせて選びます。
4. Import を開始し、完了後、自分のリポジトリを開きます。
5. Settings → General → Features で **Issues** を有効にします。
6. Settings → Actions → General で、この教材が使う Actions を実行できることを確認します。
7. 既定ブランチが `main` であることを確認します。一人で完結させるため、承認必須ルールは設定しません。

Fork ではなく独立したコピーを作ることで、Issue と PR の送信先を自分に揃えます。
Import 元に教材の Commit がまだ公開されていない場合は、講師が公開してから進めてください。

Ubuntu のターミナルで、自分の GitHub ユーザー名を設定して Clone します。

```bash
GITHUB_USER=あなたのGitHubユーザー名
cd ~/src
git clone "https://github.com/${GITHUB_USER}/issue-driven-handson.git"
cd issue-driven-handson
git remote -v
gh repo view
```

**確認**：`origin` と `gh repo view` が自分の `issue-driven-handson` を指していること。
以降のコマンドは、このリポジトリのルートで実行します。

## 4. Python 環境を作る

```bash
uv python install
uv sync --locked
uv run --locked python --version
uv run --locked pytest
uv run --locked python -c 'from calculator import add; print(add(2, 3))'
```

**期待結果**：Python 3.12 系、`12 passed`、加算結果 `5`。

| ファイル・ディレクトリ | 役割 | Git で共有 |
| --- | --- | --- |
| `.python-version` | 使用する Python 系列 | する |
| `pyproject.toml` | プロジェクトと開発依存の定義 | する |
| `uv.lock` | 依存の解決結果 | する |
| `.venv/` | uv が作る仮想環境 | しない |

`uv run` が仮想環境内のコマンドを実行します。`source .venv/bin/activate` は不要です。
依存を追加する場合は `uv add --dev パッケージ名` を使用しますが、この演習では追加不要です。

## 5. AI ツールと Skills を準備する

Claude Code または Codex の **どちらか一方**を WSL2 Ubuntu 内で準備し、ログインしてください。
インストール方法は [Claude Code](https://code.claude.com/docs/en/setup) または
[Codex CLI](https://developers.openai.com/codex/cli/) の公式手順を使用します。

この教材では [mattpocock/skills が案内するファイル配置方式](https://github.com/mattpocock/skills#installation-30-second-setup)
を使い、必要な5つだけをリポジトリ内へ導入します。同じ Skills をプラグインでも導入済みの場合は、二重導入を避けて既存のものを使ってください。

この方式には Ubuntu 内の Node.js 22.20 以上（LTS）と npm / npx が必要です。
未導入の場合は [Node.js の公式ダウンロード案内](https://nodejs.org/en/download)で WSL2 Ubuntu 向けに準備し、確認します。

```bash
node --version
npm --version
npx --version
```

### Claude Code を使う場合

Ubuntu のターミナルで実行します。インストーラーの確認では、このプロジェクトへの配置を選びます。

```bash
npx skills@latest add mattpocock/skills --agent claude-code --skill setup-matt-pocock-skills implement tdd code-review to-spec
claude
```

Claude Code 内で `/setup-matt-pocock-skills` を候補から選んで実行します。
以下の AI 向け指示も同じメッセージに添えてください。

### Codex を使う場合

```bash
npx skills@latest add mattpocock/skills --agent codex --skill setup-matt-pocock-skills implement tdd code-review to-spec
codex
```

Codex 内で `$setup-matt-pocock-skills` を候補から選んで実行します。
以下の AI 向け指示も同じメッセージに添えてください。
Skills が出ないときは導入後に AI ツールを再起動します。

### 初期設定時に添える指示（AI に入力）

```text
GitHub 開発フローの研修を準備しています。
Issue tracker は origin の自分の GitHub リポジトリを使います。
単一の小さな Python プロジェクトで、実行とテストは uv で管理します。
設定先を聞かれたら AGENTS.md を選びます。
Claude Code 向けの案内が必要なら CLAUDE.md から AGENTS.md を参照してください。
テストコマンドは uv run --locked pytest です。
Issue、PR、ラベルはまだ作らず、Commit・Push も行わないでください。
今回の変更は Skills の初期設定用ファイルに限定し、設定案を確認させてください。
```

この選択では `triage` を導入しないので、triage ラベル作成は不要です。
初期設定の案を読み、自分のリポジトリを参照していることを確認して保存させます。
設定ファイルが教材元のリポジトリを指していたら修正させてください。

AI を終了してターミナルへ戻り、準備の変更を main に保存します。
`git status` に表示された設定ファイルだけを `git add` で指定してください。
典型例は `AGENTS.md`、`docs/agents/`、Claude Code 用の `CLAUDE.md` です。
存在しないパスは指定しません。

```bash
git status --short
git diff
# 実際に生成されたパスに合わせて実行する
git add AGENTS.md docs/agents/
git diff --cached
git commit -m "docs: configure agent skills for training"
git push origin main
git status --short
```

`CLAUDE.md` も生成された場合は Commit 前に `git add CLAUDE.md` します。
外部 Skills 本体は `.gitignore` の対象です。`.venv/` や認証情報は追加しません。

**準備完了**：作業ツリーがクリーンで、初期テスト12件が成功し、AI が必要な Skills を認識する状態です。

導入方法の参照：[Skills CLI](https://github.com/vercel-labs/skills)、
[Claude Code Skills](https://code.claude.com/docs/en/skills)、
[OpenAI Skills](https://learn.chatgpt.com/docs/build-skills)。確認日：2026-10-30。
