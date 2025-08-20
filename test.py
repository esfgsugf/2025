import streamlit as st
from PIL import Image

st.set_page_config(page_title="맞춤형 스킨케어 추천", layout="centered")
st.title("📸 맞춤형 스킨케어 추천 앱")

# --- 세션 상태 초기화 ---
if "page" not in st.session_state:
    st.session_state.page = "input"
if "skin_status" not in st.session_state:
    st.session_state.skin_status = ""
if "image" not in st.session_state:
    st.session_state.image = None
if "additional_info" not in st.session_state:
    st.session_state.additional_info = ""
if "skin_type" not in st.session_state:
    st.session_state.skin_type = ""

# --- 제품 데이터 ---
product_info = {
    "라로슈포제 시카 토너": {
        "link": "https://www.oliveyoung.co.kr/product?pid=example1",
        "usage": "아침/저녁 사용, 2~3개월 사용 가능",
        "caution": "민감 피부는 패치 테스트 권장"
    },
