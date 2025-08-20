
import streamlit as st
from PIL import Image, ImageDraw, ImageFont
from streamlit_drawable_canvas import st_canvas
import requests

st.set_page_config(page_title="덕질 다이어리", page_icon="✨", layout="wide")

# ------------------------
# 메인 화면
# ------------------------
st.title("✨ 덕질 다이어리 앱 ✨")
st.write("포토카드를 꾸미고, 아이돌/배우 출연 작품을 확인해보세요!")

menu = st.sidebar.radio("메뉴 선택", ["홈", "포토카드 꾸미기", "아이돌/배우 정보"])

# ------------------------
# 홈
# ------------------------
if menu == "홈":
    st.subheader("환영합니다 💖")
    st.write("👉 왼쪽 메뉴에서 원하는 기능을 선택해주세요!")

# ------------------------
# 포토카드 꾸미기
# ------------------------
elif menu == "포토카드 꾸미기":
    st.subheader("📸 포토카드 꾸미기")

    uploaded_file = st.file_uploader("최애 사진을 업로드하세요", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        img = Image.open(uploaded_file)

        # 꾸미기 캔버스
        st.write("사진 위에 스티커나 글씨를 추가해보세요!")
        canvas_result = st_canvas(
            fill_color="rgba(255, 255, 255, 0.3)",
            stroke_width=3,
            stroke_color="#000000",
            background_image=img,
            update_streamlit=True,
            height=400,
            width=300,
            drawing_mode="freedraw",
            key="canvas",
        )

        if st.button("포토카드 저장하기"):
            st.success("포토카드가 저장되었습니다! (추후 저장 기능 연결 가능)")

# ------------------------
# 아이돌/배우 정보
# ------------------------
elif menu == "아이돌/배우 정보":
    st.subheader("🎬 아이돌/배우 정보 검색")

    name = st.text_input("이름을 입력하세요 (예: 아이유, 박보검)")
    if st.button("검색"):
        st.write(f"🔎 '{name}' 관련 드라마/예능/영화 정보를 불러오는 중...")

        # 여기서는 예시 출력만
        # 실제로는 TMDB API, 위키피디아, 멜론 API 등을 연결
        sample_data = {
            "아이유": ["드라마: 호텔 델루나", "예능: 효리네 민박", "앨범: Love poem"],
            "박보검": ["드라마: 구르미 그린 달빛", "영화: 서복", "예능: 1박2일"]
        }

        if name in sample_data:
            for info in sample_data[name]:
                st.write("✅", info)
        else:
            st.warning("아직 데이터가 없습니다. API 연결 필요!")
