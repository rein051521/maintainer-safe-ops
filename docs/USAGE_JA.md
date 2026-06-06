# 使い方ガイド（日本語）

maintainer-safe-ops は、リポジトリを公開・マージ・リリースする前に、安全性と OSS 準備状況をチェックする軽量な CLI / GitHub Action です。

## インストール（ソースから）

```bash
git clone https://github.com/rein051521/maintainer-safe-ops.git
cd maintainer-safe-ops
python -m venv .venv
source .venv/bin/activate        # Windows は .venv\Scripts\activate
pip install -e ".[dev]"
```

## ローカルでの CLI 実行

カレントディレクトリをスキャンします。

```bash
maintainer-safe-ops .
```

出力形式は `human`（既定）・`json`・`sarif` から選べます。

```bash
maintainer-safe-ops . --format json
maintainer-safe-ops . --format sarif > maintainer-safe-ops.sarif
```

高深刻度（high）のみで失敗させたい場合:

```bash
maintainer-safe-ops . --fail-on high
```

終了コード: `0`=問題なし / `1`=ブロッキング検出または必須 OSS ファイル欠如 / `2`=実行エラー。

## GitHub Actions での実行

```yaml
name: Maintainer Safe Ops

on:
  pull_request:
  push:
    branches: [main]

jobs:
  safe-ops:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: rein051521/maintainer-safe-ops@v0.1.2
        with:
          path: "."
          format: "human"
          fail-on: "medium"
```

## 誤検知の除外

`.maintainer-safe-ops.json` で、テスト用フィクスチャなど意図的に危険な文字列を含むパスを除外できます。

```json
{
  "exclude": [
    "tests/**",
    "examples/risky-project/**"
  ]
}
```

## 制限と注意

- 本ツールは正規表現ベースの軽量な目安チェックであり、専用のシークレットスキャナや SAST の置き換えではありません。
- 検出がゼロでも「秘密情報や脆弱性が存在しない」ことを保証するものではありません。
- 高リスクなプロジェクトでは、専用スキャナと人手によるレビューを併用してください。
