# app.py
import io
from typing import Tuple, Optional

import streamlit as st
from PIL import Image, ImageDraw, ImageFont, ImageOps

# --- (선택) drawable-canvas 사용 가능 여부 체크 ---
try:
    from streamlit_drawable_canvas import st_canvas  # pip install streamlit-drawable-canvas
    HAS_CANVAS = True
except Exception:
    HAS_CANVAS = False

st.set_page_config(page_title="덕질 다이어리", page_icon="✨", layout="wide")

# =============================
# 유틸 함수
# =============================
CARD_W, CARD_H = 720, 960  # 3:4 포토카드 비율

@st.cache_data(show_spinner=False)
def load_font(ttf_bytes: Optional[bytes], size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    """
    업로드된 폰트(ttf)가 있으면 그걸 사용, 없으면 기본 폰트로 대체.
    주의: 기본 폰트는 한글/이모지 렌더링이 제한적일 수 있음.
    """
    try:
        if ttf_bytes:
            return ImageFont.truetype(io.BytesIO(ttf_bytes), size=size)
        # DejaVuSans는 라틴은 잘 되지만 한글은 제한적.
        # 환경에 따라 설치되어 있을 수도 있음. 없으면 except로.
        return ImageFont.truetype("DejaVuSans.ttf", size=size)
    except Exception:
        return ImageFont.load_default()

def fit_to_card(img: Image.Image, bg_color: Tuple[int, int, int]=(255, 255, 255)) -> Image.Image:
    """이미지를 포토카드 사이즈(CARD_W x CARD_H)에 맞춰 레터박스(패딩) 포함 리사이즈."""
    img = img.convert("RGBA")
    # 대상 비율
    target_ratio = CARD_W / CARD_H
    w, h = img.size
    ratio = w / h

    if ratio > target_ratio:
        # 가로가 더 긴 경우: 가로를 맞추고 세로에 패딩
        new_w = CARD_W
        new_h = int(CARD_W / ratio)
    else:
        # 세로가 더 긴 경우: 세로를 맞추고 가로에 패딩
        new_h = CARD_H
        new_w = int(CARD_H * ratio)

    img_resized = img.resize((new_w, new_h), Image.LANCZOS)

    canvas = Image.new("RGBA", (CARD_W, CARD_H), bg_color + (255,))
    x = (CARD_W - new_w) // 2
    y = (CARD_H - new_h) // 2
    canvas.paste(img_resized, (x, y), img_resized)
    return canvas

def rounded_frame(im: Image.Image, radius: int, border_px: int, border_color: Tuple[int,int,int]) -> Image.Image:
    """라운드 처리 + 테두리."""
    im = im.copy()
    # 라운드 마스크
    mask = Image.new("L", im.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle((0, 0, im.size[0], im.size[1]), radius=radius, fill=255)
    im = Image.composite(im, Image.new("RGBA", im.size, (0,0,0,0)), mask)

    if border_px > 0:
        # 테두리는 별도 레이어에 그림
        border_layer = Image.new("RGBA", im.size, (0,0,0,0))
        d = ImageDraw.Draw(border_layer)
        # 테두리 안쪽으로 그리기
        for i in range(border_px):
            d.rounded_rectangle(
                (i, i, im.size[0]-1-i, im.size[1]-1-i),
                radius=max(0, radius - i),
                outline=border_color + (255,)
            )
        im = Image.alpha_composite(im, border_layer)
    return im

def draw_text_on_image(im: Image.Image, text: str, xy: Tuple[int,int], font: ImageFont.ImageFont, color: Tuple[int,int,int], stroke: int=0) -> Image.Image:
    im = im.copy()
    d = ImageDraw.Draw(im)
    # PIL은 hex 색상을 직접 못 읽으므로 튜플 전달
    d.text(xy, text, font=font, fill=color + (255,), stroke_width=stroke, stroke_fill=(0,0,0,255))
    return im

def draw_emoji_sticker(im: Image.Image, emoji: str, xy: Tuple[int,int], font: ImageFont.ImageFont) -> Image.Image:
    """이모지를 텍스트로 렌더링(환경에 따라 흑백/사각형으로 보일 수 있음)."""
    im = im.copy()
    d = ImageDraw.Draw(im)
    d.text(xy, emoji, font=font, fill=(255,255,255,255))
    return im

def hex_to_rgb(hex_str: str) -> Tuple[int,int,int]:
    hex_str = hex_str.lstrip("#")
    return tuple(int(hex_str[i:i+2], 16) for i in (0, 2, 4))

def to_download_bytes(im: Image.Image) -> bytes:
    buf = io.BytesIO()
    im.save(buf, format="PNG")
    buf.seek(0)
    return buf.read()

# =============================
# 세션 상태
# =============================
if "favorites" not in st.session_state:
    st.session_state.favorites = []

# =============================
# 사이드바
# =============================
st.title("✨ 덕질 다이어리 앱")
st.caption("포토카드 꾸미기 + 아이돌/배우 정보 한 번에!")

menu = st.sidebar.radio("메뉴 선택", ["홈", "포토카드 꾸미기", "아이돌/배우 정보"])

# =============================
# 홈
# =============================
if menu == "홈":
    st.subheader("환영합니다 💖")
    st.markdown(
        "- **포토카드 꾸미기**: 최애 사진 업로드 → 라운딩/프레임/텍스트/스티커로 꾸미기 → PNG 저장\n"
        "- **아이돌/배우 정보**: 이름 검색 → 대표 작품/예능(예시 데이터) → 즐겨찾기 저장"
    )
    if not HAS_CANVAS:
        st.info("자유 그리기 기능을 사용하려면 `pip install streamlit-drawable-canvas` 설치 후 재실행하세요.")

# =============================
# 포토카드 꾸미기
# =============================
elif menu == "포토카드 꾸미기":
    st.subheader("📸 포토카드 꾸미기")
    col_left, col_right = st.columns([1,1])

    with col_left:
        uploaded = st.file_uploader("최애 사진 업로드 (JPG/PNG)", type=["jpg","jpeg","png"])
        font_file = st.file_uploader("한글/특수문자용 폰트 업로드 (선택, TTF)", type=["ttf","otf"])

        with st.expander("카드 옵션"):
            bg_hex = st.color_picker("레터박스 배경색", "#FFFFFF")
            radius = st.slider("라운드 정도", 0, 80, 24)
            border_px = st.slider("프레임 두께(px)", 0, 16, 6)
            border_hex = st.color_picker("프레임 색상", "#FF7AC8")

        with st.expander("텍스트 추가"):
            text = st.text_input("표시할 텍스트", "최애 최고!")
            text_size = st.slider("텍스트 크기", 16, 120, 48)
            text_hex = st.color_picker("텍스트 색상", "#FFFFFF")
            stroke = st.slider("텍스트 외곽선(가독성)", 0, 6, 2)
            x_text = st.slider("텍스트 X 위치", 0, CARD_W, 40)
            y_text = st.slider("텍스트 Y 위치", 0, CARD_H, CARD_H - 120)

        with st.expander("스티커(이모지) 추가 - 최대 3개"):
            sticker_choices = ["✨","★","♡","❤","✦","♬","♪","✔","🫶","🌟"]
            use_s1 = st.checkbox("스티커 1 사용", True)
            s1 = st.selectbox("스티커 1", sticker_choices, index=0)
            s1_size = st.slider("스티커 1 크기", 24, 160, 72)
            s1x = st.slider("스티커 1 X", 0, CARD_W, CARD_W - 140)
            s1y = st.slider("스티커 1 Y", 0, CARD_H, 40)

            use_s2 = st.checkbox("스티커 2 사용", False)
            s2 = st.selectbox("스티커 2", sticker_choices, index=1)
            s2_size = st.slider("스티커 2 크기", 24, 160, 64)
            s2x = st.slider("스티커 2 X", 0, CARD_W, 40)
            s2y = st.slider("스티커 2 Y", 0, CARD_H, 40)

            use_s3 = st.checkbox("스티커 3 사용", False)
            s3 = st.selectbox("스티커 3", sticker_choices, index=2)
            s3_size = st.slider("스티커 3 크기", 24, 160, 56)
            s3x = st.slider("스티커 3 X", 0, CARD_W, CARD_W//2)
            s3y = st.slider("스티커 3 Y", 0, CARD_H, CARD_H//2)

        enable_draw = HAS_CANVAS and st.checkbox("자유 그리기(펜) 사용", False)

    with col_right:
        if uploaded:
            base = Image.open(uploaded)
            card = fit_to_card(base, bg_color=hex_to_rgb(bg_hex))
            # 프레임/라운딩
            card = rounded_frame(card, radius=radius, border_px=border_px, border_color=hex_to_rgb(border_hex))

            # 폰트 로드
            user_font_bytes = font_file.read() if font_file else None
            font_text = load_font(user_font_bytes, text_size)
            font_s1 = load_font(user_font_bytes, s1_size)
            font_s2 = load_font(user_font_bytes, s2_size)
            font_s3 = load_font(user_font_bytes, s3_size)

            # 텍스트
            if text.strip():
                card = draw_text_on_image(card, text, (x_text, y_text), font_text, hex_to_rgb(text_hex), stroke=stroke)

            # 스티커(이모지)
            if use_s1: card = draw_emoji_sticker(card, s1, (s1x, s1y), font_s1)
            if use_s2: card = draw_emoji_sticker(card, s2, (s2x, s2y), font_s2)
            if use_s3: card = draw_emoji_sticker(card, s3, (s3x, s3y), font_s3)

            st.image(card, caption="미리보기", use_container_width=True)

            # 자유 드로잉 캔버스 (선택)
            if enable_draw:
                st.markdown("**펜으로 자유롭게 덧그리기**")
                canvas = st_canvas(
                    fill_color="rgba(0,0,0,0)",
                    stroke_width=4,
                    stroke_color="#000000",
                    background_image=card.convert("RGB"),
                    update_streamlit=True,
                    height=CARD_H//2,  # 미리보기 영역(저장 시 원본에 합성)
                    width=CARD_W//2,
                    drawing_mode="freedraw",
                    key="draw_canvas",
                )
                # 참고: drawable-canvas 결과를 원본 크기에 합성하려면 좌표 변환/리사이즈 로직이 필요.
                # 간단히: 캔버스 이미지를 원본 크기로 리사이즈해 합성:
                if canvas and canvas.image_data is not None:
                    over = Image.fromarray((canvas.image_data).astype("uint8"))
                    over = over.resize((CARD_W, CARD_H), Image.LANCZOS).convert("RGBA")
                    card = Image.alpha_composite(card, over)

            # 다운로드
            png_bytes = to_download_bytes(card)
            st.download_button(
                "📥 PNG로 다운로드",
                data=png_bytes,
                file_name="photocard.png",
                mime="image/png"
            )
        else:
            st.info("좌측에서 이미지를 업로드하면 미리보기가 표시됩니다.")

# =============================
# 아이돌/배우 정보
# =============================
elif menu == "아이돌/배우 정보":
    st.subheader("🎬 아이돌/배우 정보 검색 (예시 데이터)")

    name = st.text_input("이름을 입력하세요 (예: 아이유, 박보검, 장원영)")
    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("검색"):
            if not name.strip():
                st.warning("이름을 입력해 주세요.")
            else:
                sample = {
                    "아이유": {
                        "드라마": ["호텔 델루나", "프로듀사"],
                        "예능": ["효리네 민박", "유희열의 스케치북(게스트)"],
                        "앨범/음원": ["Love Poem", "Palette"]
                    },
                    "박보검": {
                        "드라마": ["응답하라 1988", "구르미 그린 달빛", "청춘기록"],
                        "영화": ["서복", "원더랜드"],
                        "예능": ["런닝맨(게스트)", "1박2일(시즌3 스페셜)"]
                    },
                    "장원영": {
                        "예능/방송": ["뮤직뱅크 MC", "피크타임(게스트)"],
                        "음악": ["IVE - LOVE DIVE", "IVE - I AM"]
                    }
                }
                data = sample.get(name, None)
                if data is None:
                    st.error("아직 예시 데이터에 없습니다. (TMDB/위키 API 연동 가능)")
                else:
                    for k, v in data.items():
                        st.markdown(f"**{k}**")
                        for item in v:
                            st.write("•", item)
    with col_b:
        if st.button("⭐ 즐겨찾기에 추가"):
            if name.strip():
                st.session_state.favorites.append(name.strip())
                st.success(f"'{name.strip()}' 즐겨찾기에 추가됨!")
            else:
                st.warning("이름을 먼저 입력하세요.")

    st.divider()
    st.markdown("#### ⭐ 내 즐겨찾기")
    if st.session_state.favorites:
        st.write(", ".join(st.session_state.favorites))
    else:
        st.caption("아직 즐겨찾기가 없어요.")

    st.info(
        "실서비스로 확장하려면 TMDB API(드라마/영화), 공식 유튜브/스포티파이 API(뮤직), "
        "위키 기반 출연 목록 크롤링 등을 연결하면 좋습니다."
    )
