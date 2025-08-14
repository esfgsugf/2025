import streamlit as st
import random
import hashlib
import urllib.parse
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
# 🎨 글로벌 스타일 (CSS)
#  - 알록달록 그라데이션 배경 + 카드 스타일 + 이모지
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
          font-size: 46px; text-align:center; font-weight: 900; color:#ff4d94;
          text-shadow: 0 2px 10px rgba(255,77,148,.25); letter-spacing:.5px;
        }
        .sub-txt { text-align:center; font-size:15px; opacity:.9; }
        .card {
          padding: 18px; border-radius: 22px; text-align: center; margin: 10px 0;
          box-shadow: 0 10px 25px rgba(0,0,0,.12); border: 2px solid rgba(255,255,255,.6);
        }
        .name { font-size: 22px; font-weight: 800; margin-top: 10px; }
        .desc { font-size: 15px; opacity:.95; }
        .tag { display:inline-block; padding:6px 10px; border-radius:12px; background:rgba(255,255,255,.75); margin:4px; font-size:13px; }
        .footer { text-align:center; font-size:13px; opacity:.75; margin-top: 18px; }
        .search-btn a{ text-decoration:none; font-weight:700; }
        </style>
        """
    ),
    unsafe_allow_html=True,
)

# =============================
# 🧠 MBTI → 연예인 후보 (16 타입, 3인씩)
#  - 실제 MBTI와 정확히 일치한다고 단정하지 않으며, "분위기가 어울리는" 예시입니다.
#  - 이미지 핫링크 실패 문제를 피하기 위해, 기본은 파스텔 SVG 아바타를 사용합니다.
#  - 각 이름을 클릭/버튼으로 웹 검색해 실제 사진을 확인할 수 있습니다.
# =============================
MBTI_CELEBS = {
    "ISTJ": ["전지현", "공유", "한석규"],
    "ISFJ": ["수지", "도경수", "김유정"],
    "INFJ": ["아이유", "유아인", "이정재"],
    "INTJ": ["윤여정", "송강호", "이병헌"],
    "ISTP": ["정해인", "김우빈", "최민식"],
    "ISFP": ["김태리", "박보검", "한지민"],
    "INFP": ["박은빈", "임시완", "수현(스카라렛 요한슨)"],
    "INTP": ["남주혁", "류준열", "유재석"],
    "ESTP": ["김종국", "제니", "민호(샤이니)"],
    "ESFP": ["유나(ITZY)", "조이(레드벨벳)", "문빈"],
    "ENFP": ["박보영", "차은우", "피오"],
    "ENTP": ["양세형", "은지원", "유연석"],
    "ESTJ": ["김희애", "진(방탄소년단)", "김연아"],
    "ESFJ": ["이효리", "강다니엘", "박
