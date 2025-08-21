import streamlit as st
from PIL import Image

# --- 페이지 설정 ---
st.set_page_config(page_title="맞춤형 스킨케어 추천", layout="centered")
st.title("📸 맞춤형 스킨케어 추천 앱")

# --- CSS 스타일 (배경 + 버튼 꾸미기) ---
st.markdown("""
<style>
.stApp {
    background-color: #e0f7fa;
    background-image: url('https://em-content.zobj.net/thumbs/240/apple/354/water-wave_1f30a.png');
    background-repeat: no-repeat;
    background-position: bottom right;
    background-size: 150px 150px;
    font-family: 'Helvetica', sans-serif;
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
</style>
""", unsafe_allow_html=True)

# --- 세션 상태 초기화 ---
for key, default in [("page", "input"), ("skin_status", ""), ("image", None), ("additional_info", ""), ("skin_type", "")]:
    if key not in st.session_state:
        st.session_state[key] = default

# --- 제품 데이터 ---
product_info = {
    "라로슈포제 시카 토너": {
        "link": "https://www.oliveyoung.co.kr/product?pid=example1",
        "usage": "아침/저녁 사용, 2~3개월 사용 가능",
        "caution": "민감 피부는 패치 테스트 권장"
    },
    "닥터자르트 시카페어 크림": {
        "link": "https://www.oliveyoung.co.kr/product?pid=example2",
        "usage": "아침/저녁, 소량 사용",
        "caution": "상처 난 부위 직접 사용 주의"
    },
    "라네즈 크림스킨 토너": {
        "link": "https://www.oliveyoung.co.kr/product?pid=example3",
        "usage": "아침/저녁, 화장솜에 적당량 사용",
        "caution": "과다 사용 시 끈적임 발생"
    },
    "아벤느 시칼파트 크림": {
        "link": "https://www.oliveyoung.co.kr/product?pid=example4",
        "usage": "건조 부위 중심으로 사용, 1~2개월 사용 가능",
        "caution": "눈가 직접 사용 주의"
    },
    "약국 연고": {
        "link": "https://www.oliveyoung.co.kr/product?pid=example5",
        "usage": "트러블 부위 점사용",
        "caution": "장기간 사용 시 피부 자극 가능"
    }
}

# --- 입력 화면 ---
if st.session_state.page == "input":
    skin_type = st.selectbox(
        "내 피부 타입을 선택하세요",
        ["건성", "지성", "복합성", "민감성", "수부지"]
    )

    additional_info = st.text_area(
        "추가로 알려주고 싶은 피부 고민이나 민감 부위",
        placeholder="예: 왼쪽 볼 예민, 턱 좁쌀 여드름"
    )

    uploaded_file = st.file_uploader(
        "피부 사진을 업로드하세요 (선택)",
        type=["jpg", "png", "jpeg"]
    )

    if st.button("AI 피부 분석 & 추천"):
        st.session_state.skin_type = skin_type
        st.session_state.additional_info = additional_info

        if uploaded_file is not None:
            st.session_state.image = Image.open(uploaded_file)
            st.session_state.skin_status = "건조 + 각질 + 일부 붉은기"
        else:
            st.session_state.image = None
            st.session_state.skin_status = "입력 정보 기반 예시 분석"

        st.session_state.page = "result"

# --- 결과 화면 ---
if st.session_state.page == "result":
    st.subheader("✨ 분석 결과")
    
    if st.session_state.image is not None:
        st.image(st.session_state.image, caption="업로드한 피부 사진", use_column_width=True)

    st.write(f"- 피부 타입: {st.session_state.skin_type}")
    st.write(f"- 피부 상태: {st.session_state.skin_status}")
    st.write(f"- 추가 정보: {st.session_state.additional_info}")

    # --- 추천 제품 ---
    st.subheader("🧴 추천 제품")
    recommended = []

    if "붉은기" in st.session_state.skin_status or "예민" in st.session_state.additional_info:
        recommended = ["라로슈포제 시카 토너", "닥터자르트 시카페어 크림", "약국 연고"]
    elif "각질" in st.session_state.skin_status or "각질" in st.session_state.additional_info:
        recommended = ["라네즈 크림스킨 토너", "아벤느 시칼파트 크림"]
    else:
        recommended = ["라로슈포제 시카 토너", "아벤느 시칼파트 크림"]

    for p in recommended:
        info = product_info[p]
        st.markdown(f"**[{p}]({info['link']})**")
        st.write(f"- 사용 기간: {info['usage']}")
        st.write(f"- 유의 사항: {info['caution']}")
        st.write("---")

    if st.button("🔙 이전 화면으로 돌아가기"):
        st.session_state.page = "input"
