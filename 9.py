import streamlit as st
import cv2
import numpy as np
from PIL import Image

# 1. 頁面基本配置
st.set_page_config(page_title="超級大的皮包", layout="wide")
st.title("🎨 超級大的皮包")

# 2. 側邊欄設定 (合併選項)
st.sidebar.header("🎛️ 參數設定")
k_size = st.sidebar.selectbox("選擇矩陣大小", [3, 5, 10])
mode = st.sidebar.selectbox("模式", ["浮雕 (Emboss)", "銳化 (Sharpen)", "模糊 (Blur)"])
intensity = st.sidebar.slider("強度", 1, 30, 10)

# 3. 核心濾鏡運算函數
def apply_filter(img, size, val, mode):
    # 初始化矩陣與中心點
    kernel = np.zeros((size, size), dtype=np.float32)
    center = size // 2
    delta = 0

    if mode == "浮雕 (Emboss)":
        kernel[:, :center], kernel[:, center+1:] = -1, 1
        kernel[center, :] *= val
        delta = 128
    elif mode == "銳化 (Sharpen)":
        kernel.fill(-1)
        kernel[center, center] = (size * size) + val
    elif mode == "模糊 (Blur)":
        kernel = np.ones((size, size), np.float32) / (size * size)

    return cv2.filter2D(img, -1, kernel, delta=delta), kernel

# 4. 主程式與檔案處理
up_file = st.file_uploader("選擇圖片...", type=["jpg", "png", "jpeg"])

if up_file:
    # 格式轉換
    img_pil = Image.open(up_file)
    img_cv = cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)

    # 運算結果
    res_cv, current_k = apply_filter(img_cv, k_size, intensity, mode)
    res_rgb = cv2.cvtColor(res_cv, cv2.COLOR_BGR2RGB)

    # 並排顯示原圖與結果
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("原始圖片")
        st.image(img_pil, use_container_width=True)
    with c2:
        st.subheader(f"{mode} 效果 ({k_size}x{k_size})")
        st.image(res_rgb, use_container_width=True)

    # 數值呈現
    with st.expander("👀 查看矩陣數值"):
        st.write(current_k)
