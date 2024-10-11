from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from PIL import Image
import torch
import io

# FastAPI 인스턴스 생성
app = FastAPI()

# YOLO 모델 로드
model = torch.hub.load('ultralytics/yolov5', 'yolov5x', pretrained=True)

# 이미지 파일을 모델에 입력하여 예측하는 함수
@app.post("/predict/")
async def predict(file: UploadFile = File(...)):
    # 업로드된 이미지를 PIL로 변환
    image_data = await file.read()
    img = Image.open(io.BytesIO(image_data))

    # YOLO 모델에 이미지를 전달하고 예측 수행
    results = model(img)

    # 결과를 JSON으로 변환
    predictions = results.pandas().xyxy[0].to_dict(orient="records")

    return JSONResponse(content={"predictions": predictions})
