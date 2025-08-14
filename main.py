import streamlit as st

# 페이지 설정
st.set_page_config(page_title="MBTI 직업 추천 🎯", page_icon="💼", layout="centered")

# MBTI별 직업 데이터
mbti_jobs = {
    "ISTJ": ["📊 회계사", "🖥️ 데이터 분석가", "⚖️ 법률가"],
    "ISFJ": ["💉 간호사", "🤝 사회복지사", "📚 교사"],
    "INFJ": ["🧠 심리상담사", "✍️ 작가", "🔬 연구원"],
    "INTJ": ["📈 전략가", "💻 개발자", "🗂️ 경영 컨설턴트"],
    "ISTP": ["🔧 기계 엔지니어", "🚑 응급 구조사", "🛫 항공 정비사"],
    "ISFP": ["📷 사진작가", "🎵 음악가", "🎨 디자이너"],
    "INFP": ["📖 작가", "🎭 예술가", "💬 상담가"],
    "INTP": ["🔬 연구원", "🖥️ 프로그래머", "⚛️ 이론 물리학자"],
    "ESTP": ["📢 마케팅 전문가", "🤝 영업사원", "📰 기자"],
    "ESFP": ["🎬 배우", "🎤 가수", "🎉 이벤트 기획자"],
    "ENFP": ["🚀 창업가", "📺 광고기획자", "🎙️ 강연가"],
    "ENTP": ["💡 발명가", "💼 사업가", "🏢 스타트업 창업자"],
    "ESTJ": ["🎖️ 군인", "🏦 경영자", "📋 프로젝트 매니저"],
    "ESFJ": ["🏫 교사", "💊 간호사", "🧑‍💼 HR 매니저"],
    "ENFJ": ["📚 교육자", "🗳️ 정치인", "🏅 코치"],
    "ENTJ": ["👑 CEO", "📊 전략 컨설턴트", "💼 경영진"]
}

# 스타일 (HTML + CSS)
st.markdown("""
    <style>
    .title {
        font-size: 40px;
        text-align: center;
        color: #ff69b4;
        font-weight: bold;
    }
    .job-card {
        background-color: #fff5f8;
        padding: 15px;
        border-radius: 15px;
        margin: 10px 0;
        font-size: 20px;
        box-shadow: 2px 2px 8px rgba(255,105,180,0.3);
    }
    </style>
""", unsafe_allow_html=True)

# 제목
st.markdown("<div class='title'>💼✨ MBTI 직업 추천 ✨💼<br>당신의 성향에 딱 맞는 직업 찾기 🔍</div>", unsafe_allow_html=True)
st.write("")

# MBTI 선택
selected_mbti = st.selectbox("🌈 **당신의 MBTI를 선택하세요**", list(mbti_jobs.keys()))

# 결과 출력
if selected_mbti:
    st.markdown(f"### 📌 {selected_mbti} 추천 직업 🎯")
    for job in mbti_jobs[selected_mbti]:
        st.markdown(f"<div class='job-card'>{job}</div>", unsafe_allow_html=True)

# 푸터
st.write("---")
st.markdown("💡 *이 사이트는 교육용으로 제작되었습니다.*")
