import streamlit as st
from transformers import pipeline
from PIL import Image, ImageDraw, ImageFont
import torch
import time
import os
import sys

# Streamlit Cloud 경로 문제 해결을 위한 설정
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from object_detection_header import sidebar_menu, model_dict

# 1. 페이지 설정
st.set_page_config(page_title="AI Multi-Vision Tool", layout="centered")

# 2. 사이드바 및 모델 정보 가져오기
selected_name, top_k_count = sidebar_menu()
model_id = model_dict[selected_name]


# 3. 모델 로드 (태스크 자동 판별)
@st.cache_resource
def load_vision_model(m_id):
    device_id = 0 if torch.cuda.is_available() else -1

    # 모델 이름에 따라 태스크 자동 결정
    if "detr" in m_id.lower():
        task = "object-detection"
    else:
        task = "image-classification"

    return pipeline(task=task, model=m_id, device=device_id), task


with st.spinner(f"[{selected_name}] 모델을 로드 중입니다..."):
    vision_model, current_task = load_vision_model(model_id)

# 4. 메인 화면 구성
st.title("🤖 통합 이미지 분석기")
st.write(f"현재 모드: **{current_task.upper()}**")

uploaded_file = st.file_uploader(
    "이미지를 업로드하세요",
    type=['jpg', 'jpeg', 'png', 'jfif', 'webp']
)

if uploaded_file is not None:
    # 이미지 로드 및 RGB 변환 (webp, jfif 등 호환성 확보)
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="업로드된 이미지", use_container_width=True)

    # [중요] 이미지 바로 아래 알림 전용 공간
    alert_placeholder = st.empty()

    # 5. 분석 실행
    with st.spinner('AI 분석 진행 중...'):
        results = vision_model(image)

    alert_placeholder.success("🚀 분석 완료!")

    # 6. 결과 시각화 (태스크별 분기)
    if current_task == "image-classification":
        st.subheader("📊 분류 결과 (Top-K)")
        for res in results[:top_k_count]:
            col1, col2 = st.columns([1, 4])
            with col1:
                st.write(f"**{res['label']}**")
            with col2:
                st.progress(res['score'])
                st.write(f"{round(res['score'] * 100, 2)}%")

    elif current_task == "object-detection":
        st.subheader("🎯 객체 탐지 결과")

        # 박스를 그리기 위한 이미지 복사
        draw_img = image.copy()
        draw = ImageDraw.Draw(draw_img)

        for res in results:
            box = res['box']
            label = res['label']
            score = res['score']

            # 박스 그리기
            draw.rectangle(
                [(box['xmin'], box['ymin']), (box['xmax'], box['ymax'])],
                outline="red", width=4
            )
            # 라벨 텍스트
            draw.text((box['xmin'], box['ymin'] - 10), f"{label} {round(score * 100, 1)}%", fill="red")

        # 결과 이미지 출력
        st.image(draw_img, caption="탐지된 사물 위치", use_container_width=True)

        # 탐지 목록 요약
        for res in results:
            st.write(f"📍 발견: **{res['label']}** (신뢰도: {round(res['score'] * 100, 2)}%)")

    # 3초 뒤 알림 지우기
    time.sleep(3)
    alert_placeholder.empty()

else:
    st.info("이미지를 업로드하면 분석이 시작됩니다.")