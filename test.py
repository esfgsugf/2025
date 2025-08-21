if st.session_state.page == "input":
    st.title("💧 나만의 스킨케어 코치 💧")

    skin_type = st.selectbox("피부 타입 선택", ["건성", "지성", "민감성", "복합성", "수부지"], key="skin_type_select_input")
    main_concern = st.radio("가장 고민되는 피부 상태 선택", ["붉은기(홍조)", "각질", "트러블(여드름)", "민감함", "없음"], key="main_concern_radio_input")
    other_concerns = st.text_input("기타 고민 입력", placeholder="예: 모공, 탄력 저하, 잡티 등", key="other_concerns_input_field")
    uploaded_image = st.file_uploader("피부 사진 업로드 (선택)", type=["png","jpg","jpeg"], key="upload_image_input")

    next_clicked = st.button("다음", key="next_button_input")
    if next_clicked:
        image = Image.open(uploaded_image) if uploaded_image else None
        ai_results, analysis_details = simple_skin_analysis(image)
        st.session_state.skin_status = ai_results
        st.session_state.skin_analysis_details = analysis_details
        st.session_state.skin_type = skin_type
        st.session_state.main_concern_radio = main_concern
        st.session_state.other_concerns_input = other_concerns
        st.session_state.uploaded_image = uploaded_image
        st.session_state.page = "result"
        # rerun 제거 → 조건부로 page 렌더링
