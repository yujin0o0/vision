import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io
import os

st.set_page_config(page_title="밈 생성기", page_icon="😂")

st.title("😂 나만의 밈 생성기")
st.markdown("문구를 입력하고 이미지를 선택해 나만의 짤을 만들어보세요!")

top_text = st.text_input("상단 문구", "이게 웃긴다고?")
bottom_text = st.text_input("하단 문구", "진짜? 😂")
uploaded_image = st.file_uploader("짤로 쓸 이미지를 업로드하거나 기본 이미지 사용", type=["jpg", "jpeg", "png"])

DEFAULT_IMAGE_PATH = "sample_meme.jpg"

# 작업 디렉터리와 파일 리스트 출력 (디버그용)
st.write("현재 작업 디렉터리:", os.getcwd())
st.write("현재 폴더 파일 목록:", os.listdir("."))

# 폰트 경로 지정 (프로젝트 루트에 있다고 가정)
FONT_PATH = os.path.join(os.getcwd(), "NanumGothicBold.ttf")

@st.cache_data
def load_default_image():
    try:
        return Image.open(DEFAULT_IMAGE_PATH)
    except:
        st.error("❗ 기본 이미지(sample_meme.jpg)를 찾을 수 없습니다.")
        return None

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

def create_meme(image, top_text, bottom_text):
    draw = ImageDraw.Draw(image)
    font_size = max(int(image.width / 2), 100)  # 글자 크게, 최소 100 보장

    try:
        font = ImageFont.truetype(FONT_PATH, font_size)
    except OSError:
        st.error(f"❗ 한글 폰트 파일을 찾을 수 없습니다: {FONT_PATH}")
        font = ImageFont.load_default()

    draw_centered_text(draw, top_text, font, image.width, 10)

    try:
        bbox = draw.textbbox((0, 0), bottom_text, font=font)
        text_height = bbox[3] - bbox[1]
    except AttributeError:
        text_height = draw.textsize(bottom_text, font=font)[1]

    y_bottom = image.height - text_height - 10
    draw_centered_text(draw, bottom_text, font, image.width, y_bottom)

    return image

if uploaded_image:
    image = Image.open(uploaded_image)
else:
    image = load_default_image()

if image and st.button("📸 밈 생성하기!"):
    meme = create_meme(image.copy(), top_text, bottom_text)
    st.image(meme, caption="🎉 생성된 밈", use_column_width=True)

    buf = io.BytesIO()
    meme.save(buf, format="PNG")
    byte_im = buf.getvalue()

    st.download_button(
        label="💾 밈 이미지 다운로드",
        data=byte_im,
        file_name="meme.png",
        mime="image/png"
    )
