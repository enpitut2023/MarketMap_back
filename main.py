from fastapi import FastAPI, Query
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image, ImageDraw, ImageFont
from typing import List
app = FastAPI()

origins = [
    "http://localhost:3000",
    "https://main--marvelous-frangipane-e310c5.netlify.app",
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
    font = ImageFont.truetype('wqy-microhei.ttc', 30)

    #base_w, base_h = base.size =>1920, 1292
    logo_w, logo_h  = logo.size

    scale = 0.2 # 0.3だとはみ出る　，座標がちょうど良くない
    logo_resized = logo.resize((int(logo_w * scale), int(logo_h * scale)))
    

    data = [[1, "調味料", "醤油", 530, 276],
            [2, "調味料", "マヨネーズ", 900, 87],
            [3, "肉", "牛肉", 1235, 10], #通し番号,カテゴリ名,商品名,x座標,y座標
            [4, "魚", "鮭", 826, 24],
            ]

    for i in param:
        x = data[i][3] -20
        y = data[i][4] +5
        base.paste(logo_resized, (x, y), logo_resized)
        im = Image.new("RGB", (60, 30), (255, 255, 255))
        draw = ImageDraw.Draw(im)
        draw.text((0, 0), data[i][2], 'black', font=font)
        base.paste(im, (x+50, y+110))

    base.save(out_path)
    
    return FileResponse(out_path, media_type="image/png")

@app.get("/image/white")
def whitemap():
    Image.open('map_master.png').convert('RGB').save('map_master.jpeg')
    path = "map_master.jpeg"
    return FileResponse(path, media_type="image/jpeg")
