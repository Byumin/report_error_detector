import streamlit as st
from PIL import Image
import io

st.set_page_config(layout="wide")
st.title("📌 이미지 좌표 클릭 도구")

# 1. 이미지 업로드
uploaded_file = st.file_uploader("📂 이미지 파일을 업로드하세요 (JPG, PNG)", type=["jpg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="🖱️ 클릭할 위치를 기억해두세요. (아직 실시간 클릭은 구현되지 않음)", use_column_width=True)

    st.markdown("✅ 현재 이 앱은 이미지 crop 또는 좌표 저장까지 포함하는 **프로토타입 구조**입니다.")
    st.markdown("❗ Streamlit은 이미지 위 좌표 실시간 클릭을 기본적으로 지원하지 않으므로, **별도 좌표 입력 방식 또는 cropper로 대체**해야 합니다.")

    # 2. 수동 좌표 입력 UI (좌상단 → 우하단)
    st.subheader("🧭 수동 좌표 입력 (예: 그래프 영역)")
    x1 = st.number_input("좌측 상단 X", min_value=0)
    y1 = st.number_input("좌측 상단 Y", min_value=0)
    x2 = st.number_input("우측 하단 X", min_value=0)
    y2 = st.number_input("우측 하단 Y", min_value=0)

    if st.button("✂️ 이미지 Crop"):
        cropped = image.crop((x1, y1, x2, y2))
        st.image(cropped, caption="🎯 잘린 이미지", use_column_width=False)

        # 다운로드 버튼
        buf = io.BytesIO()
        cropped.save(buf, format="PNG")
        st.download_button("📥 잘린 이미지 다운로드", buf.getvalue(), file_name="cropped_graph.png", mime="image/png")