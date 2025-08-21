import streamlit as st
from PIL import Image
import numpy as np
import random
import requests
from bs4 import BeautifulSoup
# import openai  # 실제 GPT API 이용 시

st.set_page_config(page_title="스킨케어 추천 앱", layout="centered")

if "page" not in st.session_state:
    st.session_state.page = "input"

# 기존 피부 팁, 유튜버 데이터
skin_tips = {
    "붉은기(홍조)": {"cause": "피부 장벽 약화, 알러지 반응, 자외선 노출", "tip": "저자극 진정 라인 사용, 자외선 차단 철저"},
    "각질": {"cause": "피부 수분 부족, 턴오버 지연", "tip": "각질 제거는 주 1회 이하, 수분 크림 충분히 사용"},
    "트러블(여드름)": {"cause": "피지 과다, 세균 증식", "tip": "과도한 세안 금지, 진정 & 살균 성분 사용"},
    "민감함": {"cause": "피부 장벽 손상, 알러지 반응", "tip": "저자극, 무향 제품 사용 및 충분한 보습"}
}

youtubers = {
    "건성": ["인씨(InC)", "유트루(Yoo True)"],
    "지성": ["회사원A"],
    "민감성": ["피부과전문의", "피부관리 전문가"],
    "복합성": ["피부과전문의", "피부관리 전문가"],
    "수부지": ["인씨(InC)", "유트루(Yoo True)"]
}

# 간단 AI 피부 분석
def simple_skin_analysis(image: Image.Image):
    img = image.resize((100,100))
    arr = np.array(img)
    red_mean = arr[:,:,0].mean()
    green_mean = arr[:,:,1].mean()
    blue_mean = arr[:,:,2].mean()
    results = []
    if red_mean > green_mean + 15:
        results.append("붉은기(홍조)")
    if random.random() > 0.7:
        results.append("각질")
    if random.random() > 0.8:
        results.append("트러블(여드름)")
    return results

# 올리브영 웹 크롤링 예시 함수
def fetch_oliveyoung_products(keyword):
    """
    키워드 기반 최신 제품 리스트 크롤링 (예시)
    """
    url = f"https://www.oliveyoung.co.kr/store/search/searchMain.do?query={keyword}"
    headers = {"User-Agent":"Mozilla/5.0"}
    resp = requests.get(url, headers=headers)
    products = []
    if resp.status_code == 200:
        soup = BeautifulSoup(resp.text, "html.parser")
        items = soup.select(".prd_name")[:5]  # 최대 5개
        for item in items:
            name = item.get_text(strip=True)
            products.append({"name": name, "caution": "사용 시 주의사항 확인"})
    return products if products else [{"name": f"{keyword} 추천 제품 없음", "caution": ""}]

# 입력 페이지
if st.session_state.page == "input":
    st.title("AI 스킨케어 추천")

    skin_type = st.selectbox("피부 타입을 선택하세요", ["건성", "지성", "민감성", "복합성", "수부지"])

    st.write("### 피부 고민을 알려주세요")
    main_concern = st.radio(
        "가장 고민되는 피부 상태를 선택하세요",
        ["붉은기(홍조)", "각질", "트러블(여드름)", "민감함", "없음"]
    )

    other_concerns = st.text_input("기타 고민이 있다면 입력", placeholder="예: 모공, 탄력 저하, 잡티 등")

    uploaded_image = st.file_uploader("피부 사진 업로드 (선택)", type=["png","jpg","jpeg"])
    if uploaded_image:
        image = Image.open(uploaded_image)
        st.image(image, caption="업로드한 사진", use_column_width=True)

        if st.button("AI 피부 분석"):
            ai_results = simple_skin_analysis(image)
            st.session_state.skin_status = ai_results
            st.session_state.skin_type = skin_type
            st.session_state.page = "result"
            st.success(f"AI 분석 완료: {', '.join(ai_results)}")

    if st.button("추천 제품 보기"):
        status_list = [main_concern] if main_concern != "없음" else []
        status_list += [c.strip() for c in other_concerns.split(",") if c.strip()]
        st.session_state.skin_type = skin_type
        st.session_state.skin_status = status_list
        st.session_state.page = "result"

# 결과 페이지
elif st.session_state.page == "result":
    st.title("맞춤 추천 결과")

    tab1, tab2, tab3, tab4 = st.tabs(["추천 제품", "피부 원인 & 팁", "유튜버 추천", "다시 입력"])

    with tab1:
        st.subheader("추천 제품")
        recommended_products = []
        for status in st.session_state.skin_status:
            recommended_products += fetch_oliveyoung_products(status)

        # 중복 제거
        seen = set()
        unique_products = []
        for p in recommended_products:
            if p['name'] not in seen:
                unique_products.append(p)
                seen.add(p['name'])

        if not unique_products:
            st.write("추천 제품이 없습니다.")
        else:
            for product in unique_products:
                st.write(f"**{product['name']}**")
                st.write(f"주의사항: {product['caution']}")
                st.write("---")

    with tab2:
        st.subheader("피부 증상 원인 & 관리 팁")
        for symptom, data in skin_tips.items():
            if symptom in st.session_state.skin_status:
                st.markdown(f"### {symptom}")
                st.write(f"**원인:** {data['cause']}")
                st.write(f"**관리 팁:** {data['tip']}")
                st.write("---")

    with tab3:
        st.subheader("추천 유튜버 채널")
        for name in youtubers.get(st.session_state.skin_type, []):
            st.write(f"- {name}")

    with tab4:
        if st.button("다시 입력하기"):
            st.session_state.page = "input"
