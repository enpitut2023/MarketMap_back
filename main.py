from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image

app = FastAPI()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/image/pinned")
def map():
    Image.open('map_master.png').convert('RGB').save('map_master.jpeg')
    base_path = 'map_master.jpeg' # ベース画像
    logo_path = 'pin2.png' # 重ねる透過画像
    out_path = 'out.png' # 出力ファイル

    base = Image.open(base_path)
    logo = Image.open(logo_path)

    #base_w, base_h = base.size =>1920, 1292
    logo_w, logo_h  = logo.size

    scale = 0.3
    logo_resized = logo.resize((int(logo_w * scale), int(logo_h * scale)))

    data = [["醤油", "調味料", 300, 520],
            ["牛肉", "肉", 1500, 1000],
            ["マヨネーズ", "調味料", 100, 300], #商品名,カテゴリ名,x座標,y座標
            ["鮭", "魚", 700, 700]]

    n = 4 #表示件数

    for i in range(n):
        x = data[i][2]
        y = data[i][3]
        base.paste(logo_resized, (x, y), logo_resized)

    base.save(out_path)
    
    return FileResponse(out_path, media_type="image/png")

@app.get("/image/white")
def whitemap():
    Image.open('map_master.png').convert('RGB').save('map_master.jpeg')
    path = "map_master.jpeg"
    return FileResponse(path, media_type="image/jpeg")