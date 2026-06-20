import json
import os
from pathlib import Path

from fastapi import FastAPI, UploadFile, File
from google import genai
from google.genai import types

app = FastAPI()

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise RuntimeError("Environment variable GEMINI_API_KEY is required")

client = genai.Client(
    api_key=api_key
)

PROMPT = """
전단지 이미지를 분석해서 상품 목록을 JSON 배열로 반환해라.

형식:

[
  {
    "name": "상품명",
    "price": 1000,
    "unit": "개"
  }
]

JSON 외의 다른 텍스트는 출력하지 마라.
"""


@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    image_bytes = await file.read()

    # response = client.models.generate_content(
    #     model="gemini-2.5-flash",
    #     contents=[
    #         PROMPT,
    #         {
    #             "mime_type": file.content_type,
    #             "data": image_bytes
    #         }
    #     ]
    # )
    
    image_part = types.Part.from_bytes(
        data=image_bytes,
        mime_type="image/jpeg"
    )

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[
            "전단지의 상품과 가격을 JSON으로 추출해줘",
            image_part
        ]
    )

    text = response.text.strip()

    try:        
        products = json.loads(text)
        
        json_file = f"{Path(file.filename).stem}.json"
        with open(json_file, "w", encoding="utf-8") as f:
            json.dump(
                products,
                f,
                ensure_ascii=False,
                indent=2
            )        
        
    except Exception:
        return {
            "error": "JSON parsing failed",
            "raw_response": text
        }

    return {
        "products": products
    }