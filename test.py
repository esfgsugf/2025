import streamlit as st

# --------------------
# 초기 세션 상태 설정
# --------------------
if "page" not in st.session_state:
    st.session_state.page = "input"
if "skin_type" not in st.session_state:
    st.session_state.skin_type = ""
if "skin_status" not in st.session_state:
    st.session_state.skin_status = ""
if "additional_info" not in st.session_state:
    st.session_state.additional_info = ""

# --------------------
# 제품 데이터 예시
# --------------------
product_info = {
    "건성": [
        {"name": "라운드랩 1025 독도 토너",
         "link": "https://www.oliveyoung.co.kr/store/goods/getGoodsDetail.do?goodsNo=A000000123",
         "duration": "2~3개월",
         "caution": "장기간 사용 시 피부에 맞는지 체크 필요"},
        {"name": "닥터지 레드 블레미쉬 크림",
         "link": "https://www.oliveyoung.co.kr/store/goods/getGoodsDetail.do?goodsNo=A000000456",
         "duration": "2개월",
         "caution": "민감 부위에는 소량 사용"}
    ],
    "지성": [
        {"name": "이니스프리 그린티 씨드 세럼",
         "link": "https://www.oliveyoung.co.kr/store/goods/getGoodsDetail.do?goodsNo=A000000789",
         "duration": "3개월",
         "caution": "지성 피부에 맞는 수분감"}
    ]
}

# --------------------
# 피부 증상별 원인과 관리 팁
# --------------------
skin_tips = {
    "붉은기": {
        "cause": "피부 장벽 약화, 알러지 반응, 자외선 노출",
        "tip": "저자극 진정 라인 사용, 자외선 차단 철저"
    },
    "각질": {
        "cause": "피부 수분 부족, 턴오버 지연",
        "tip": "각질 제거는 주 1회 이하, 수분 크림 충분히 사용"
    }
}

# --------------------
# 피부 타입별 유튜버 추천
# --------------------
youtubers = {
    "건성": [
        {"name": "Arang", "link": "https://www.youtube.com/@arang"},
        {"name": "Hoonion", "link": "https://www.youtube.com/@hoonion"}
    ],
    "지성": [
        {"name": "Minicar", "link": "https://www.youtube.com/@minicar"}
    ],
    "민감성": [
        {"name": "Heizle", "link": "https://www.youtube.com/@heizle"}
    ],
    "복합성": [
        {"name": "Director Pi", "link": "https://www.youtube.com/@directorpi"}
    ]
}

# --------------------
# 입력 페이지
# --------------------
if st.session_state.page == "input":
    st.title("AI 스킨케어 추천 앱")

    skin_type = st.selectbox("피부 타입을 선택하세요", ["건성", "지성", "민감성", "복합성"])
    skin_status = st.text_area("현재 피부 상태를 입력하세요 (예: 붉은기, 각질, 트러블)")
    additional_info = st.text_area("추가로 알려주고 싶은 피부 고민이나 민감 부위",
                                   placeholder="예: 코 주변이 자주 벗겨짐, 눈가가 예민함 등")

    if st.button("추천 받기"):
        st.session_state.skin_type = skin_type
        st.session_state.skin_status = skin_status
        st.session_state.additional_info = additional_info
        st.session_state.page = "result"
        st.rerun()

# --------------------
# 결과 페이지
# --------------------
elif st.session_state.page == "result":
    st.title("추천 결과")

    tab1, tab2, tab3, tab4 = st.tabs(["추천 제품", "피부 원인 & 팁", "유튜버 추천", "다시 입력"])

    # 추천 제품 탭
    with tab1:
        st.subheader("추천 제품")
        for product in product_info.get(st.session_state.skin_type, []):
            st.markdown(f"### [{product['name']}]({product['link']})")
            st.write(f"- 사용 기간: {product['duration']}")
            st.write(f"- 유의점: {product['caution']}")
            st.write("---")

    # 피부 원인 & 팁 탭
    with tab2:
        st.subheader("피부 증상 원인 & 관리 팁")
        for symptom, data in skin_tips.items():
            if (symptom in st.session_state.skin_status) or (symptom in st.session_state.additional_info):
                st.markdown(f"### {symptom}")
                st.write(f"**원인:** {data['cause']}")
                st.write(f"**관리 팁:** {data['tip']}")
                st.write("---")

    # 유튜버 추천 탭
    with tab3:
        st.subheader("추천 유튜버 채널")
        for yt in youtubers.get(st.session_state.skin_type, []):
            st.markdown(f"- [{yt['name']}]({yt['link']})")

    # 다시 입력 탭
    with tab4:
        if st.button("다시 입력하기"):
            st.session_state.page = "input"
            st.rerun()
