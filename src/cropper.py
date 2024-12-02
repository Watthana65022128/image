import cv2
import numpy as np
import os

def crop_characters(image_path, output_dir):
    # อ่านรูปภาพ
    image = cv2.imread(image_path)
    
    # ตรวจสอบว่าอ่านรูปภาพสำเร็จหรือไม่
    if image is None:
        print(f"Error: Could not read image from {image_path}")
        return
        
    # แปลงเป็นภาพขาวดำ
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # สร้าง kernel สำหรับ morphological operations
    kernel = np.ones((5,5), np.uint8)
    
    # ทำให้ภาพชัดขึ้นโดยใช้ threshold
    _, threshold = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY_INV)
    
    # ใช้ morphological operations เพื่อลดสัญญาณรบกวน
    threshold = cv2.dilate(threshold, kernel, iterations=1)
    threshold = cv2.erode(threshold, kernel, iterations=1)
    
    # หา contours
    contours, _ = cv2.findContours(threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # สร้างโฟลเดอร์สำหรับเก็บผลลัพธ์
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # วนลูปผ่านแต่ละ contour
    for idx, contour in enumerate(contours):
        # หากพื้นที่ของ contour มีขนาดเหมาะสม
        area = cv2.contourArea(contour)
        if area > 100:  # ปรับค่าตามความเหมาะสม
            x, y, w, h = cv2.boundingRect(contour)
            
            # เพิ่มระยะขอบ
            padding = -5
            y_start = max(y - padding, -50)
            y_end = min(y + h + padding, image.shape[0])
            x_start = max(x - padding, -50)
            x_end = min(x + w + padding, image.shape[1])
            
            # ตัดภาพตามกรอบที่พบ
            char_image = image[y_start:y_end, x_start:x_end]
            
            # บันทึกไฟล์
            output_path = os.path.join(output_dir, f'char_{idx}.png')
            cv2.imwrite(output_path, char_image)
    
    print(f"Saved cropped images to {output_dir}")