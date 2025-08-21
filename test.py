import streamlit as st
from PIL import Image

st.set_page_config(page_title="스킨케어 추천 앱", layout="centered")

if "page" not in st.session_state:
    st.session_state.page = "input"

# 제품 정보 예시
product_info = {
    "붉은기(홍조)": [
        {"name": "닥터지 레드 블레미쉬 수딩 크림",
         "link": "https://www.oliveyoung.co.kr/",
         "caution": "자극이 적은 진정 라인 위주로 사용"}
    ],
    "각질": [
        {"name": "라로슈포제 시카플라스트 밤 B5",
         "link": "https://www.oliveyoung.co.kr/",
         "caution": "각질 제거는 주 1회 이하로 제한"}
    ],
    "트러블(여드름)": [
        {"name": "아크네스 트러블 케어 크림",
         "link": "https://www.oliveyoung.co.kr/",
         "caution": "과도한 유분 제거 금지, 진정 라인 사용"}
    ],
    "민감함": [
        {"name": "센텔리안24 마데카 크림",
         "link": "https://www.oliveyoung.co.kr/",
         "caution": "향, 알코올 없는 저자극 제품 추천"}
    ]
}

# 피부 증상별 원인과 관리 팁
skin_tips = {
    "붉은기(홍조)": {"cause": "피부 장벽 약화, 알러지 반응, 자외선 노출", "tip": "저자극 진정 라인 사용, 자외선 차단 철저"},
    "각질": {"cause": "피부 수분 부족, 턴오버 지연", "tip": "각질 제거는 주 1회 이하, 수분 크림 충분히 사용"},
    "트러블(여드름)": {"cause": "피지 과다, 세균 증식", "tip": "과도한 세안 금지, 진정 & 살균 성분 사용"},
    "민감함": {"cause": "피부 장벽 손상, 알러지 반응", "tip": "저자극, 무향 제품 사용 및 충분한 보습"}
}

# 실제 유튜버 추천
youtubers = {
    "건성": [{"name": "인씨(InC)", "link": "https://www.youtube.com/@InC"},
             {"name": "유트루(Yoo True)", "link": "https://www.youtube.com/@YooTrue"}],
    "지성": [{"name": "회사원A", "link": "https://www.youtube.com/@officeworkera"}],
    "민감성": [{"name": "피부과전문의", "link": "https://www.youtube.com/@dermatologist"},
              {"name": "피부관리 전문가", "link": "https://www.youtube.com/@skincareexpert"}],
    "복합성": [{"name": "피부과전문의", "link": "https://www.youtube.com/@dermatologist"},
              {"name": "피부관리 전문가", "link": "https://www.youtube.com/@skincareexpert"}],
    "수부지": [{"name": "인씨(InC)", "link": "https://www.youtube.com/@InC"},
               {"name": "유트루(Yoo True)", "link": "https://www.youtube.com/@YooTrue"}]
}

# 입력 페이지
if st.session_state.page == "input":
    st.title("AI 스킨케어 추천")

    skin_type = st.selectbox("피부 타입을 선택하세요", ["건성", "지성", "민감성", "복합성", "수부지"])

    st.write("### 피부 고민을 알려주세요")
    main_concern = st.radio(
        "현재 가장 고민되는 피부 상태를 선택하세요",
        ["붉은기(홍조)", "각질", "트러블(여드름)", "민감함", "없음"]
    )

    other_concerns = st.text_input("기타 고민이 있다면 입력해주세요", placeholder="예: 모공, 탄력 저하, 잡티 등")

    # 사진 업로드 옵션
    uploaded_image = st.file_uploader("피부 사진을 업로드 하세요 (선택 사항)", type=["png", "jpg", "jpeg"])

    if uploaded_image:
        image = Image.open(uploaded_image)
        st.image(image, caption="업로드한 피부 사진", use_column_width=True)

    # AI 분석 버튼
    if st.button("AI 피부 분석"):
        st.info("AI 분석 기능은 추후 업데이트 예정입니다.")

    # 추천 버튼
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

        # 중복 제거
        for status in st.session_state.skin_status:
            for product in product_info.get(status, []):
                if product['name'] not in [p['name'] for p in recommended_products]:
                    recommended_products.append(product)

        if not recommended_products:
            st.write("추천 제품이 없습니다.")
        else:
            for product in recommended_products:
                st.write(f"**{product['name']}**")
                st.write(f"주의사항: {product['caution']}")
                st.markdown(f"[바로 사러가기]({product['link']})")
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
        for yt in youtubers.get(st.session_state.skin_type, []):
            st.markdown(f"- [{yt['name']}]({yt['link']})")

    with tab4:
        if st.button("다시 입력하기"):
            st.session_state.page = "input"
