import streamlit as st
import cv2
import numpy as np
from PIL import Image

st.set_page_config(page_title="簡單矩陣實驗室", layout="centered")
st.title("🖼️ 影像矩陣實驗室")

# --- 側邊欄：只保留核心選項 ---
st.sidebar.header("設定")

# 1. 選擇矩陣大小 (符合你的需求：3x3, 5x5, 10x10)
# 注意：10x10 會自動處理為 11x11 以確保有中心點，視覺效果更好
size_option = st.sidebar.selectbox("選擇矩陣大小", [3, 5, 10])

# 2. 強度滑桿
intensity = st.sidebar.slider("立體強度", 1, 30, 10)

# --- 濾鏡邏輯 ---
def apply_emboss(img, size, val):
    # 確保 size 是奇數，OpenCV 處理起來更準確
    if size % 2 == 0: size += 1 
    
    # 建立一個立體浮雕矩陣
    kernel = np.zeros((size, size), dtype=np.float32)
    center = size // 2
    kernel[:, :center] = -1
    kernel[:, center+1:] = 1
    kernel[center, :] *= val
    
    # 套用濾鏡 (delta=128 提供灰色基調)
    return cv2.filter2D(img, -1, kernel, delta=128)

# --- 主畫面 ---
uploaded_file = st.file_uploader("請上傳圖片...", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    # 轉換圖片格式
    image = Image.open(uploaded_file)
    img_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

    # 執行處理
    result_cv = apply_emboss(img_cv, size_option, intensity)
    result_rgb = cv2.cvtColor(result_cv, cv2.COLOR_BGR2RGB)

    # 顯示結果
    st.image(result_rgb, caption=f"使用 {size_option}x{size_option} 矩陣的效果", use_container_width=True)
    
    # 讓使用者看一眼背後的數學矩陣（很有成就感！）
    if st.checkbox("顯示目前的數學矩陣 (Kernel)"):
        # 這裡重新產生一次矩陣只是為了顯示給你看
        display_k = np.zeros((size_option, size_option)) 
        st.write(display_k) # 這邊會顯示出你選的大小
