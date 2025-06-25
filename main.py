import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io

# 페이지 설정
st.set_page_config(page_title="밈 생성기", page_icon="😂")

st.title("😂 나만의 밈 생성기")
st.markdown("문구를 입력하고 이미지를 선택해 나만의 짤을 만들어보세요!")

# 사용자 입력
top_text = st.text_input("상단 문구", "이게 웃긴다고?")
bottom_text = st.text_input("하단 문구", "진짜? 😂")
uploaded_image = st.file_uploader("짤로 쓸 이미지를 업로드하거나 기본 이미지 사용", type=["jpg", "jpeg", "png"])

# 기본 이미지 경로 (같은 폴더에 sample_meme.jpg 넣어두기)
DEFAULT_IMAGE_PATH = "sample_meme.jpg"

# 기본 이미지 불러오기 함수
@st.cache_data
def load_default_image():
    try:
        return Image.open(DEFAULT_IMAGE_PATH)
    except:
        st.error("기본 이미지가 없습니다. sample_meme.jpg 파일을 프로젝트에 포함시켜 주세요.")
        return None

# 중앙 정렬 텍스트 삽입 함수 (textbbox 사용)
def draw_centered_text(draw, text, font, image_width, y_position):
    try:
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
    except AttributeError:
        # Pillow 버전 낮은 경우 fallback
        text_width, _ = draw.textsize(text, font=font)

    x_position = (image_width - text_width) / 2
    draw.text((x_position, y_position), text, font=font, fill="white", stroke_width=2, stroke_fill="black")

# 밈 생성 함수
def create_meme(image, top_text, bottom_text):
    draw = ImageDraw.Draw(image)
    font_size = int(image.width / 12)

    try:
        font = ImageFont.truetype("arial.ttf", font_size)
    except:
        font = ImageFont.load_default()

    # 상단 텍스트
    draw_centered_text(draw, top_text.upper(), font, image.width, 10)

    # 하단 텍스트
    try:
        bbox = draw.textbbox((0, 0), bottom_text.upper(), font=font)
        text_height = bbox[3] - bbox[1]
    except AttributeError:
        text_height = draw.textsize(bottom_text.upper(), font=font)[1]

    y_bottom = image.height - text_height - 10
    draw_centered_text(draw, bottom_text.upper(), font, image.width, y_bottom)

    return image

# 이미지 선택
if uploaded_image:
    image = Image.open(uploaded_image)
else:
    image = load_default_image()

# 밈 생성
if image and st.button("📸 밈 생성하기!"):
    meme = create_meme(image.copy(), top_text, bottom_text)
    st.image(meme, caption="🎉 생성된 밈", use_column_width=True)

    # 다운로드 링크
    buf = io.BytesIO()
    meme.save(buf, format="PNG")
    byte_im = buf.getvalue()

    st.download_button(
        label="💾 밈 이미지 다운로드",
        data=byte_im,
        file_name="meme.png",
        mime="image/png"
    )
