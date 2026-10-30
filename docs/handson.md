# ハンズオン：割り算の Issue からマージまで

[README](../README.md) · [環境準備](setup.md) · [困ったとき](troubleshooting.md)

環境準備を終え、自分のリポジトリで初期テスト12件が成功している状態から始めます。
コマンドはすべて WSL2 Ubuntu の Bash で、リポジトリのルートから実行します。
`text` のコードブロックは AI への指示、`bash` はターミナルでの操作です。

## 1. 実装者：Issue を起票する（10分）

自分のリポジトリの GitHub 画面で **Issues → New issue → 機能追加**を選びます。
タイトルを「電卓に割り算を追加する」にし、本文を以下に置き換えます。

```markdown
## 背景
現在の電卓は加算・減算・乗算に対応しているが、割り算ができない。
他の演算と同じように、関数を呼び出して割り算を使いたい。

## 変更内容
calculator.py に divide(a: float, b: float) -> float を追加する。
Python の通常の除算と同様に a / b の結果を返す。

## 受け入れ条件
- [ ] divide(6, 3) が 2.0 を返す
- [ ] divide(5, 2) が 2.5 を返す（切り捨てない）
- [ ] 小数入力の divide(0.3, 0.1) が約 3.0 を返す
- [ ] divide(-6, 3) が -2.0、divide(6, -3) が -2.0 を返す
- [ ] divide(0, 3) が 0.0 を返す
- [ ] 分母が 0 または 0.0 のとき ZeroDivisionError を送出する
- [ ] 上記のテストと既存のテストが uv run pytest で成功する

## 今回扱わないこと
CLI・画面の追加、入力文字列の変換、例外メッセージの指定、
NaN・無限大の独自処理、既存の演算の仕様変更。
```

起票後に **実際の Issue 番号と URL** を控えてください。
Issue 番号は `1` とは限りません。以下では例として `7` を使います。

CLI を使う場合も同じ Issue は一度だけ作成します。
本文を `/tmp/issue-driven-issue.md` に保存して次のコマンドで起票できます。
一時ファイルはリポジトリの外へ置き、演習の Commit には含めません。

```bash
gh issue create --title "電卓に割り算を追加する" --body-file /tmp/issue-driven-issue.md
```

**確認**：目的と「できたかどうかを判定する条件」が、実装前に言葉になっています。

## 2. 実装者：作業ブランチを作る（5分）

`ISSUE_NUMBER` の値を自分の番号に置き換えます。この値は同じターミナル内で後から使います。

```bash
git switch main
git pull --ff-only origin main
git status --short
ISSUE_NUMBER=7
git switch -c "feature/${ISSUE_NUMBER}-add-division"
git branch --show-current
gh issue view "$ISSUE_NUMBER"
```

`git status --short` に変更がある場合は先に内容を確認してください。
ブランチは同じリポジトリ内で作業を分ける仕組みです。main へ直接実装せず、PR で変更を確認できるようにします。

## 3. 実装者：判断理由を学習用 ADR に残す（10分）

Issue は「何を作り、何ができれば完了か」、ADR（Architecture Decision Record）は「なぜその選択をしたか」を残します。
今回は Issue で決めた割り算の仕様について、判断理由を短い文書にする練習です。
戻り値を通常の除算に揃えることと、ゼロ除算を例外にすることを1件にまとめます。

### 通常の開発で grill-with-docs を使う場合

設計や仕様を相談する際は、次の流れで判断理由を記録できます。

1. 開発者が `grill-with-docs` を実行し、実現したい機能や設計案を伝えます。
2. AI エージェントが前提・選択肢・制約について質問し、開発者が回答します。
3. 対話の中で判断が固まると、AI エージェントが回答内容と合意した理由に応じて ADR の作成を提案し、必要な記録を `docs/adr/` に追加します。
4. 開発者が ADR の内容を確認し、後の実装や PR レビューで参照します。

`grill-with-docs` は内部で `grilling` と `domain-modeling` を使い、対話と文書化を進めます。
ADR は質問への回答がすべて終わった後に一括で作るとは限らず、対話中に判断が固まった時点で記録されます。
記録すべき判断が生じたときに ADR が増えていく仕組みで、実行するたびに必ずファイルが作られるわけではありません。
参照：[grill-with-docs](https://github.com/mattpocock/skills/blob/main/skills/engineering/grill-with-docs/SKILL.md)、
[domain-modeling](https://github.com/mattpocock/skills/blob/main/skills/engineering/domain-modeling/SKILL.md)。

### 今回は短い学習用の手順で作成する

実務では、この規模の変更に ADR が必須とは限りません。
mattpocock/skills も、変更コストが大きく、背景なしでは分かりにくく、実際の選択肢の比較がある場合に作成を提案します。
今回は **ADR の作成・参照・レビューを体験するための学習用** として明示的に作成します。
`grill-with-docs` の実行や Skills の追加インストールは不要です。

`claude` または `codex` を起動し、通常のチャットへ以下を入力します。
`#7` は自分の Issue 番号へ置き換えてください。

```text
GitHub 開発フローの研修で、学習用 ADR を1件作成します。
今回は小さな電卓なので grill-with-docs は実行しません。
Issue #7 と calculator.py を読み、Issue ですでに決めた仕様の理由を整理してください。

次の代替案について、呼び出し側にどのような違いが出るか短く比較してください。
- 割り算の結果をそのまま返す案と、整数に切り捨てる案
- ゼロ除算で ZeroDivisionError を送出する案と、None や 0 を返す案

Issue の仕様を採用する理由と、その結果呼び出し側が注意することを、
私が理解できるよう説明してください。実際には話し合っていない経緯を作らないでください。
その後、背景・決定・比較した選択肢と理由・影響を含む短い ADR 案を示して停止してください。
Issue へのリンクも含めてください。まだファイルの保存や実装、Commit、Push はしないでください。
```

案を読み、「なぜ 0 を返してはいけないか」「例外が出ると呼び出し側は何をする必要があるか」を自分の言葉で説明します。
分からない点は AI に質問し、理由に納得してから保存を依頼します。

```text
この判断を採用します。確認した ADR 案を docs/adr/0001-division-policy.md に保存してください。
最初に docs/adr/ を確認し、既存の ADR がある場合は上書きせず、最大番号の次の番号で保存してください。
今回は学習用であることを本文にも記載してください。
実装、Commit、Push はまだ行わないでください。
```

期待する構成は次のとおりです。完成済みの ADR は教材に入れていないため、自分の確認した理由を保存します。

```text
docs/adr/
└── 0001-division-policy.md
```

保存先は小文字の `docs/adr/` です。既存ファイルがあれば採番結果に合わせて、以降のパスも読み替えます。
短い ADR で十分です。大きな設計書や詳細な議事録は作りません。
公式の形式も短い文章を基本にしています：[ADR-FORMAT.md](https://github.com/mattpocock/skills/blob/main/skills/engineering/domain-modeling/ADR-FORMAT.md)。

**確認**：Issue の条件を写しただけではなく、代替案を採用しなかった理由と、採用した仕様の影響が書かれています。

## 4. 実装者：Skills でテストと実装を進める（30分）

前の工程の AI セッションを使います。終了していた場合は `claude` または `codex` を起動します。
以下の例は Issue `7` なので、**送信前に自分の番号または URL へ置き換えます**。
AI 内には Bash の `ISSUE_NUMBER` 変数は自動では展開されません。

| 目的 | Claude Code 内 | Codex 内 |
| --- | --- | --- |
| 実装 | `/implement` | `$implement` |
| TDD を個別に使う | `/tdd` | `$tdd` |
| レビューを個別に使う | `/code-review` | `$code-review` |

候補一覧で mattpocock/skills 由来のものを選びます。名前が衝突する場合は一覧に表示される正式名を使ってください。
標準の `implement` は TDD とコードレビューを組み込み、最後に Commit します。
今回は Git の学習のため、Commit を自分で行う指示を明示します。

**Claude Code では `/implement`、Codex では `$implement` に続けて入力：**

```text
自分の origin リポジトリの Issue #7 を実装してください。
まず Issue を取得し、タイトルと受け入れ条件を示してください。
docs/adr/ の割り算の ADR を読み、決定と理由を確認してください。
Issue・ADR・実装に矛盾があれば、勝手に書き換えず私に確認してください。
現在の feature ブランチで calculator.py と tests/test_calculator.py を変更します。
ADR は前の工程で作成済みなので、今回は参照してください。
Python 環境とテストは uv で管理し、uv run pytest を使ってください。

研修なので、次の順で人間が確認しながら進めます。
1. 最初の割り算テストを1つだけ追加し、実行して意図した失敗を示して停止する。
2. 私が「続けて」と伝えたら最小実装して成功を確認する。
3. 受け入れ条件を1つずつテスト→実装の順で満たす。
4. 全テストと code-review を実行し、結果と残る課題を示す。

この指示は implement の標準の Commit 手順より優先します。
Commit、Push、Issue の更新・クローズ、PR 作成・マージは行わないでください。
課題の完成コードを先に一括生成しないでください。
```

最初の失敗を確認します。新しい `divide` が存在しないことによる ImportError や AttributeError は、この段階では想定内です。
uv や pytest が起動しない、ファイル名が誤っているなど、課題と関係ない失敗は先に直します。

**AI が停止したら確認すること：**

- 追加されたテストは、Issue のどの条件を検証しているか。
- 実装前に失敗している理由を説明できるか。
- そのテストが、関数を実装すれば成功する内容になっているか。

理解できたら「続けて」と伝えます。小数の比較は `pytest.approx`、ゼロ除算の検証は `pytest.raises` を使うよう依頼できます。
浮動小数点では計算結果が厳密一致しない場合があるため、小数の期待値には許容誤差を使います。

AI がテストと実装を終えたら、レビュー結果を読み、必要な修正を依頼します。
`implement` が Skills を内部で呼べない環境では、同じ制約を添えて `tdd`、実装完了後に `code-review` を個別に呼び出します。

最後に AI を終了して、自分でも実行します。

```bash
uv run pytest
uv run python -c 'from calculator import divide; print(divide(5, 2))'
git diff --check
git diff
git status --short
```

**期待結果**：全テスト成功、動作例は `2.5`。テスト数は追加方法で変わるので、実際の結果を記録します。
変更対象は `calculator.py`、`tests/test_calculator.py` と、前の工程で作成した ADR です。
新規の ADR は `git diff` には表示されないため、`git status --short` とファイルを開いて内容を確認します。

## 5. 実装者：Commit・Push する（5分）

Commit はローカルの履歴への保存、Push はその履歴を GitHub に送る操作です。
まず保存する差分を自分で確認します。

```bash
git add calculator.py tests/test_calculator.py docs/adr/
git diff --cached
git commit -m "feat: add division support"
git push -u origin HEAD
git status --short
```

**確認**：GitHub に feature ブランチがあり、変更が Commit され、作業ツリーがクリーンになっています。
AI がすでに Commit していた場合は[対処方法](troubleshooting.md)を確認します。

## 6. 実装者：PR を作る（10分）

自分の GitHub リポジトリで **Pull requests → New pull request** を選びます。

- base：`main`
- compare：自分の `feature/番号-add-division`
- タイトル：`電卓に割り算を追加する`

テンプレートへ次の内容を記載します。

```markdown
## 目的・変更内容
Issue の要望に対応し、calculator.py に divide を追加した。
通常の除算とゼロ除算のテストを追加した。
仕様の選択理由を docs/adr/0001-division-policy.md に記録した。

## 関連 Issue
Closes #7

## 確認結果
- 実行コマンド: uv run pytest
- 結果: （自分が実行した件数）passed
- 変更前: divide 関数がなく、割り算を呼び出せない
- 変更後: divide(5, 2) が 2.5 を返す

## セルフレビュー
- [ ] Issue の受け入れ条件を満たしている
- [ ] 正常系・境界値・エラーのテストを確認した
- [ ] ADR の理由を理解し、Issue・実装・テストとの整合性を確認した
- [ ] Files changed に意図しない変更がない
```

`#7`、ADR のパス、テスト件数を実際の値に置き換え、**Create pull request** で作成します。
チェック欄は次のレビューで確認してからチェックします。
PR 番号と Issue 番号は別の番号です。

PR 本文の `Closes #番号` により、既定ブランチへのマージ時に Issue が自動で閉じます。
PR を作っただけでは閉じません。
詳細：[GitHub の Issue と PR のリンク](https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/linking-a-pull-request-to-an-issue)。

CLI で作る場合は、上記本文を `/tmp/issue-driven-pr.md` に保存し、以下を使います。UI で作成済みなら実行しません。

```bash
gh pr create --base main --title "電卓に割り算を追加する" --body-file /tmp/issue-driven-pr.md
```

## 7. レビュー担当：一人二役で確認する（20分）

ここで実装者からレビュー担当へ切り替えます。AI の評価も参考にしつつ、自分でコードを読んで確認します。

1. Issue の受け入れ条件を読み直します。
2. PR の **Files changed** で、関数とテストを読みます。
3. 各条件に対応するテストがあり、期待値が正しいことを確認します。
4. ADR に選択理由があり、その決定が Issue・実装・テストと一致していることを確認します。
5. 既存機能の削除や `.venv` など意図しないファイルがないことを確認します。
6. **Checks** で `Tests / pytest` が成功したことを確認します。
7. Files changed → **Review changes → Comment → Submit review** でレビューを残します。

自分の PR では Approve を選べません。Comment 形式で完了します。
根拠：[GitHub の承認レビューの制約](https://docs.github.com/en/pull-requests/how-tos/review-pull-requests/approving-a-pull-request-with-required-reviews)。

**問題がなかった場合のコメント例：**

```text
受け入れ条件をコードとテストに照らして確認しました。
整数の割り算が切り捨てられないこと、小数・負数・分子ゼロ、
ゼロ除算の例外がテストされていることを確認しました。
ADR の代替案と選択理由を読み、実装が決定に従っていることも確認しました。
既存の演算の変更はなく、Tests / pytest も成功しています。
現時点で修正を依頼する点はありません。
```

実際に確認した内容に書き換えます。問題を見つけたら、対象行にコメントを残し、期待する動作と理由を書きます。
練習のために架空の問題を作る必要はありません。

### 修正が必要な場合

実装者へ戻り、同じ feature ブランチで修正します。AI に依頼する場合も Commit と Push は自分で行います。

```bash
uv run pytest
git diff
git add calculator.py tests/test_calculator.py
# ADR も修正した場合だけ追加する
git add docs/adr/
git commit -m "fix: address review feedback"
git push
```

同じ PR に追加の Commit が反映されます。新しい PR は作りません。
CI の再実行が成功したら、修正を確認したコメントを残し、行コメントの会話を解決します。
PR 本文のテスト結果とセルフレビューのチェック欄も更新します。

CLI の確認・レビューは次のコマンドでもできます。現在のブランチの PR が対象です。

```bash
gh pr diff
gh pr checks
gh pr review --comment --body "受け入れ条件と差分、テスト結果を確認しました。詳細は PR 本文に記載しました。"
```

## 8. 実装者：マージして完了を確認する（10分）

1. PR のチェック欄と CI 成功、未対応の指摘がないことを確認します。
2. **Squash and merge** を選んでマージを確定します。
3. **Delete branch** で GitHub 側の作業ブランチを削除します。
4. Issue が **Closed** になり、マージした PR へのリンクがあることを確認します。

CLI でマージする場合は UI 操作の代わりに実行します。

```bash
gh pr merge --squash
```

ローカルを最新の main に揃えます。

```bash
git switch main
git pull --ff-only origin main
git fetch --prune
uv sync
uv run pytest
uv run python -c 'from calculator import divide; print(divide(5, 2))'
git status --short
```

**完了**：PR は Merged、Issue は Closed、main で全テスト成功、動作例は `2.5` です。
GitHub の main で `docs/adr/` を開き、自分が作成した ADR が残っていることも確認します。
ローカルの feature ブランチは残して構いません。

最後に、Issue・ブランチ・Commit・Push・PR・レビューそれぞれの役割を自分の言葉で説明してみてください。
ADR は何を記録し、Issue とどう違うかも説明してみてください。
この演習で残る ADR は1件です。継続開発では、記録すべき別の判断が生じたときに `0002-...md` のように追加します。
機能追加ごとに必ず ADR を増やす必要はありません。

## 発展：to-spec で次の課題を起票する

本編を終えてから、例えば「余りを求める関数を追加する」を AI と相談します。
仕様と受け入れ条件を会話で決め、Claude Code の `/to-spec` または Codex の `$to-spec` を明示的に呼び出します。
この Skill は会話を仕様にまとめて Issue tracker に公開します。起票先と本文を確認してから作成させてください。
本編の割り算 Issue は再作成しません。

手動起票と AI による起票の違いを比べ、どちらでも人間が目的と受け入れ条件を確認する必要があることを振り返ります。
