import pandas as pd
import matplotlib.pyplot as plt
from pymongo import MongoClient
from sklearn.linear_model import LinearRegression
import numpy as np
from matplotlib import font_manager

# กำหนดฟอนต์ที่รองรับภาษาไทยเป็น Kanit ผ่าน font_manager
font_path = "./Kanit-Regular.ttf"  # ระบุพาธฟอนต์ที่ติดตั้ง
font_prop = font_manager.FontProperties(fname=font_path)

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
    df = pd.DataFrame(data)

    df['date'] = pd.to_datetime(df['date'])
    df.set_index('date', inplace=True)

    df['TDS_MA'] = df['tds'].rolling(window=30, min_periods=1).mean()

    X = np.array((df.index - df.index[0]).days).reshape(-1, 1)
    y = df['tds'].values

    model = LinearRegression()
    model.fit(X, y)

    future_days = 10
    future_X = np.array(range(len(df), len(df) + future_days)).reshape(-1, 1)
    future_y = model.predict(future_X)

    future_dates = pd.date_range(start=df.index[-1] + pd.Timedelta(days=1), periods=future_days)

    plt.figure(figsize=(10, 5))
    plt.plot(df.index, df['tds'], label="TDS จริง", alpha=0.5)
    plt.plot(df.index, df['TDS_MA'], label="TDS Moving Average (30 วัน)", color='red')

    plt.legend(prop=font_prop)
    plt.xlabel("วันที่", fontproperties=font_prop)
    plt.ylabel("ค่า TDS (PPM)", fontproperties=font_prop)
    plt.title("กราฟ TDS จริงและค่าเฉลี่ยเคลื่อนที่", fontproperties=font_prop)
    plt.grid()
    plt.tight_layout()
    plt.savefig('water_quality_graph1.png', dpi=300)

    plt.figure(figsize=(10, 5))
    plt.plot(df.index, df['TDS_MA'], label="TDS Moving Average (30 วัน)", color='red')
    plt.plot(future_dates, future_y, label="การคาดการณ์ (10 วัน)", color='green', linestyle='--')

    plt.legend(prop=font_prop)
    plt.xlabel("วันที่", fontproperties=font_prop)
    plt.ylabel("ค่า TDS (PPM)", fontproperties=font_prop)
    plt.title("กราฟ TDS Moving Average และการคาดการณ์", fontproperties=font_prop)
    plt.grid()

    plt.tight_layout()
    plt.savefig('water_quality_graph2.png', dpi=300)
