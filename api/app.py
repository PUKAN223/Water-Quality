from flask import Flask, request, jsonify, send_file
from pymongo import MongoClient
import datetime
from flask_cors import CORS 
import pandas as pd
import matplotlib.pyplot as plt
from pymongo import MongoClient
from sklearn.linear_model import LinearRegression
import numpy as np
from matplotlib import font_manager

app = Flask(__name__)

CORS(app)

client = MongoClient("mongodb://localhost:27017/")
db = client["water_quality"]
collection = db["tds_data"]

# กำหนดฟอนต์ที่รองรับภาษาไทยเป็น Kanit ผ่าน font_manager
font_path = "./Kanit-Regular.ttf"  # ระบุพาธฟอนต์ที่ติดตั้ง
font_prop = font_manager.FontProperties(fname=font_path)

# เชื่อมต่อ MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["water_quality"]
collection = db["tds_data"]

def generate_water_quality_graphs():
    # ดึงข้อมูลจาก MongoDB
    data = list(collection.find({}, {"_id": 0, "date": 1, "tds": 1}).sort("date", 1))

    # ตรวจสอบว่ามีข้อมูลก่อนแปลงเป็น DataFrame
    if not data:
        print("No data found in MongoDB.")
        return

    df = pd.DataFrame(data)

    df['date'] = pd.to_datetime(df['date'])
    df.set_index('date', inplace=True)

    # คำนวณค่า Moving Average (30 วัน)
    df['TDS_MA'] = df['tds'].rolling(window=30, min_periods=1).mean()

    # Prepare data for linear regression
    X = np.array((df.index - df.index[0]).days).reshape(-1, 1)
    y = df['tds'].values

    model = LinearRegression()
    model.fit(X, y)

    # คาดการณ์ 10 วันข้างหน้า
    future_days = 10
    future_X = np.array(range(len(df), len(df) + future_days)).reshape(-1, 1)
    future_y = model.predict(future_X)

    future_dates = pd.date_range(start=df.index[-1] + pd.Timedelta(days=1), periods=future_days)

    # สร้างกราฟที่ 1
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

    # สร้างกราฟที่ 2
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



@app.route('/api/upload', methods=['POST'])
def upload_data():
    data = request.get_json()
    tds_value = data.get("tds")

    if tds_value is not None:
        document = {"date": datetime.datetime.utcnow(), "tds": tds_value}
        collection.insert_one(document)
        generate_water_quality_graphs()
        return jsonify({"message": "Data saved", "tds": tds_value}), 200
    return jsonify({"error": "Invalid data"}), 400

@app.route('/api/data', methods=['GET'])
def get_data():
    data = list(collection.find().sort("date", -1).limit(100))
    for item in data:
        item["_id"] = str(item["_id"])
    return jsonify(data)

@app.route('/api/latest', methods=['GET'])
def get_latest():
    item = collection.find_one(sort=[("date", -1)])
    if item:
        item["_id"] = str(item["_id"])
        return jsonify(item)
    return jsonify({"error": "No data found"}), 404

@app.route('/img1', methods=['GET'])
def get_image_1():
    return send_file('./water_quality_graph1.png', mimetype='image/png')

@app.route('/img2', methods=['GET'])
def get_image_2():
    return send_file('./water_quality_graph2.png', mimetype='image/png')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)