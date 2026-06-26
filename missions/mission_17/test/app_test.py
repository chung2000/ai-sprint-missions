import streamlit as st
from transformers import pipeline
from PIL import Image
import torch
import time
#from app_header import sidebar_menu
from app_header_test import sidebar_menu

# --- 1. 페이지 설정 및 사이드바 ---
st.set_page_config(page_title="ViT Image Classifier", layout="centered")
selected_model = sidebar_menu()


# --- 2. 모델 로드 (캐싱 및 GPU 설정) ---
@st.cache_resource
def load_model():
    # GPU 사용 가능 여부 확인
    device_id = 0 if torch.cuda.is_available() else -1
    # 정확한 task와 model 명시
    return pipeline(
        task="image-classification",
        model="google/vit-base-patch16-224",
        device=device_id
    )


with st.spinner("AI 모델을 불러오는 중입니다..."):
    classifier = load_model()

# --- 3. 메인 UI 및 파일 업로드 ---
st.title("Vision Transformer 분석기")
st.write(f"현재 활성화된 모델: **{selected_model}**")

ALLOWED_EXTENSIONS = ['jpg', 'jpeg', 'png', 'jfif', 'webp']

uploaded_file = st.file_uploader(
    "이미지 파일을 업로드하세요 (jpg, jpeg, png, jfif, webp 지원)",
    type=ALLOWED_EXTENSIONS
)

# --- 4. 로직 실행 (파일이 업로드되었을 때) ---
if uploaded_file is not None:
    # 이미지 열기
    image = Image.open(uploaded_file)
    width, height = image.size

    # 이미지 출력
    st.image(image, caption=f"원본 이미지 ({width}x{height})", use_container_width=True)

    # 이미지 바로 아래 알림 전용 공간
    alert_placeholder = st.empty()

    # 해상도 체크 및 리사이징
    if width != 224 or height != 224:
        alert_placeholder.warning(f"⚠️ 권장 해상도(224x224)가 아닙니다. 리사이징 후 분석을 시작합니다.")
        input_image = image.resize((224, 224))
        time.sleep(1)  # 사용자가 메시지를 읽을 시간을 줌
    else:
        alert_placeholder.info("✅ 최적의 해상도입니다. 분석을 시작합니다.")
        input_image = image

    # --- 5. 모델 추론 ---
    with st.spinner("이미지 분석 중..."):
        results = classifier(input_image)

    # 분석 완료 후 알림 업데이트
    alert_placeholder.success("🚀 분석이 완료되었습니다!")

    # --- 6. 결과 시각화 ---
    st.subheader("📊 예측 결과")

    # 결과를 표 형태로 정리하여 보여주기
    for i, res in enumerate(results):
        label = res['label']
        score = res['score']

        col1, col2 = st.columns([1, 4])
        with col1:
            st.write(f"**{label}**")
        with col2:
            st.progress(score)
            st.write(f"{round(score * 100, 2)}%")

    # 3초 후 상단 알림 지우기 (선택 사항)
    time.sleep(3)
    alert_placeholder.empty()

else:
    st.info("이미지 파일을 업로드하면 분석이 시작됩니다.")