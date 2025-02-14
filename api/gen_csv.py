import pandas as pd
from pymongo import MongoClient

# เชื่อมต่อ MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["water_quality"]
collection = db["tds_data"]

# ดึงข้อมูลจาก MongoDB
data = list(collection.find({}, {"_id": 0, "date": 1, "tds": 1}).sort("date", 1))

# ตรวจสอบว่ามีข้อมูลก่อนแปลงเป็น DataFrame
if not data:
    print("No data found in MongoDB.")
else:
    # แปลงข้อมูลเป็น DataFrame
    df = pd.DataFrame(data)

    # บันทึกข้อมูลเป็น CSV
    df.to_csv('water_quality_data.csv', index=False)  # index=False เพื่อไม่ให้เขียนหมายเลข index ของ pandas
    print("CSV file created successfully.")
