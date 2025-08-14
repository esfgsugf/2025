import streamlit as st
from textwrap import dedent

# =============================
# 🧩 페이지 기본 설정
# =============================
st.set_page_config(
    page_title="MBTI → 연예인 추천",
    page_icon="🌈",
    layout="centered"
)

# =============================
# 🎨 스타일 (CSS)
# =============================
st.markdown(
    dedent(
        """
        <style>
        @keyframes gradientMove {
          0% { background-position: 0% 50%; }
          50% { background-position: 100% 50%; }
          100% { background-position: 0% 50%; }
        }
        .stApp {
          background: linear-gradient(135deg, #FFDEE9, #B5FFFC, #FFE7A1, #D4FFEA);
          background-size: 400% 400%;
          animation: gradientMove 18s ease infinite;
        }
        .mega-title {
          font-size: 44px;
          text-align: center;
          font-weight: 900;
          color: #ff4d94;
          text-shadow: 0 2px 10px rgba(255,77,148,.25);
          letter-spacing: .5px;
        }
        .celebs-card {
          padding: 22px;
          border-radius: 22px;
          text-align: center;
          box-shadow: 0 10px 25px rgba(0,0,0,.12);
          border: 2px solid rgba(255,255,255,.6);
          background-color: rgba(255, 255, 255, 0.5);
          margin: 15px 0;
        }
        .celebs-name {
          font-size: 22px;
          font-weight: 700;
          margin-top: 8px;
        }
        .footer { text-align:center; font-size:13px; opacity:.75; margin-top: 30px; }
        </style>
        """
    ),
    unsafe_allow_html=True,
)

# =============================
# 🧠 MBTI → 연예인 매핑
# =========================
