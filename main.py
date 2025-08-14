import streamlit as st
from textwrap import dedent

# =============================
# 🧩 페이지 설정
# =============================
st.set_page_config(
    page_title="MBTI 노래 추천 🎶",
    page_icon="🎵",
    layout="centered"
)

# =============================
# 🎨 스타일
# =============================
st.markdown(
    dedent("""
    <style>
    @keyframes gradientMove {
      0% { background-position: 0% 50%; }
      50% { background-position: 100% 50%; }
      100% { background-position: 0% 50%; }
    }
    .stApp {
      background: linear-gradient(135deg, #FFD3A5, #FD6585, #FF9A8B, #A18CD1, #FBC2EB);
      background-size: 400% 400%;
      animation: gradientMove 20s ease infinite;
    }
    .mega-title {
      font-size: 42px;
      text-align: center;
      font-weight: 900;
      color: white;
      text-shadow: 0 3px 12px rgba(0,0,0,.25);
    }
    .song-card {
      padding: 20px;
      border-radius: 20px;
      text-align: center;
      box-shadow: 0 8px 20px rgba(0,0,0,.15);
      background-color: rgba(255,255,255,0.8);
      margin: 12px 0;
    }
    .song-title {
      font-size: 20px;
      font-weight: bold;
      margin-top: 8px;
    }
    .footer { text-align:center; font-size:13px; opacity:.8; margin-top: 25px; }
    </style>
    """),
    unsafe_allow_html=True
)

# =============================
# 🎵 MBTI → 노래 추천
# =============================
MBTI_SONGS = {
    "ISTJ": [
        ("김광석 - 바람이 불어오는 곳", "https://www.youtube.com/watch?v=7UuTce5gRj8"),
        ("아이유 - 밤편지", "https://www.youtube.com/watch?v=BzYnNdJhZQw"),
        ("박효신 - 야생화", "https://www.youtube.com/watch?v=uS1Sm9ZJ1YE")
    ],
    "ISFJ": [
        ("태연 - Fine", "https://www.youtube.com/watch?v=jeqdYqsrsA0"),
        ("에일리 - 첫눈처럼 너에게 가겠다", "https://www.youtube.com/watch?v=ZCAnLxRvNNc"),
        ("폴킴 - 모든 날, 모든 순간", "https://www.youtube.com/watch?v=u5r77-OQwa8")
    ],
    "INFJ": [
        ("방탄소년단 - 봄날", "https://www.youtube.com/watch?v=4ujQOR2DMFM"),
        ("볼빨간사춘기 - 우주를 줄게", "https://www.youtube.com/watch?v=8t2VQF8JXZI"),
        ("자우림 - 스물다섯, 스물하나", "https://www.youtube.com/watch?v=COIpybG6s6M")
    ],
    "INTJ": [
        ("혁오 - 톰보이", "https://www.youtube.com/watch?v=tLQLa6lM3Us"),
        ("AKMU - 어떻게 이별까지 사랑하겠어, 널 사랑하는 거지", "https://www.youtube.com/watch?v=ttx8nAHTW5M"),
        ("데이식스 - 예뻤어", "https://www.youtube.com/watch?v=4RJWqIEo_Tc")
    ],
    "ISTP": [
        ("기리보이 - 호랑이소굴", "https://www.youtube.com/watch?v=ENnAaMRTpR4"),
        ("빈지노 - Always Awake", "https://www.youtube.com/watch?v=An_b2l3X4i0"),
        ("크러쉬 - Oasis", "https://www.youtube.com/watch?v=hn7oQ_gNe8o")
    ],
    "ISFP": [
        ("아이유 - Palette", "https://www.youtube.com/watch?v=d9IxdwEFk1c"),
        ("로꼬, 유주 - 우연히 봄", "https://www.youtube.com/watch?v=HTJtK3I-Hj8"),
        ("장범준 - 노래방에서", "https://www.youtube.com/watch?v=pq8qwDP0LKY")
    ],
    "INFP": [
        ("적재 - 별 보러 가자", "https://www.youtube.com/watch?v=0FB2EoKTK_Q"),
        ("우효 - 민들레", "https://www.youtube.com/watch?v=UyIPQ6jDgjQ"),
        ("선우정아 - 도망가자", "https://www.youtube.com/watch?v=8iIU6Tp-9A0")
    ],
    "INTP": [
        ("10cm - 사랑은 은하수 다방에서", "https://www.youtube.com/watch?v=54v6mK0b-8Y"),
        ("자이언티 - 꺼내 먹어요", "https://www.youtube.com/watch?v=l0TnQ7nOqGU"),
        ("딘 - D (Half Moon)", "https://www.youtube.com/watch?v=6T9cgf0DbGs")
    ],
    "ESTP": [
        ("싸이 - 강남스타일", "https://www.youtube.com/watch?v=9bZkp7q19f0"),
        ("비 - Rainism", "https://www.youtube.com/watch?v=5nBaE-UdAlE"),
        ("ZICO - 아무노래", "https://www.youtube.com/watch?v=UuV2BmJ1p_I")
    ],
    "ESFP": [
        ("마마무 - HIP", "https://www.youtube.com/watch?v=0FB2EoKTK_Q"),
        ("현아 - Bubble Pop!", "https://www.youtube.com/watch?v=bw9CALKOvAI"),
        ("트와이스 - Cheer Up", "https://www.youtube.com/watch?v=c7rCyll5AeY")
    ],
    "ENFP": [
        ("세븐틴 - 아주 NICE", "https://www.youtube.com/watch?v=J-wFp43XOrA"),
        ("레드벨벳 - 빨간 맛", "https://www.youtube.com/watch?v=WyiIGEHQP8o"),
        ("악동뮤지션 - 200%", "https://www.youtube.com/watch?v=0degL6RjNNE")
    ],
    "ENTP": [
        ("지코 - Artist", "https://www.youtube.com/watch?v=4l5cZ0sFC6w"),
        ("G-Dragon - Crayon", "https://www.youtube.com/watch?v=t3ULhmadHkg"),
        ("CL - 나쁜 기집애", "https://www.youtube.com/watch?v=7LP4foN3Xs4")
    ],
    "ESTJ": [
        ("박진영 - Honey", "https://www.youtube.com/watch?v=rrJMBxBga-s"),
        ("엄정화 - Festival", "https://www.youtube.com/watch?v=3cL4Z70H6SE"),
        ("SES - I'm Your Girl", "https://www.youtube.com/watch?v=p1N3yqyQ2gM")
    ],
    "ESFJ": [
        ("이효리 - U-Go-Girl", "https://www.youtube.com/watch?v=beW9AH1Goxg"),
        ("카라 - Mister", "https://www.youtube.com/watch?v=EmqDfqE0pMY"),
        ("소녀시대 - Gee", "https://www.youtube.com/watch?v=U7mPqycQ0tQ")
    ],
    "ENFJ": [
        ("태연 - I", "https://www.youtube.com/watch?v=iF0Xw2Xn4J8"),
        ("방탄소년단 - Dynamite", "https://www.youtube.com/watch?v=gdZLi9oWNZg"),
        ("이선희 - 그 중에 그대를 만나", "https://www.youtube.com/watch?v=gkCkO6YpJbA")
    ],
    "ENTJ": [
        ("비욘세 - Run the World", "https://www.youtube.com/watch?v=VBmMU_iwe6U"),
        ("에미넴 - Lose Yourself", "https://www.youtube.com/watch?v=_Yhyp-_hX2s"),
        ("Queen - We Will Rock You", "https://www.youtube.com/watch?v=-tJYN-eG1zk")
    ]
}

# =============================
# 📌 UI
# =============================
st.markdown("<h1 class='mega-title'>🎵 MBTI로 듣는 추천 노래 🎶</h1>", unsafe_allow_html=True)
st.write("당신의 MBTI를 선택하면, 잘 어울리는 노래 3곡을 추천해드려요!")

mbti = st.selectbox("MBTI를 선택하세요", list(MBTI_SONGS.keys()))

if mbti:
    st.markdown(f"### 🎯 {mbti} 타입 추천곡")
    songs = MBTI_SONGS[mbti]
    for title, link in songs:
        st.markdown(
            f"""
            <div class='song-card'>
                <div class='song-title'>🎵 {title}</div>
                <a href="{link}" target="_blank">▶️ 유튜브로 듣기</a>
            </div>
            """,
            unsafe_allow_html=True
        )

st.markdown("<div class='footer'>이 사이트는 MBTI별로 어울리는 노래를 재미로 추천합니다 😊</div>", unsafe_allow_html=True)
