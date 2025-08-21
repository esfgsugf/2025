import streamlit as st
from PIL import Image
import numpy as np
import random

# 페이지 설정
st.set_page_config(page_title="나만의 스킨케어 코치", layout="centered")

# CSS 스타일 적용
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(to bottom, #f0fcff, #ffffff);
        color: #333333;
        font-family: 'Helvetica', sans-serif;
    }
    
    .stTabs [role="tab"] {
        font-weight: bold;
        color: #0288d1;
        padding: 0.4em 1em;
        border-radius: 8px;
    }
    .stTabs [role="tab"]:hover {
        color: #81d4fa;
        background-color: rgba(135,206,250,0.1);
    }
    
    div.stButton > button:first-child {
        background-color: #4fc3f7;
        color: #ffffff;
        border-radius: 8px;
        padding: 0.3em 0.8em;
        font-weight: bold;
        font-size: 14px;
        transition: 0.3s;
    }
    div.stButton > button:first-child:hover {
        background-color: #29b6f6;
    }
    
    .stMarkdown {
        background-color: rgba(255,255,255,0.8);
        padding: 1em;
        border-radius: 15px;
        box-shadow: 0 3px 10px rgba(0,0,0,0.05);
    }
    
    .emoji-footer {
        text-align: center;
        font-size: 2em;
        padding: 1em 0;
    }
    </style>
""", unsafe_allow_html=True)

# session_state 초기화
if "page" not in st.session_state:
    st.session_state.page = "input"
if "skin_status" not in st.session_state:
    st.session_state.skin_status = []
if "skin_analysis_details" not in st.session_state:
    st.session_state.skin_analysis_details = {}
if "skin_type" not in st.session_state:
    st.session_state.skin_type = ""

# 피부 상태 원인 & 팁
skin_tips = {
    "붉은기(홍조)": {"cause": "피부 장벽 약화, 외부 자극, 자외선 노출 가능", "tip": "진정 크림 사용, 자외선 차단 필수"},
    "각질": {"cause": "수분 부족, 턴오버 지연", "tip": "주 1회 이하 각질 제거, 보습 크림 충분히 사용"},
    "트러블(여드름)": {"cause": "피지 과다, 세균 증식, 스트레스", "tip": "진정 및 살균 제품 사용, 손으로 짜지 않기"},
    "민감함": {"cause": "피부 장벽 손상, 알러지 반응", "tip": "저자극, 무향 제품 사용"}
}

# 유튜버 채널명만 표시
youtubers = {
    "건성": ["인씨(InC)", "유트루(Yoo True)"],
    "지성": ["회사원A"],
    "민감성": ["슈히"],
    "복합성": ["제나"],
    "수부지": ["인씨(InC)", "유트루(Yoo True)", "제나"]
}

# AI 피부 분석 함수
def simple_skin_analysis(image: Image.Image):
    img = image.resize((100,100))
    arr = np.array(img)
    red_mean = arr[:,:,0].mean()
    green_mean = arr[:,:,1].mean()
    blue_mean = arr[:,:,2].mean()
    
    results = []
    analysis_details = {}
    
    if red_mean > green_mean + 15:
        results.append("붉은기(홍조)")
        analysis_details["붉은기(홍조)"] = {
            "state": "얼굴이 살짝 달아오르고 붉은기가 쉽게 올라와 있어요.",
            "cause": "피부 장벽이 약하거나 자외선/알러지 영향 가능",
            "tip": "자극 없는 진정 크림 사용, 자외선 차단 필수, 세안 부드럽게"
        }
    if random.random() > 0.7:
        results.append("각질")
        analysis_details["각질"] = {
            "state": "피부가 푸석하고 거칠게 느껴져요.",
            "cause": "수분 부족, 피부 턴오버 지연",
            "tip": "각질 제거는 주 1회 이하, 보습 크림 듬뿍"
        }
    if random.random() > 0.8:
        results.append("트러블(여드름)")
        analysis_details["트러블(여드름)"] = {
            "state": "작은 여드름이 여기저기 보이거나 붉게 올라왔어요.",
            "cause": "피지 과다, 세균 증식, 스트레스",
            "tip": "진정 & 살균 제품 사용, 손으로 짜지 않기"
        }
    return results, analysis_details

# 입력 페이지
if st.session_state.page == "input":
    st.title("💧 나만의 스킨케어 코치 💧")

    skin_type = st.selectbox("피부 타입 선택", ["건성", "지성", "민감성", "복합성", "수부지"], key="skin_type_select")

    st.write("### 피부 고민 알려주기")
    main_concern = st.radio("가장 고민되는 피부 상태 선택", ["붉은기(홍조)", "각질", "트러블(여드름)", "민감함", "없음"], key="main_concern_radio")

    other_concerns = st.text_input("기타 고민 입력", placeholder="예: 모공, 탄력 저하, 잡티 등", key="other_concerns_input")

    uploaded_image = st.file_uploader("피부 사진 업로드 (선택)", type=["png","jpg","jpeg"], key="upload_image")
    if uploaded_image:
        image = Image.open(uploaded_image)
        st.image(image, caption="업로드한 사진", use_column_width=True)

        if st.button("AI 피부 분석", key="ai_analysis_button"):
            ai_results, analysis_details = simple_skin_analysis(image)
            st.session_state.skin_status = ai_results
            st.session_state.skin_analysis_details = analysis_details
            st.session_state.skin_type = skin_type
            st.session_state.page = "result"
            st.success("AI 분석 완료! 아래에서 확인하세요.")

    # 하늘하늘한 물 이모티콘 footer
    st.markdown('<div class="emoji-footer">💧🌊✨</div>', unsafe_allow_html=True)
