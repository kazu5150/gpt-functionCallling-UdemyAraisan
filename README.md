# レシート処理自動化ツール

このプロジェクトは、レシート画像を自動的に処理し、重要な情報を抽出してExcelファイルに保存するPythonスクリプトです。OpenAI GPT-4 APIを使用して画像認識と情報抽出を行います。

## 機能

- 指定されたディレクトリからランダムにレシート画像（PNG形式）を選択
- 選択された画像をBase64エンコード
- OpenAI GPT-4 APIを使用して画像から以下の情報を抽出:
  - 購入日
  - 店舗名
  - 購入品の説明
  - 合計金額
- 抽出された情報をExcelファイルに保存
- 処理済みの画像を別のディレクトリに移動

## 必要条件

- Python 3.6以上
- 以下のPythonライブラリ:
  - os
  - base64
  - requests
  - openpyxl
  - json
  - random
  - dotenv
  - shutil

## インストール方法

1. このリポジトリをクローンするか、ZIPファイルとしてダウンロードします。

```
git clone https://github.com/yourusername/receipt-processor.git
cd receipt-processor
```

2. 仮装環境を作成し、必要なライブラリをインストールします。

```
python -m venv myvenv
source myvenv/bin/activate

pip install -r requirements.txt
```

3. `.env`ファイルを作成し、OpenAI APIキーを設定します。

```
OPENAI_API_KEY=your_api_key_here
```

## 使用方法

1. レシート画像（PNG形式）を`reciet`ディレクトリに配置します。

2. スクリプトを実行します。

```
python receipt_processor.py
```

3. 処理結果は`receipts.xlsx`ファイルに保存されます。

4. 処理済みの画像は`reciet_done`ディレクトリに移動されます。

## プロジェクト構造

```
receipt-processor/
│
├── receipt_processor.py  # メインスクリプト
├── .env                  # 環境変数（APIキー）
├── requirements.txt      # 必要なPythonライブラリ
├── reciet/               # 処理前のレシート画像を格納するディレクトリ
├── reciet_done/          # 処理済みのレシート画像を移動するディレクトリ
└── receipts.xlsx         # 抽出されたデータを保存するExcelファイル
```

## 注意事項

- このスクリプトを使用するには、有効なOpenAI APIキーが必要です。
- 大量の画像を処理する場合は、APIの使用制限と料金に注意してください。
- レシート画像は個人情報を含む可能性があるため、適切なセキュリティ対策を講じてください。

## ライセンス

このプロジェクトは [MITライセンス](LICENSE) のもとで公開されています。

## 貢献方法

1. このリポジトリをフォークします。
2. 新しい機能ブランチを作成します (`git checkout -b feature/AmazingFeature`)
3. 変更をコミットします (`git commit -m 'Add some AmazingFeature'`)
4. ブランチにプッシュします (`git push origin feature/AmazingFeature`)
5. プルリクエストを作成します。

