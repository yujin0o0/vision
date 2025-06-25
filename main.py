import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io
import os

st.set_page_config(page_title="밈 생성기", page_icon="😂")

st.title("😂 나만의 밈 생성기")
st.markdown("문구를 입력하고 이미지를 선택해 나만의 짤을 만들어보세요!")

# 사용자 입력
top_text = st.text_input("상단 문구", "이게 웃긴다고?")
bottom_text = st.text_input("하단 문구", "진짜? 😂")
uploaded_image = st.file_uploader("짤로 쓸 이미지를 업로드하거나 기본 이미지 사용", type=["jpg", "jpeg", "png"])

# 파일 경로
DEFAULT_IMAGE_PATH = "sample_meme.jpg"
FONT_PATH = "NanumGothicBold.ttf"  # 반드시 GitHub 루트에 업로드되어 있어야 함

# 디버그용 출력
st.write("📁 현재 디렉터리:", os.getcwd())
st.write("📄 폴더 내 파일 목록:", os.listdir("."))

# 기본 이미지 불러오기
@st.cache_data
def load_default_image():
    try:
        return Image.open(DEFAULT_IMAGE_PATH)
    except:
        st.error("❗ 기본 이미지(sample_meme.jpg)를 찾을 수 없습니다.")
        return None

# 텍스트 중앙 정렬해서 그림 위에 씌우기
def draw_centered_text(draw, text, font, image_width, y_position):
    try:
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
    except AttributeError:
        text_width, _ = draw.textsize(text, font=font)
    x_position = (image_width - text_width) / 2
    draw.text(
        (x_position, y_position),
        text,
        font=font,
        fill="white",
        stroke_width=3,
        stroke_fill="black"
    )

# 밈 생성 함수
def create_meme(image, top_text, bottom_text):
    draw = ImageDraw.Draw(image)
    font_size = max(int(image.width * 0.12), 80)  # 이미지 너비 기준으로 크게

    try:
        font = ImageFont.truetype(FONT_PATH, font_size)
    except OSError:
        st.error(f"❗ 폰트 파일을 찾을 수 없습니다: {FONT_PATH}")
        font = ImageFont.load_default()

    draw_centered_text(draw, top_text, font, image.width, 10)

    try:
        bbox = draw.textbbox((0,
