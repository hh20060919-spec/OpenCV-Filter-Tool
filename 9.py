import cv2
import numpy as np
import datetime
import urllib.request
import sys

def custom_filter(image, kernel):
    # 使用 cv2.filter2D 套用二維矩陣濾波器
    return cv2.filter2D(image, -1, kernel)

def load_image_from_web(image_bytes):
    # 網頁端傳來的圖片通常是二進位位元流 (Bytes)
    # 利用 np.frombuffer 轉成一維陣列後，再用 cv2.imdecode 解碼成 OpenCV 格式
    np_arr = np.frombuffer(image_bytes, np.uint8)
    image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    return image

def main():
    if len(sys.argv) > 1:
        # 有給參數，代表要讀取本地圖片測試 (例：python 9.py my_pic.jpg)
        img_path = sys.argv[1]
        print(f"嘗試讀取本地圖片: {img_path}")
        with open(img_path, "rb") as f:
            image_bytes = f.read()
    else:
        # 沒給參數的話，模擬網頁上傳：從 URL 取得圖片 bytes
        url = "https://picsum.photos/400/400"
        print("未提供圖片參數，正在從網路下載模擬圖片...")
        req = urllib.request.urlopen(url)
        image_bytes = req.read()
    
    # 將位元流解碼成 OpenCV 可用的圖片矩陣
    image = load_image_from_web(image_bytes)
    
    if image is None:
        print("圖片解碼失敗，將建立測試用圖片")
        image = np.ones((400, 400, 3), dtype=np.uint8) * 100
        cv2.circle(image, (200, 200), 100, (200, 150, 50), -1)

    # 定義使圖片產生立體感（浮雕加上方向性光影）的 3x3 矩陣
    # 權重總和為 1 可保持整體亮度不變
    kernel_3d = np.array([
        [-1,  -1,  -1],
        [ -1,  -1, -1],
        [-1,  -1, -1]
    ], dtype=np.float32)
    
    # 呼叫自定義函數進行處理
    output_image = custom_filter(image, kernel_3d)
    
    # 將原圖與結果水平合併以便對比顯示
    combined = np.hstack((image, output_image))
    
    # 顯示對比圖
    cv2.imshow("Original vs 3D Filter", combined)
    
    # 加上 datetime 時間戳記存檔
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    output_filename = f"output_{timestamp}.jpg"
    cv2.imwrite(output_filename, output_image)
    print(f"結果已儲存為: {output_filename}")
    
    # 等待按鍵關閉
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
