## python の環境構築

1. **仮想環境の作成とアクティベート**

まず、仮想環境を作成してアクティベートします。これにより、必要なパッケージをインストールするための独立した環境が用意されます。

[venv の使い方と説明を参考に](https://packaging.python.org/ja/latest/guides/installing-using-pip-and-virtual-environments/)

```bash
python -m venv venv
source venv/bin/activate  # macOS/Linuxの場合
venv\Scripts\activate  # Windowsの場合はこちら
```

2. requirements.txt 　ファイルを使ってパッケージをインストールするためには、以下のコマンドを使用します。

```bash
pip install -r requirements.txt
```

3. 仮想環境の無効化（必要に応じて）

```bash
deactivate
```

## Function Calling や画像データを送る API の参考にしたリンク

[画像を送る API](https://platform.openai.com/docs/guides/vision)
[function calling](https://platform.openai.com/docs/assistants/tools/function-calling/quickstart)
