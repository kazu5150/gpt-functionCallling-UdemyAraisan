# cron の設定

1. 下記コマンドを入力

```bash
which python
```

このコマンドで出力した python が現在使っている python です！

2. 下記のシェルファイル python_index.sh を作る

```sh
#!/bin/bash

# 仮想環境のアクティベート
source /<your file path>/python_risou3/venv/bin/activate

# スクリプトのディレクトリに移動
cd /<your file path>/python_risou3

# スクリプトの実行
python index.py
```

3. シェルの権限を変更して実行できるようにして、crontab を開く

```bash
chmod +x python_index.sh
crontab -e
```

4. crontab -e 　の後にこのコードを貼り付け

```bash
* * * * * /bin/bash /<your file path>/python_risou3/python_index.sh >> /<your file path>/python_risou3/cron.log 2>&1
```
