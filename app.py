import streamlit as st
from rembg import remove
from PIL import Image
import io

st.set_page_config(page_title="صانع صور المعاملات", page_icon="📷", layout="centered")

st.markdown("<h1 style='text-align: center; color: #1f77b4;'>📷 صانع صور المعاملات الذكي</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: gray;'>أضف صورتك الشخصية، ودع الذكاء الاصطناعي يعالجها فوراً</p>", unsafe_allow_html=True)

uploaded_file = st.file_uploader("اختر صورتك الشخصية من الاستوديو", type=["jpg", "jpeg", "png"])

col1, col2 = st.columns(2)
with col1:
    bg_color = st.selectbox("لون الخلفية", ["أبيض (رسمي)", "أزرق (جوازات)", "أحمر"])
with col2:
    size_type = st.selectbox("القياس القياسي", ["3x4 سم", "4x6 سم"])

if uploaded_file is not None:
    st.image(uploaded_file, caption="الصورة الأصلية", use_container_width=True)
    
    if st.button("معالجة الصورة وإزالة الخلفية", use_container_width=True):
        with st.spinner("جاري المعالجة بالذكاء الاصطناعي، انتظر قليلاً..."):
            input_bytes = uploaded_file.read()
            output_bytes = remove(input_bytes, model_name='u2netp')
            output_image = Image.open(io.BytesIO(output_bytes)).convert("RGBA")
            
            color_map = {
                'أبيض (رسمي)': (255, 255, 255, 255),
                'أزرق (جوازات)': (0, 119, 182, 255),
                'أحمر': (217, 4, 41, 255)
            }
            bg_rgb = color_map.get(bg_color, (255, 255, 255, 255))
            
            background = Image.new("RGBA", output_image.size, bg_rgb)
            final_image = Image.alpha_composite(background, output_image)
            
            if size_type == '4x6 سم':
                final_image = final_image.resize((400, 600), Image.Resampling.LANCZOS)
            else:
                final_image = final_image.resize((300, 400), Image.Resampling.LANCZOS)
            
            final_image = final_image.convert("RGB")
            
            img_io = io.BytesIO()
            final_image.save(img_io, 'JPEG', quality=95)
            img_io.seek(0)
            
            st.success("تمت المعالجة بنجاح! 🎉")
            st.image(final_image, caption="الصورة النهائية للمعاملة", use_container_width=True)
            
            st.download_button(
                label="تحميل الصورة النهائية بجودة عالية",
                data=img_io,
                file_name="processed_id_photo.jpg",
                mime="image/jpeg",
                use_container_width=True
            )
