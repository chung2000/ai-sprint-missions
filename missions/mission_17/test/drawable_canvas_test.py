import streamlit as st
from streamlit_drawable_canvas import st_canvas
import numpy as np
from PIL import Image

st.title("숫자 그리기 판")

# 1. 캔버스 설정
canvas_result = st_canvas(
    fill_color="rgba(255, 165, 0, 0.3)",  # 채우기 색상
    stroke_width=10,  # 펜 굵기
    stroke_color="#000000",  # 펜 색상 (검정)
    background_color="#FFFFFF",  # 배경 색상 (흰색)
    height=200,  # 높이
    width=200,  # 너비
    drawing_mode="freedraw",  # 자유 그리기 모드
    key="canvas",
)

# 2. 결과 처리
if canvas_result.image_data is not None:
    # 캔버스 데이터를 numpy 배열로 변환 (RGBA 형태)
    img = canvas_result.image_data

    # AI 모델에 넣기 위해 흑백 변환 또는 크기 조정이 필요할 수 있습니다.
    st.image(img, caption="그려진 숫자 확인")

    # (선택) 모델 예측 버튼
    if st.button("숫자 맞추기"):
        # 여기에 모델 추론 로직 추가
        st.write("모델이 숫자를 분석 중입니다...")