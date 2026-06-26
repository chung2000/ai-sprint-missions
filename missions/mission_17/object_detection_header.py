import streamlit as st

# 사용할 모델 리스트 정의
model_dict = {
    "ViT (기본-분류)": "google/vit-base-patch16-224",
    "ResNet-50 (고속-분류)": "microsoft/resnet-50",
    "DETR (객체탐지)": "facebook/detr-resnet-50"
}


def sidebar_menu():
    st.sidebar.title("🔍 AI Vision 설정")
    st.sidebar.markdown("---")

    # 모델 선택
    selected_name = st.sidebar.selectbox("사용할 모델을 선택하세요", list(model_dict.keys()))

    # 결과 개수 조절 (분류 모드에서 사용)
    top_k = st.sidebar.slider("표시할 결과 개수", 1, 5, 3)

    st.sidebar.markdown("---")
    st.sidebar.info("지원 확장자: jpg, jpeg, png, jfif, webp")

    return selected_name, top_k