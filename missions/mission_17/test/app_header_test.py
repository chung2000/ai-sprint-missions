import streamlit as st


def sidebar_menu():
    # 1. 사이드바 로고 설정 (URL 또는 로컬 경로)
    logo_url = "https://cdn-icons-png.flaticon.com/512/5968/5968350.png"  # 파이썬 로고 예시
    st.sidebar.image(logo_url, width=100)
    st.sidebar.title("🖼️ 이미지 분석기")
    st.sidebar.markdown("---")

    # 2. 메뉴 구성
    st.sidebar.subheader("설정")
    model_option = st.sidebar.selectbox(
        "사용 모델 선택",
        ["Google ViT-Base"]
    )

    st.sidebar.info("이 앱은 224x224 해상도에 최적화되어 있습니다.")

    return model_option