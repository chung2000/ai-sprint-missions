import os
from huggingface_hub import InferenceClient
from dotenv import load_dotenv

load_dotenv()
token = os.getenv("HF_API_TOKEN").strip()
client = InferenceClient(api_key=token)

try:
    # 가장 가벼운 모델로 테스트
    result = client.text_classification("I love this movie!", model="distilbert-base-uncased-finetuned-sst-2-english")
    print("🚀 인증 성공! 결과:", result)
except Exception as e:
    print("❌ 인증 실패 상세 에러:", e)