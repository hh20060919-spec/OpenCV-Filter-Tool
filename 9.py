import streamlit as st
import cv2
import numpy as np
from PIL import Image

st.set_page_config(page_title="OpenCV 立體濾鏡工具")
st.title("🎨 影像立體濾鏡工具")
st.write("上傳一張圖片，我們會套用自定義的 3D 矩陣讓它產生立體感！")

# 側邊欄：讓使用者調整矩陣數值
st.sidebar.header("調整濾波器矩陣")
val = st.sidebar.slider("邊緣強度", 1, 20, 10)

# 定義 3x3 矩陣 (使用你之前的 Sobel 變體)
kernel = np.array([
    [-3,  0,  3],
    [-val, 0, val],
    [-3,  0,  3]
], dtype=np.float32)

# 上傳檔案元件
uploaded_file = st.file_uploader("請選擇圖片...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # 讀取圖片並轉為 OpenCV 格式
    image = Image.open(uploaded_file)
    img_array = np.array(image)
    img_cv = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)

    # 執行濾波處理 (加上 delta=128 讓立體感更清晰)
    output_cv = cv2.filter2D(img_cv, -1, kernel, delta=128)
    
    # 轉回 RGB 供網頁顯示
    output_rgb = cv2.cvtColor(output_cv, cv2.COLOR_BGR2RGB)

    # 顯示結果
    col1, col2 = st.columns(2)
    with col1:
        st.header("原圖")
        st.image(image, use_container_width=True)
    with col2:
        st.header("立體效果")
        st.image(output_rgb, use_container_width=True)

    # 下載按鈕
    result_img = Image.fromarray(output_rgb)
    st.download_button("下載處理後的圖片", data=uploaded_file, file_name="output.png")
