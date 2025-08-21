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

# 결과 화면에서 탭 구성
tab1, tab2, tab3, tab4 = st.tabs(["추천 제품", "피부 원인 & 팁", "유튜버 추천", "다시 입력"])

with tab1:
    st.subheader("추천 제품")
    # 제품 리스트 출력 (기존 코드 활용)

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
