import streamlit as st
from transformers import pipeline
from PIL import Image
import torch
import time

# 1. 모델 로드 함수 (캐싱 처리 및 GPU 설정)
@st.cache_resource
def load_model():
    # GPU 사용 가능 여부 확인 (있으면 0, 없으면 -1)
    device_id = 0 if torch.cuda.is_available() else -1
    return pipeline(task="image-classification",
                    model="google/vit-base-patch16-224",
                    device=device_id)


# 모델 불러오기
classifier = load_model()

st.title("🖼️ 이미지 분류 웹 애플리케이션")

# 2. 파일 업로더
ALLOWED_EXTENSIONS = ['jpg', 'jpeg', 'png', 'jfif', 'webp']
uploaded_file = st.file_uploader("이미지 파일 업로드(224x224 크기 권장)", type=ALLOWED_EXTENSIONS)

if uploaded_file is not None:
    # 파일을 이미지 객체로 변환
    image = Image.open(uploaded_file)
    width, height = image.size

    # A. 해상도 체크 기능
    if width != 224 or height != 224:
        st.warning(f"⚠️ 권장 해상도는 224x224입니다. (현재: {width}x{height})")
        # 모델 입력을 위해 강제로 리사이징
        input_image = image.resize((224, 224))
        st.info("모델 분석을 위해 이미지를 224x224로 리사이징했습니다.")
    else:
        st.success("✅ 적절한 해상도의 이미지입니다.")
        input_image = image

    # 화면에 이미지 표시
    st.image(input_image, caption=f"분석 대상 이미지 ({width}x{height})", width=300)

    # 2. 알림을 표시할 전용 공간 생성 (이미지 바로 아래)
    #alert_placeholder = st.empty()

    # B. 자동 모델 추론 기능
    with st.spinner('AI가 이미지를 분석하고 있습니다...'):
        # 모델 추론 수행
        predictions = classifier(input_image)

        # 업로드 완료 및 분석 완료 토스트 알림
        #st.toast("분석 완료!", icon="🚀")
        # 분석이 완료된 시점에 이미지 바로 아래에 메시지 표시
        #alert_placeholder.success("✅ 분석이 성공적으로 완료되었습니다!")

    # 결과 출력
    st.subheader("📊 분석 결과")
    for i, res in enumerate(predictions):
        label = res['label']
        score = res['score']
        st.write(f"**{i + 1}위: {label}** ({round(score * 100, 2)}%)")
        st.progress(score)  # 확률을 바 형태로 표시

    # 5. [선택 사항] 3초 후에 알림 메시지만 자동으로 지우기
    #time.sleep(3)
    #alert_placeholder.empty()