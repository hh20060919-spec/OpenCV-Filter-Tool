import streamlit as st
import cv2
import numpy as np
from PIL import Image

st.set_page_config(page_title="超級大的皮包", layout="wide")
st.title("🎨 超級大的皮包")

# --- 側邊欄控制區 ---
st.sidebar.header("🎛️ 影像控制面板")

# 1. 濾鏡模式選擇
filter_mode = st.sidebar.selectbox(
    "選擇濾鏡模式",
    ["浮雕立體 (Emboss)", "影像銳化 (Sharpen)", "邊緣偵測 (Edge Detection)", "高斯模糊 (Blur)"]
)

# 2. 強度調整滑桿
val = st.sidebar.slider("濾鏡影響強度", 1, 30, 10)

# 3. 亮度與對比度
brightness = st.sidebar.slider("亮度調整", -100, 100, 0)
contrast = st.sidebar.slider("對比度調整", 1.0, 3.0, 1.0)

# --- 濾鏡邏輯定義 ---
def get_kernel(mode, intensity):
    if mode == "浮雕立體 (Emboss)":
        return np.array([[-3, 0, 3], [-intensity, 0, intensity], [-3, 0, 3]], dtype=np.float32)
    elif mode == "影像銳化 (Sharpen)":
        return np.array([[0, -1, 0], [-1, 5+(intensity/10), -1], [0, -1, 0]], dtype=np.float32)
    elif mode == "邊緣偵測 (Edge Detection)":
        return np.array([[-1, -1, -1], [-1, intensity, -1], [-1, -1, -1]], dtype=np.float32)
    elif mode == "高斯模糊 (Blur)":
        size = (intensity // 5) * 2 + 1 # 確保是奇數
        return np.ones((size, size), np.float32) / (size * size)
    return None

# --- 主程式區 ---
uploaded_file = st.file_uploader("拖曳或選擇圖片...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # 讀取圖片
    image = Image.open(uploaded_file)
    img_array = np.array(image)
    img_cv = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)

    # A. 調整亮度與對比
    img_cv = cv2.convertScaleAbs(img_cv, alpha=contrast, beta=brightness)

    # B. 套用濾鏡
    kernel = get_kernel(filter_mode, val)
    delta_val = 128 if filter_mode == "浮雕立體 (Emboss)" else 0
    output_cv = cv2.filter2D(img_cv, -1, kernel, delta=delta_val)
    
    # 轉回 RGB 顯示
    output_rgb = cv2.cvtColor(output_cv, cv2.COLOR_BGR2RGB)

    # 顯示佈局
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("原始圖片")
        st.image(image, use_container_width=True)
    with col2:
        st.subheader(f"{filter_mode} 效果")
        st.image(output_rgb, use_container_width=True)

    # 下載按鈕
    st.sidebar.markdown("---")
    st.sidebar.download_button("💾 下載結果", data=uploaded_file, file_name="processed_image.png")
