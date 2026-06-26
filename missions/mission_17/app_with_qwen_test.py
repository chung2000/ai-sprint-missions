import streamlit as st
from transformers import pipeline, Qwen2VLForConditionalGeneration, AutoProcessor
from qwen_vl_utils import process_vision_info
from PIL import Image
import torch
import time
import os
import sys

# 경로 설정
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from app_header import sidebar_menu, model_dict

# 1. 페이지 설정
st.set_page_config(page_title="Advanced Vision AI", layout="centered")

# 2. 사이드바 메뉴 (모델명에 'Qwen'이 포함된 경우를 대비)
# model_dict에 "Qwen2.5-VL-3B": "Qwen/Qwen2.5-VL-3B-Instruct" 등을 추가해두었다고 가정합니다.
selected_name, top_k_count = sidebar_menu()
model_id = model_dict[selected_name]


# 3. 모델 로드 로직 (Qwen과 일반 모델 분리)
@st.cache_resource
def load_ai_model(m_id):
    device = "cuda" if torch.cuda.is_available() else "cpu"

    # Qwen 계열 모델인 경우
    if "qwen" in m_id.lower():
        model = Qwen2VLForConditionalGeneration.from_pretrained(
            m_id, torch_dtype="auto", device_map="auto"
        )
        processor = AutoProcessor.from_pretrained(m_id)
        return {"model": model, "processor": processor, "type": "qwen"}

    # 일반 분류 모델인 경우
    else:
        pipe = pipeline("image-classification", model=m_id, device=0 if device == "cuda" else -1)
        return {"model": pipe, "type": "classification"}


with st.spinner(f"[{selected_name}] 모델을 준비 중입니다..."):
    engine = load_ai_model(model_id)

# 4. 메인 UI
st.title("🚀 하이브리드 비전 분석기")
uploaded_file = st.file_uploader("이미지를 업로드하세요", type=['jpg', 'jpeg', 'png', 'jfif', 'webp'])

if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")

    # 지시사항 반영: width='stretch'
    st.image(image, caption="분석 이미지", width='stretch')

    alert_placeholder = st.empty()

    # 5. 모델 타입별 추론 프로세스
    if engine["type"] == "classification":
        with st.spinner("이미지 분류 중..."):
            results = engine["model"](image)
            alert_placeholder.success("✅ 분류 완료!")

            st.subheader("📊 분류 결과")
            for res in results[:top_k_count]:
                col1, col2 = st.columns([1, 4])
                with col1: st.write(f"**{res['label']}**")
                with col2: st.progress(res['score']); st.write(f"{round(res['score'] * 100, 2)}%")

    elif engine["type"] == "qwen":
        # Qwen 모드에서는 사용자 질문을 받을 수 있습니다.
        user_prompt = st.text_input("AI에게 이미지에 대해 물어보세요", value="Describe this image in detail.")

        if st.button("질문하기"):
            with st.spinner("Qwen이 이미지를 해석 중..."):
                model = engine["model"]
                processor = engine["processor"]

                # Qwen 전용 입력 구성
                messages = [
                    {
                        "role": "user",
                        "content": [
                            {"type": "image", "image": image},
                            {"type": "text", "text": user_prompt},
                        ],
                    }
                ]

                # 텍스트 및 이미지 프로세싱
                text = processor.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
                image_inputs, _ = process_vision_info(messages)
                inputs = processor(
                    text=[text],
                    images=image_inputs,
                    padding=True,
                    return_tensors="pt"
                ).to(model.device)

                # 답변 생성
                generated_ids = model.generate(**inputs, max_new_tokens=256)
                generated_ids_trimmed = [
                    out_ids[len(in_ids):] for in_ids, out_ids in zip(inputs.input_ids, generated_ids)
                ]
                output_text = processor.batch_decode(
                    generated_ids_trimmed, skip_special_tokens=True, clean_up_tokenization_spaces=False
                )

                alert_placeholder.success("✅ 답변 생성 완료!")
                st.subheader("💬 AI 답변")
                st.info(output_text[0])

    # 알림 자동 삭제
    time.sleep(3)
    alert_placeholder.empty()