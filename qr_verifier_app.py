import streamlit as st
from PIL import Image
import numpy as np
import cv2
import io

st.set_page_config(page_title="QR Code Authenticity Checker", layout="centered")

# Watermark pattern
secret_pattern = [
    [1, 0, 1],
    [0, 1, 0],
    [1, 0, 1]
]

def verify_watermark(img, pattern, start_pos):
    arr = np.array(img.convert("RGB"))
    for i in range(len(pattern)):
        for j in range(len(pattern[0])):
            y = start_pos[1] + i
            x = start_pos[0] + j
            if y < arr.shape[0] and x < arr.shape[1]:
                pixel = arr[y, x]
                is_black = all(v < 50 for v in pixel)
                if pattern[i][j] != int(is_black):
                    return False
            else:
                return False
    return True

def process_qr_image(file):
    img = Image.open(file).convert("RGB")
    img_cv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    detector = cv2.QRCodeDetector()
    data, _, _ = detector.detectAndDecode(img_cv)
    qr_data = data if data else "Unreadable"

    width, height = img.size
    start_pos = (width - 10, height - 10)
    is_authentic = verify_watermark(img, secret_pattern, start_pos)

    return {
        "qr_data": qr_data,
        "authenticity": "✅ AUTHENTIC" if is_authentic else "❌ COUNTERFEIT",
        "watermark": "Matched" if is_authentic else "Not Matched"
    }

st.title("🔍 QR Code Authenticity Verifier")

uploaded_file = st.file_uploader("Upload a QR Code Image", type=["png", "jpg", "jpeg"])

uploaded_file = st.file_uploader("Upload a QR Code Image", type=["png", "jpg", "jpeg"])

if uploaded_file:
    st.image(uploaded_file, caption="Uploaded QR Image", use_container_width=True)
    result = process_qr_image(uploaded_file)
    st.markdown("---")
    st.write(f"**QR Data:** {result['qr_data']}")
    st.write(f"**Watermark:** {result['watermark']}")
    st.write(f"**Final Result:** {result['authenticity']}")


