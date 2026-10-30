# Issue → 実装 → PR を一人二役で学ぶハンズオン

Python の小さな電卓に割り算を追加し、GitHub の開発フローを体験します。
実装者とレビュー担当を自分で交代し、各自のリポジトリで完結できます。
AI には mattpocock/skills を使い、GitHub の主要操作は自分で行います。

**対象環境は Windows の WSL2 Ubuntu（Bash）です。** コマンドは Ubuntu のターミナルで実行してください。
Python の仮想環境と依存関係は uv で管理します。Claude Code または Codex のどちらかを選んで進められます。

## 学習目標

- Issue に目的と受け入れ条件を書く
- 仕様を選んだ理由を学習用 ADR に残し、実装と一緒にレビューする
- 作業ブランチでテストと実装を変更する
- Commit と Push の違いを理解する
- PR に変更理由とテスト結果を記載し、Issue を紐付ける
- 差分と CI を確認し、レビューコメントを残してマージする

## 進め方

1. [環境準備](docs/setup.md)で、WSL2 Ubuntu、ツール、各自のリポジトリ、Skills を準備します。
2. [ハンズオン本編](docs/handson.md)に沿って、Issue からマージまで進めます。
3. 詰まった場合は[トラブルシューティング](docs/troubleshooting.md)を確認します。

講師・教材管理者向けの注意事項は[講師ガイド](docs/instructor.md)にまとめています。
動画視聴は不要です。Python の関数と基本的なターミナル操作を知っている方を想定しています。

| 内容 | 目安 |
| --- | ---: |
| 環境準備 | 事前に実施（30〜60分程度） |
| Issue 起票・ブランチ作成 | 15分 |
| 学習用 ADR の作成 | 10分 |
| Skills によるテスト・実装 | 30分 |
| Commit・Push・PR | 15分 |
| 一人二役レビュー・必要な修正 | 20分 |
| マージ・振り返り | 10分 |

本編は合計約100分です。ADR は小さな判断を題材に1件作成し、Git の履歴に残します。
実務での作成基準とは分けた学習用の工程で、`grill-with-docs` の実行は不要です。

## サンプルの初期状態

`calculator.py` には `add`、`subtract`、`multiply` が実装済みです。
割り算の関数とテストは受講者が追加します。開始時点のテストは12件すべて成功します。

Clone 後、リポジトリのルートで実行します。

```bash
uv sync
uv run pytest
uv run python -c 'from calculator import add; print(add(2, 3))'
```

`uv sync` が `.venv` を作成します。activate や `pip install` は不要です。
`uv.lock` は Git で共有し、`.venv` は共有しません。

## 完了チェック

- [ ] 自分の GitHub リポジトリに受け入れ条件付きの Issue がある
- [ ] main 以外のブランチで割り算とテストを追加した
- [ ] `docs/adr/` に判断理由を記録し、実装との整合性をレビューした
- [ ] テストの失敗と成功を確認した
- [ ] PR に関連 Issue と実際のテスト結果を書いた
- [ ] 自分で差分を読み、Comment 形式のレビューを残した
- [ ] CI が成功している
- [ ] PR をマージし、Issue の自動クローズを確認した
- [ ] ローカルの main を更新して動作確認した

## 参照元

外部ツールの導入方法と Skills の名称は 2026-10-30 に公開ドキュメントで確認しました。
バージョンによって画面や呼び出し方法が変わる場合は、各ツールの候補表示と公式手順を確認してください。

- [mattpocock/skills](https://github.com/mattpocock/skills)
- [uv: Working on projects](https://docs.astral.sh/uv/guides/projects/)
- [Claude Code: Skills](https://code.claude.com/docs/en/skills)
- [OpenAI: Build skills](https://learn.chatgpt.com/docs/build-skills)
- [GitHub: GitHub flow](https://docs.github.com/en/get-started/using-github/github-flow)
