# 必要なライブラリをインポートします。
import os
import base64
import requests
import openpyxl
import json
import random
from dotenv import load_dotenv
import shutil

# .envファイルから環境変数を読み込みます。これにより、APIキーなどの機密情報をコード内に直接書かずに済みます。
load_dotenv()

# 環境変数からAPIキーを取得します。
api_key = os.getenv("OPENAI_API_KEY")

# 画像が格納されているディレクトリと、処理が完了した画像を移動するディレクトリのパスを設定します。
image_dir = "reciet"
done_dir = "reciet_done"

# レシート情報を保存するExcelファイルのパスを設定します。
excel_path = "receipts.xlsx"


# 画像ファイルをBase64エンコードする関数を定義します。
def encode_image(image_path):
    # 画像ファイルを読み込み、Base64形式に変換します。
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


# 画像ファイルを処理済みディレクトリに移動する関数を定義します。
def move_image_to_done(image_path, done_dir):
    # 処理済みディレクトリが存在しない場合は作成します。
    if not os.path.exists(done_dir):
        os.makedirs(done_dir)
    # 画像ファイルを処理済みディレクトリに移動します。
    shutil.move(image_path, done_dir)


# レシート情報を抽出するためにAPIリクエストを送信する関数を定義します。
def extract_receipt_info(base64_image):
    # APIリクエストのヘッダーを設定します。Content-Typeをapplication/jsonにし、認証情報を含めます。
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"}

    # 関数の定義を含むリクエストペイロードを設定します。ここでは、購入日、店舗名、商品説明、金額の抽出を要求しています。
    functions = [
        {
            "name": "extract_receipt_data",
            "description": "Extracts key information from a receipt image",
            "parameters": {
                "type": "object",
                "properties": {
                    "purchase_date": {
                        "type": "string",
                        "description": "The date of purchase in YYYY-MM-DD format",
                    },
                    "store_name": {
                        "type": "string",
                        "description": "The name of the store",
                    },
                    "description": {
                        "type": "string",
                        "description": "A brief description of the items purchased",
                    },
                    "amount": {
                        "type": "number",
                        "description": "The total amount of the purchase",
                    },
                },
                "required": ["purchase_date", "store_name", "description", "amount"],
            },
        }
    ]

    # APIリクエストのペイロードを作成します。画像をBase64形式で含めます。
    payload = {
        "model": "gpt-4o",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "このレシート画像からデータを抽出して、日本語で返してください。",
                    },
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/png;base64,{base64_image}"},
                    },
                ],
            }
        ],
        "functions": functions,
        "function_call": {"name": "extract_receipt_data"},
    }

    # 作成したペイロードを確認のために表示します。
    print("Payload:", json.dumps(payload, indent=2, ensure_ascii=False))

    # APIエンドポイントに対してPOSTリクエストを送信し、レスポンスを取得します。
    response = requests.post(
        "https://api.openai.com/v1/chat/completions", headers=headers, json=payload
    )
    result = response.json()

    # レスポンスから抽出されたデータを取得します。
    if "function_call" in result["choices"][0]["message"]:
        function_args = json.loads(
            result["choices"][0]["message"]["function_call"]["arguments"]
        )
        return function_args
    else:
        # エラーメッセージを表示します。
        print("Error: Function call not found in the response")
        return None

#    try:
#        if "function_call" in result:
#            function_response = result["function_call"]
#            extracted_data = json.loads(function_response["arguments"])
#            return extracted_data
#        else:
#            print("Unexpected response structure:")
#            print(json.dumps(result, indent=2))
#            return None
#    except KeyError as e:
#        print(f"KeyError: {e}")
#        print("Unexpected response structure:")
#        print(json.dumps(result, indent=2))
#        return None


# 抽出したデータをExcelファイルに追加する関数を定義します。
def update_excel_with_data(data, excel_path):
    # Excelファイルが存在する場合は開き、存在しない場合は新規作成します。
    if os.path.exists(excel_path):
        wb = openpyxl.load_workbook(excel_path)
        ws = wb.active
    else:
        wb = openpyxl.Workbook()
        ws = wb.active
        # 新規作成した場合はヘッダーを追加します。
        ws.append(["Purchase Date", "Store Name", "Description", "Amount"])

    # 抽出したデータをExcelシートに追加します。
    ws.append(
        [data["purchase_date"], data["store_name"], data["description"], data["amount"]]
    )
    # 変更を保存します。
    wb.save(excel_path)


# メインの処理を行う関数を定義します。
def main():
    # 指定されたディレクトリ内のPNGファイルをリストアップします。
    png_files = [f for f in os.listdir(image_dir) if f.endswith(".png")]

    # PNGファイルが見つからない場合はメッセージを表示して終了します。
    if not png_files:
        print("No PNG files found in the directory.")
        return

    # ランダムに選択された画像ファイルのパスを取得します。
    image_path = os.path.join(image_dir, random.choice(png_files))
    print(f"Selected image: {image_path}")

    # 画像をBase64エンコードします。
    base64_image = encode_image(image_path)
    # レシート情報を抽出します。
    receipt_data = extract_receipt_info(base64_image)

    # 抽出に成功した場合はExcelファイルにデータを追加し、画像を処理済みディレクトリに移動します。
    if receipt_data:
        print("Extracted Data:", receipt_data)
        update_excel_with_data(receipt_data, excel_path)
        move_image_to_done(image_path, done_dir)
    else:
        # 抽出に失敗した場合はメッセージを表示します。
        print("Failed to extract receipt data.")


# スクリプトを実行します。
if __name__ == "__main__":
    main()
