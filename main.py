from fastapi import FastAPI, Query
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image, ImageDraw, ImageFont
from typing import List
import os
import urllib.request
import pandas as pd
import uuid
import time

os.makedirs(".fonts", exist_ok = True)

print("ダウンロード中です")

urllib.request.urlretrieve("https://github.com/evosystem-jp/heroku-buildpack-cjk-font/raw/master/fonts/wqy-microhei.ttc", ".fonts/wqy-microhei.ttc")

print("ダウンロードが完了しました。")

app = FastAPI()

origins = [
    "http://localhost:3000",
    "https://market-map.netlify.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/image/pinned")
def map(param: List[int]):
    Image.open('map_master.png').convert('RGB').save('map_master.jpeg')
    base_path = 'map_master.jpeg' # ベース画像
    logo_path = 'pin2.png' # 重ねる透過画像
    unique_id = str(uuid.uuid1())
    image_dir = "images/"
    if not os.path.exists(image_dir):
        os.makedirs(image_dir)
    out_path = os.path.join(image_dir, f"{unique_id}.png")
    print(out_path)
    # out_path = 'out.png' # 出力ファイル

    image_folder = "images"
    three_minutes_ago = time.time() - 3 * 60
    for filename in os.listdir(image_folder):
        file_path = os.path.join(image_folder, filename)
        if os.path.isfile(file_path):
            # 画像のタイムスタンプを取得
            file_timestamp = os.path.getctime(file_path)

            # 3分前よりも古い画像を削除
            if file_timestamp < three_minutes_ago:
                os.remove(file_path)
                print(f"Deleted: {file_path}")



    base = Image.open(base_path)
    logo = Image.open(logo_path)

    #キャプション用の設定
    with open(".fonts/wqy-microhei.ttc", "rb") as f:
        font = ImageFont.truetype(f, 30)

    #base_w, base_h = base.size =>1920, 1292
    logo_w, logo_h  = logo.size

    scale = 0.2 # 0.3だとはみ出る　，座標がちょうど良くない
    logo_resized = logo.resize((int(logo_w * scale), int(logo_h * scale)))
    

    data = pd.read_csv("./data.csv")
    # 任意のフォントファイルのパスとフォントサイズを指定
    font_path = "path/to/font.ttf"
    font_size = 14

    # ベース画像を元にしたコピーを作成
    base_with_caption = base.copy()
    draw = ImageDraw.Draw(base_with_caption)

    for i in param:
        item = data[data['通し番号'] == i]
        x_list = item["x座標"].tolist()  # x座標をリストに変換
        y_list = item["y座標"].tolist()  # y座標をリストに変換
        caption_list = item["商品名"].tolist() #商品名をリストに変換
    
        for x, y, caption in zip(x_list, y_list, caption_list):
            base.paste(logo_resized, (x, y-80), logo_resized)
            
            im = Image.new("RGB", (60, 30), (255, 255, 255))
            draw = ImageDraw.Draw(im)
            draw.text((0, 0), caption, 'black', font=font)
            base.paste(im, (x, y+25))
            base.save(out_path)
<<<<<<< Updated upstream
        """im = Image.new("RGB", (60, 30), (255, 255, 255))
        draw = ImageDraw.Draw(im)
        item2 = item["商品名"]
        draw.text((0, 0), item2, 'black', font=font)
        base.paste(im, (x+50, y+110))"""
            
    # with open(out_path, "wb") as f:
    #     f.write(b"Generated Image Data")

    response =  FileResponse(out_path, media_type = "image/png")
    return response
=======
    
    return FileResponse(out_path, media_type="image/png")
>>>>>>> Stashed changes

@app.get("/image/white")
def whitemap():
    Image.open('map_master.png').convert('RGB').save('map_master.jpeg')
    path = "map_master.jpeg"
    return FileResponse(path, media_type="image/jpeg")
