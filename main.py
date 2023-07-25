from fastapi import FastAPI, Query
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image, ImageDraw, ImageFont
from typing import List
import os
import urllib.request
import pandas as pd

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
    out_path = 'out.png' # 出力ファイル

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
        
        """for x, y in zip(x_list, y_list):
            # キャプションを取得する
            caption = item["商品名"].iloc[0]  # 商品名は同じ通し番号内で共通なので、先頭の要素を取得

            # キャプションの表示位置
            caption_x = x + 50
            caption_y = y + 110

            # キャプションのフォントを指定
            font = ImageFont.truetype(font_path, font_size)

            # キャプションを画像に描画
            draw.text((caption_x, caption_y), caption, fill=(0, 0, 0), font=font)  # fillで文字の色を指定
            
            base_with_caption.save(out_path)"""

        for x, y in zip(x_list, y_list):
            base.paste(logo_resized, (x-100, y), logo_resized)
            base.save(out_path)
        """im = Image.new("RGB", (60, 30), (255, 255, 255))
        draw = ImageDraw.Draw(im)
        item2 = item["商品名"]
        draw.text((0, 0), item2, 'black', font=font)
        base.paste(im, (x+50, y+110))"""
            
    
    return FileResponse(out_path, media_type="image/png")

@app.get("/image/white")
def whitemap():
    Image.open('map_master.png').convert('RGB').save('map_master.jpeg')
    path = "map_master.jpeg"
    return FileResponse(path, media_type="image/jpeg")
