import streamlit as st
from PIL import Image
import numpy as np
import random

st.set_page_config(page_title="나만의 스킨케어 코치", layout="centered")

# CSS 스타일 적용
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(to bottom, #e0f7fa, #ffffff);
        color: #333333;
    }
    
    .stTabs [role="tab"] {
        font-weight: bold;
        color: #0288d1;
    }
    .stTabs [role="tab"]:hover {
        color: #81d4fa;
    }
    
    div.stButton > button:first-child {
        background-color: #81d4fa;
        color: #ffffff;
        border-radius: 12px;
        padding: 0.5em 1.2em;
        font-weight: bold;
    }
    div.stButton > button:first-child:hover {
        background-color: #4fc3f7;
    }
    
    .stMarkdown {
        background-color: rgba(255,255,255,0.7);
        padding: 1em;
        border-radius: 15px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    </style>
""", unsafe_allow_html=True)

if "page" not in st.session_state:
    st.session_state.page = "input"

# 피부 상태 원인 & 팁
skin_tips = {
    "붉은기(홍조)": {"cause": "피부 장벽 약화, 외부 자극, 자외선 노출 가능", "tip": "진정 크림 사용, 자외선 차단 필수"},
    "각질": {"cause": "수분 부족, 턴오버 지연", "tip": "주 1회 이하 각질 제거, 보습 크림 충분히 사용"},
    "트러블(여드름)": {"cause": "피지 과다, 세균 증식, 스트레스", "tip": "진정 및 살균 제품 사용, 손으로 짜지 않기"},
    "민감함": {"cause": "피부 장벽 손상, 알러지 반응", "tip": "저자극, 무향 제품 사용"}
}

# 유튜버 채널명만 표시 (피부과 전문의 제거)
youtubers = {
    "건성": ["인씨(InC)", "유트루(Yoo True)"],
    "지성": ["회사원A"],
    "민감성": ["피부관리 전문가"],
    "복합성": ["피부관리 전문가"],
    "수부지": ["인씨(InC)", "유트루(Yoo True)"]
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

# AI 제품 추천 함수
def ai_product_recommendation(skin_status_list):
    products = []
    product_templates = [
        {"name": "진정 수딩 크림", "duration": "4주 사용 권장", "caution": "장기간 사용 시 피부 변화 관찰"},
        {"name": "보습 세럼", "duration": "6주 사용 권장", "caution": "과도한 사용 금지"},
        {"name": "각질 케어 토너", "duration": "주 1~2회 사용", "caution": "민감 피부는 사용 주의"},
        {"name": "저자극 클렌저", "duration": "매일 사용 가능", "caution": "눈가 접촉 주의"},
        {"name": "수분 마스크팩", "duration": "주 1~2회 사용", "caution": "과도한 사용 피하기"}
    ]
    for status in skin_status_list:
        products.append(random.choice(product_templates))
    seen = set()
    unique_products = []
    for p in products:
        if p['name'] not in seen:
            unique_products.append(p)
            seen.add(p['name'])
    return unique_products

# 입력 페이지
if st.session_state.page == "input":
    st.title("나만의 스킨케어 코치")

    skin_type = st.selectbox("피부 타입 선택", ["건성", "지성", "민감성", "복합성", "수부지"])

    st.write("### 피부 고민 알려주기")
    main_concern = st.radio("가장 고민되는 피부 상태 선택", ["붉은기(홍조)", "각질", "트러블(여드름)", "민감함", "없음"])

    other_concerns = st.text_input("기타 고민 입력", placeholder="예: 모공, 탄력 저하, 잡티 등")

    uploaded_image = st.file_uploader("피부 사진 업로드 (선택)", type=["png","jpg","jpeg"])
    if uploaded_image:
        image = Image.open(uploaded_image)
        st.image(image, caption="업로드한 사진", use_column_width=True)

        if st.button("AI 피부 분석"):
            ai_results, analysis_details = simple_skin_analysis(image)
            st.session_state.skin_status = ai_results
            st.session_state.skin_analysis_details = analysis_details
            st.session_state.skin_type = skin_type
            st.session_state.page = "result"
            st.success("AI 분석 완료! 아래에서 확인하세요.")

    if st.button("추천 제품 보기"):
        status_list = [main_concern] if main_concern != "없음" else []
        status_list += [c.strip() for c in other_concerns.split(",") if c.strip()]
        st.session_state.skin_type = skin_type
        st.session_state.skin_status = status_list
        st.session_state.skin_analysis_details = {}
        st.session_state.page = "result"

# 결과 페이지
elif st.session_state.page == "result":
    st.title("나만의 스킨케어 코치")
    tab1, tab2, tab3, tab4 = st.tabs(["추천 제품", "피부 분석", "유튜버 추천", "다시 입력"])

    with tab1:
        st.subheader("추천 제품")
        recommended_products = ai_product_recommendation(st.session_state.skin_status)
        if recommended_products:
            for product in recommended_products:
                st.write(f"**{product['name']}**")
                st.write(f"- 사용 기간: {product['duration']}")
                st.write(f"- 주의사항: {product['caution']}")
                st.write("---")

    with tab2:
        st.subheader("AI 피부 분석 결과")
        if st.session_state.skin_analysis_details:
            for symptom, detail in st.session_state.skin_analysis_details.items():
                st.markdown(f"### {symptom}")
                st.write(f"**상태:** {detail['state']}")
                st.write(f"**원인:** {detail['cause']}")
                st.write(f"**관리 팁:** {detail['tip']}")
                st.write("---")
        else:
            st.write("사진 AI 분석 없이 수동 입력만 했습니다.")

    with tab3:
        st.subheader("추천 유튜버 채널")
        yt_list = youtubers.get(st.session_state.skin_type, [])
        if yt_list:
            for name in yt_list:
                st.write(f"- {name}")

    with tab4:
        if st.button("다시 입력하기"):
            st.session_state.page = "input"
