import streamlit as st


model_dict = {
    "ViT (기본)": "google/vit-base-patch16-224",
    "ResNet-50 (고속)": "microsoft/resnet-50",
    "ConvNeXt (최신)": "facebook/convnext-tiny-224",
    "MobileNet (경량)": "google/mobilenet_v2_1.0_224"
    ##, "Qwen2-VL (경량)": "Qwen/Qwen2-VL-2B-Instruct
    ##, "Qwen2-VL (초경량)": "Qwen/Qwen2-VL-Chat"
}

def sidebar_menu():
    # 1. 사이드바 로고 설정 (URL 또는 로컬 경로)
    logo_url = "https://cdn-icons-png.flaticon.com/512/5968/5968350.png"  # 파이썬 로고 예시
    st.sidebar.image(logo_url, width=100)
    st.sidebar.title("🖼️ 이미지 분석기")
    st.sidebar.markdown("---")

    # 2. 메뉴 구성
    st.sidebar.subheader("설정")

    # model_option = st.sidebar.selectbox(
    #     "사용 모델 선택",
    #     ["Google ViT-Base",
    #      "resnet-50",
    #      "convnext-tiny-224",
    #     "Google mobilenet_v2_1.0_224"],
    # )

    # 사이드바 선택
    ##selected_model_name = st.sidebar.selectbox("모델 선택", list(model_dict.keys()))
    selected_name = st.sidebar.selectbox("모델 선택", list(model_dict.keys()))

    # 선택된 이름에 해당하는 ID를 찾아서 반환
    selected_id = model_dict[selected_name]
    print("selected_name : ", selected_name)

    st.sidebar.info("이 앱은 224x224 해상도에 최적화되어 있습니다.")

    return selected_name, selected_id