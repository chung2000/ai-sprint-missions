import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

# 1. Hugging Face 및 Supabase 클라이언트 임포트
from huggingface_hub import InferenceClient
from supabase import create_client, Client

load_dotenv()

app = FastAPI(title="Movie Review AI API (Vercel + DB)")

# --- 2. 환경 변수 및 클라이언트 설정 ---
HF_API_TOKEN = os.getenv("HF_API_TOKEN")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Hugging Face 클라이언트 (토큰 없으면 경고)
if not HF_API_TOKEN:
    print("⚠️ 경고: HF_API_TOKEN이 없습니다.")
hf_client = InferenceClient(api_key=HF_API_TOKEN)

# Supabase 클라이언트
if not SUPABASE_URL or not SUPABASE_KEY:
    print("⚠️ 경고: SUPABASE 정보가 없습니다.")
    supabase: Client = None
else:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# 모델 ID (로컬에서 검증된 모델 사용)
MODEL_ID = "daekeun-ml/koelectra-small-v3-nsmc"


# --- 3. 데이터 모델 ---
class ReviewCreate(BaseModel):
    movie_id: int
    movie_title: str  # DB 저장을 위해 영화 제목도 받도록 수정 권장 (또는 내부 조회)
    content: str


# --- 4. AI 분석 함수 ---
def analyze_sentiment(text: str):
    if not hf_client:
        return "UNKNOWN", 0.0

    try:
        # API 호출
        response = hf_client.text_classification(text=text, model=MODEL_ID)
        top_pred = max(response, key=lambda x: x['score'])

        # 라벨 파싱 (1/LABEL_1 = 긍정)
        label_str = str(top_pred['label']).upper()
        label = "POSITIVE" if "1" in label_str or "POS" in label_str else "NEGATIVE"
        return label, top_pred['score']

    except Exception as e:
        print(f"❌ AI 분석 실패: {e}")
        # API 실패 시 기본값 반환 (서버 다운 방지)
        return "ERROR", 0.0


# --- 5. API 엔드포인트 ---

@app.get("/")
def root():
    return {"message": "Movie Review API with Supabase is running!"}


# [리뷰 조회] - Supabase에서 가져오기
@app.get("/reviews/")
def get_all_reviews(movie_id: Optional[int] = None):
    if not supabase:
        return []

    try:
        query = supabase.table("reviews").select("*").order("created_at", desc=True)

        if movie_id:
            query = query.eq("movie_id", movie_id)

        response = query.execute()
        return response.data  # DB에서 가져온 리스트 반환

    except Exception as e:
        print(f"DB 조회 에러: {e}")
        raise HTTPException(status_code=500, detail="데이터베이스 조회 실패")


# [리뷰 생성] - AI 분석 후 Supabase에 저장
@app.post("/reviews/")
def create_review(review: ReviewCreate):
    # 1. AI 감성 분석
    label, score = analyze_sentiment(review.content)

    # 2. 저장할 데이터 준비
    new_review_data = {
        "movie_id": review.movie_id,
        "movie_title": review.movie_title,
        "content": review.content,
        "sentiment": label,
        "sentiment_score": round(score, 4),
        # created_at은 DB가 자동으로 생성하므로 생략 가능
    }

    # 3. Supabase 저장
    if supabase:
        try:
            data = supabase.table("reviews").insert(new_review_data).execute()
            # 저장된 데이터(ID 포함) 반환
            return data.data[0]
        except Exception as e:
            print(f"DB 저장 에러: {e}")
            raise HTTPException(status_code=500, detail="리뷰 저장 실패")
    else:
        return {"error": "DB 연결 안됨", "data": new_review_data}


# (영화 목록 API는 기존 JSON 파일을 읽거나, 추후 DB로 옮길 수 있습니다)
# 여기서는 간단히 기존 파일 유지 예시
@app.get("/movies/")
def get_movies():
    # 실제로는 DB에 movies 테이블도 만드는 것이 좋습니다.
    # 일단 빈 리스트 반환하거나 기존 로직 유지
    return []


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)