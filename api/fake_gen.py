import pandas as pd
import numpy as np
from pymongo import MongoClient

# กำหนดจำนวนข้อมูล (30 วัน)
n_days = 30

# สร้างวันที่ (ย้อนหลัง 30 วันจากวันนี้) 
i = 50
dates = pd.date_range(end=pd.to_datetime('today'), periods=n_days, freq='D')

# สร้างค่า TDS (ค่าคุณภาพน้ำ) สมมุติเป็นตัวเลขสุ่มในช่วง 0-1000
TDS_values = np.round(np.random.uniform(50, 80, n_days), 2)

# สร้าง DataFrame
data = pd.DataFrame({
    'date': dates,
    'tds': TDS_values
})

# เชื่อมต่อ MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["water_quality"]
collection = db["tds_data"]

# แปลงข้อมูล DataFrame ให้เป็น dictionary เพื่อบันทึกลง MongoDB
data_dict = data.to_dict(orient="records")

# บันทึกข้อมูลลง MongoDB
collection.insert_many(data_dict)

# แสดงข้อมูลที่ถูกบันทึก
print("Data has been inserted into MongoDB.")
