import streamlit as st
from PIL import Image

st.set_page_config(page_title="AI 피부 분석 & 스킨케어 추천", layout="centered")

if "page" not in st.session_state:
    st.session_state.page = "input"

# 제품 정보 예시
product_info = {
    "진정": [
        {
            "name": "라로슈포제 시카플라스트 밤B5",
            "link": "https://www.oliveyoung.co.kr/store/goods/getGoodsDetail.do?goodsNo=A000000000",
            "period": "2주 이상 사용 가능",
            "caution": "상처 부위는 피하고 얇게 발라주세요."
        },
        {
            "name": "닥터지 레드 블레미쉬 수딩 크림",
            "link": "https://www.oliveyoung.co.kr/store/goods/getGoodsDetail.do?goodsNo=B000000000",
            "period": "매일 사용 가능",
            "caution": "저녁에 충분히 흡수되도록 사용"
        }
    ],
    "보습": [
        {
            "name": "세타필 모이스춰라이징 로션",
            "link": "https://www.oliveyoung.co.kr/store/goods/getGoodsDetail.do?goodsNo=C000000000",
            "period": "아침, 저녁 꾸준히 사용",
            "caution": "피부가 붉을 때는 적게 사용"
        }
    ]
}

# 피부 증상별 원인과 관리 팁
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

# 피부 타입별 유튜버 추천
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

if st.session_state.page == "input":
    st.title("AI 피부 분석 & 스킨케어 추천")

    skin_type = st.radio("피부 타입을 선택하세요", ["건성", "지성", "민감성", "복합성"])

    st.write("### 피부 상태를 선택하거나 입력하세요")
    selected_status = st.multiselect("피부 상태 선택", ["붉은기", "각질", "여드름", "민감함"])
    custom_status = st.text_input("추가 입력 (쉼표로 구분)", placeholder="예: 트러블, 홍조")

    # 입력값을 리스트로 변환 후 합치기
    custom_status_list = [s.strip() for s in custom_status.split(",") if s.strip()]
    skin_status = selected_status + custom_status_list

    additional_info = st.text_area("추가로 알려주고 싶은 피부 고민", placeholder="예: 코 주변이 많이 건조해요.")

    photo = st.file_uploader("피부 사진을 업로드하세요 (선택사항)", type=["jpg", "png"])
    use_ai = st.checkbox("사진 없이 AI 분석하기")

    if st.button("추천 받기"):
        st.session_state.skin_type = skin_type
        st.session_state.skin_status = skin_status
        st.session_state.additional_info = additional_info
        st.session_state.page = "result"
        st.rerun()

elif st.session_state.page == "result":
    st.title("추천 결과")

    tab1, tab2, tab3, tab4 = st.tabs(["추천 제품", "피부 원인 & 팁", "유튜버 추천", "다시 입력"])

    with tab1:
        st.subheader("추천 제품")
        for status in st.session_state.skin_status:
            if status in ["붉은기", "민감함"]:
                category = "진정"
            else:
                category = "보습"
            for product in product_info.get(category, []):
                st.markdown(f"### [{product['name']}]({product['link']})")
                st.write(f"사용 기간: {product['period']}")
                st.write(f"주의사항: {product['caution']}")
                st.write("---")

    with tab2:
        st.subheader("피부 증상 원인 & 관리 팁")
        for symptom, data in skin_tips.items():
            if symptom in st.session_state.skin_status or symptom in st.session_state.additional_info:
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
            st.rerun()
