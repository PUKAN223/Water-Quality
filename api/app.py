from flask import Flask, request, jsonify
from pymongo import MongoClient
import datetime

app = Flask(__name__)

# เชื่อมต่อ MongoDB
client = MongoClient("mongodb://localhost:27017/")  # เปลี่ยนเป็น URL ของ MongoDB Atlas หากใช้ Cloud
db = client["water_quality"]
collection = db["tds_data"]

# ฟังก์ชันบันทึกข้อมูลลง MongoDB
def save_data(tds_value):
    collection.insert_one({
        "date": datetime.datetime.utcnow(),
        "tds": tds_value
    })

# API รับค่าจาก ESP32
@app.route('/api/upload', methods=['POST'])
def upload_data():
    data = request.get_json()
    tds_value = data.get("tds")

    if tds_value is not None:
        save_data(tds_value)
        return jsonify({"message": "Data saved", "tds": tds_value}), 200
    return jsonify({"error": "Invalid data"}), 400

# API ส่งข้อมูลไปยัง Frontend
@app.route('/api/data', methods=['GET'])
def get_data():
    data = list(collection.find().sort("date", -1).limit(100))
    for item in data:
        item["_id"] = str(item["_id"])  # แปลง ObjectId เป็น string
    return jsonify(data)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
