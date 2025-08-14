import streamlit as st

# 페이지 설정
st.set_page_config(page_title="MBTI → 짱구 캐릭터 추천", page_icon="🐻", layout="centered")

# MBTI → 캐릭터 데이터
mbti_characters = {
    "ENFP": {
        "name": "짱구 🐻",
        "desc": "엉뚱하고 장난기 많은 에너자이저! 호기심 대마왕 🔥",
        "img": "https://i.ibb.co/zsW5vZW/shinchan.png",
        "color": "#FFD93D"
    },
    "INTJ": {
        "name": "철수 📚",
        "desc": "계획적이고 이성적인 전략가! 똑똑한 두뇌파 🧠",
        "img": "https://i.ibb.co/h9mYpSS/cheolsu.png",
        "color": "#6BCB77"
    },
    "ISFJ": {
        "name": "유리 🌸",
        "desc": "다정다감하고 배려심 많은 친구! 친구 사랑 1등 🥰",
        "img": "https://i.ibb.co/JjdnzQk/yuri.png",
        "color": "#FF6F91"
    },
    "ESTP": {
        "name": "훈이 😎",
        "desc": "활발하고 사교적인 분위기 메이커! 장난도 잘 치는 스타일 😂",
        "img": "https://i.ibb.co/4NnTrM4/huni.png",
        "color": "#4D96FF"
    },
    "INFP": {
        "name": "맹구 🪨",
        "desc": "순수하고 독특한 매력을 가진 예술가 타입 🎨",
        "img": "https://i.ibb.co/RCSXHkq/maenggu.png",
        "color": "#845EC2"
    },
    "ENTJ": {
        "name": "신형만 👔",
        "desc": "책임감 있고 추진력 넘치는 가장! 하지만 라면도 좋아함 🍜",
        "img": "https://i.ibb.co/tqfPMS3/shinhyungman.png",
        "color": "#FF9671"
    },
    "ESFJ": {
        "name": "봉미선 👜",
        "desc": "다정하고 현실적인 주부! 가족 사랑 최고 💖",
        "img": "https://i.ibb.co/gJYbZJQ/bongmison.png",
        "color": "#FFC75F"
    }
}

# 스타일 (CSS)
st.markdown("""
    <style>
    body {
        background: linear-gradient(135deg, #FFDEE9 0%, #B5FFFC 100%);
    }
    .title {
        font-size: 40px;
        text-align: center;
        font-weight: bold;
        color: #FF6F91;
        text-shadow: 1px 1px 3px rgba(0,0,0,0.1);
    }
    .char-card {
        padding: 20px;
        border-radius: 20px;
        text-align: center;
        margin-top: 20px;
        box-shadow: 4px 4px 12px rgba(0,0,0,0.15);
    }
    .char-name {
        font-size: 28px;
        font-weight: bold;
        margin-top: 10px;
    }
    .char-desc {
        font-size: 18px;
        margin-top: 5px;
    }
    img {
        border-radius: 15px;
    }
    </style>
""", unsafe_allow_html=True)

# 제목
st.markdown("<div class='title'>🌈 MBTI로 알아보는 짱구 캐릭터 추천 🐻</div>", unsafe_allow_html=True)
st.write("")

# MBTI 선택
selected_mbti = st.selectbox("✨ 당신의 MBTI를 선택하세요", list(mbti_characters.keys()))

# 결과 출력
if selected_mbti:
    char = mbti_characters[selected_mbti]
    st.markdown(
        f"""
        <div class='char-card' style='background-color:{char["color"]};'>
            <img src="{char['img']}" width="200">
            <div class='char-name'>{char['name']}</div>
            <div class='char-desc'>{char['desc']}</div>
        </div>
        """,
        unsafe_allow_html=True
    )
