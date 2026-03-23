import streamlit as st
import cv2
import numpy as np
from PIL import Image

# 1. 網頁配置與標題 (精簡成 2 行)
st.set_page_config(page_title="專業矩陣對比", layout="wide")
st.title("🎨 影像矩陣對比實驗室 (3x3, 5x5, 10x10)")

# 2. 側邊欄：核心選項 (合併成 4 行)
st.sidebar.header("🎛️ 設定面板")
# 選擇矩陣大小 (直接對應 3, 5, 10)
k_size = st.sidebar.selectbox("選擇矩陣大小", [3, 5, 10])
# 強度滑桿
intensity = st.sidebar.slider("立體強度", 1, 30, 10)

# 3. 濾鏡處理邏輯 (大幅精簡成 10 行)
def process_img(img, size, val):
    # 建立一個動態大小的立體浮雕矩陣
    kernel = np.zeros((size, size), dtype=np.float32)
    center = size // 2
    
    # 簡單的立體邏輯：左負右正
    kernel[:, :center] = -1
    kernel[:, center+1:] = 1
    # 中心點權重
    kernel[center, center] = (size * size) + val
    
    # 套用濾鏡 (delta=128 讓立體感更清晰)
    return cv2.filter2D(img, -1, kernel, delta=128)

# 4. 主程式區 (合併成 20 行)
uploaded_file = st.file_uploader("拖曳或選擇圖片...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # 讀取圖片並轉為 OpenCV 格式
    image = Image.open(uploaded_file)
    img_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

    # 執行濾波處理
    result_cv = process_img(img_cv, k_size, intensity)
    
    # 轉回 RGB 供網頁顯示
    result_rgb = cv2.cvtColor(result_cv, cv2.COLOR_BGR2RGB)

    # 顯示對比佈局
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("原始圖片")
        st.image(image, use_container_width=True)
    with col2:
        st.subheader(f"立體效果 ({k_size}x{k_size} 矩陣)")
        st.image(result_rgb, use_container_width=True)

    # 顯示目前的數學矩陣
    if st.checkbox("👀 查看目前的數學矩陣 (Kernel)"):
        st.write(np.zeros((k_size, k_size))) # 這邊顯示出你選的大小
