import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io

st.set_page_config(page_title="밈 생성기", page_icon="😂")

st.title("😂 나만의 밈 생성기")
st.markdown("원하는 문구를 넣어서 나만의 짤을 만들어보세요!")

# 사용자가 입력할 텍스트
top_text = st.text_input("상단 문구", "이게 웃긴다고?")
bottom_text = st.text_input("하단 문구", "진짜? 😂")

# 이미지 업로드 or 기본 이미지 사용
uploaded_image = st.file_uploader("짤로 쓸 이미지를 업로드하거나 기본 이미지로 생성하세요", type=["jpg", "jpeg", "png"])

# 기본 이미지 불러오기
if uploaded_image:
    image = Image.open(uploaded_image)
else:
    image = Image.open("sample_meme.jpg")  # 같은 폴더에 기본 이미지 저장

# 이미지에 문구 입히기
def create_meme(image, top_text, bottom_text):
    draw = ImageDraw.Draw(image)
    font_size = int(image.width / 12)
    try:
        font = ImageFont.truetype("arial.ttf", font_size)
    except:
        font = ImageFont.load_default()

    # 텍스트 삽입 (상단)
    draw.text((10, 10), top_text.upper(), font=font, fill="white", stroke_width=2, stroke_fill="black")

    # 텍스트 삽입 (하단)
    text_width, text_height = draw.textsize(bottom_text, font=font)
    x = 10
    y = image.height - text_height - 10
    draw.text((x, y), bottom_text.upper(), font=font, fill="white", stroke_width=2, stroke_fill="black")

    return image

if st.button("📸 밈 생성하기!"):
    meme = create_meme(image.copy(), top_text, bottom_text)
    st.image(meme, caption="생성된 밈", use_column_width=True)

    # 다운로드 링크 생성
    buf = io.BytesIO()
    meme.save(buf, format="PNG")
    byte_im = buf.getvalue()
    st.download_button(
        label="💾 밈 이미지 다운로드",
        data=byte_im,
        file_name="meme.png",
        mime="image/png"
    )
