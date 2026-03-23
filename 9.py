import streamlit as st
import cv2
import numpy as np
from PIL import Image

st.set_page_config(page_title="專業影像實驗室", layout="wide")
st.title("🎨 影像矩陣實驗室 (可選矩陣大小)")

# --- 側邊欄控制區 ---
st.sidebar.header("🎛️ 濾鏡參數設定")

# 1. 選擇矩陣大小 (Kernel Size)
k_size_str = st.sidebar.selectbox("選擇矩陣大小 (Kernel Size)", ["3x3", "5x5", "7x7", "9x9", "11x11"])
k_size = int(k_size_str.split('x')[0]) # 把 "3x3" 變成數字 3

# 2. 濾鏡模式選擇
filter_mode = st.sidebar.selectbox(
    "選擇濾鏡模式",
    ["浮雕立體 (Emboss)", "影像銳化 (Sharpen)", "邊緣偵測 (Edge Detection)", "高斯模糊 (Blur)"]
)

# 3. 強度調整滑桿
val = st.sidebar.slider("濾鏡強度 (Intensity)", 1, 30, 10)

# --- 動態矩陣邏輯 ---
def create_dynamic_kernel(mode, size, intensity):
    # 初始化一個全為 0 的矩陣
    kernel = np.zeros((size, size), dtype=np.float32)
    center = size // 2
    
    if mode == "浮雕立體 (Emboss)":
        # 簡單的立體邏輯：左負右正
        kernel[:, :center] = -1
        kernel[:, center+1:] = 1
        kernel[center, :] *= intensity
        return kernel
    
    elif mode == "影像銳化 (Sharpen)":
        kernel.fill(-1)
        # 中心點權重 = 矩陣總格數 + 強度
        kernel[center, center] = (size * size) + intensity
        return kernel
    
    elif mode == "邊緣偵測 (Edge Detection)":
        kernel.fill(-1)
        kernel[center, center] = (size * size) - 1 + intensity
        return kernel
    
    elif mode == "高斯模糊 (Blur)":
        return np.ones((size, size), np.float32) / (size * size)
    
    return None

# --- 主程式區 ---
uploaded_file = st.file_uploader("拖曳或選擇圖片...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    img_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

    # 執行濾波處理
    current_kernel = create_dynamic_kernel(filter_mode, k_size, val)
    
    # 浮雕模式通常需要灰色偏置 (delta) 比較好看
    delta_val = 128 if
