import streamlit as st
from PIL import Image

st.title("📸 맞춤형 스킨케어 추천 앱")

# 1. 피부 타입 선택
skin_type = st.selectbox("내 피부 타입을 선택하세요", ["건성", "지성", "복합성", "민감성"])

# 2. 추가 텍스트 입력
additional_info = st.text_area("추가로 알려주고 싶은 피부 고민이나 민감 부위", placeholder="예: 왼쪽 볼 예민, 턱 좁쌀 여드름")

# 3. 사진 업로드 (선택)
uploaded_file = st.file_uploader("피부 사진을 업로드하세요 (선택)", type=["jpg", "png", "jpeg"])

# 4. AI 분석 버튼
if st.button("AI 피부 분석"):
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="업로드한 피부 사진", use_column_width=True)
        
        # --- 실제 AI 분석 연결 가능 ---
        st.subheader("✨ AI 분석 결과 (예시)")
        st.write("- 피부 상태: 건조 + 각질 + 일부 붉은기")
    else:
        st.warning("사진을 업로드하지 않으셨습니다. 직접 입력한 정보를 기반으로 분석합니다.")
        st.write("- 피부 상태: 입력 정보 기반 예시 분석")

# 5. 추천 제품 버튼
if st.button("추천 제품 보기"):
    st.subheader("🧴 추천 제품")
    # 예시 추천 로직
    if "붉은기" in additional_info or (uploaded_file is not None and "붉은기" in "예시 분석"):
        st.write("- 시카 토너: 라로슈포제 시카 토너")
        st.write("- 시카 크림: 닥터자르트 시카페어 크림")
    elif "각질" in additional_info:
        st.write("- 각질 케어 토너: 라네즈 크림스킨 토너")
        st.write("- 수분 크림: 아벤느 시칼파트 크림")
    else:
        st.write("- 기본 보습 토너/크림 추천")
