import os
from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient

app = Flask(__name__)

MONGO_URI = os.environ.get("MONGO_URI", "mongodb://admin:mongo@mongo:27017/")
DB_NAME = os.environ.get("DB_NAME", "ipa2026_db")

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
routers_col = db["routers"]
status_col = db["router_status"]

@app.route('/')
def index():
    data = list(routers_col.find())
    return render_template('index.html', data=data)

@app.route('/add', methods=['POST'])
def add_router():
    ip = request.form.get('ip')
    username = request.form.get('username')
    password = request.form.get('password')

    if ip and username and password:
        routers_col.insert_one({
            "ip": ip,
            "username": username,
            "password": password
        })
    return redirect(url_for('index'))

@app.route('/delete', methods=['POST'])
def delete_comment():
    idx = int(request.form.get('idx'))
    routers = list(routers_col.find())
    if 0 <= idx < len(routers):
        target_id = routers[idx]['_id']
        routers_col.delete_one({'_id': target_id})
    return redirect(url_for('index'))

# --- ส่วนที่เพิ่มเข้ามาใหม่ ---
@app.route('/router/<ip>')
def router_detail(ip):
    # ดึงข้อมูล Interface Status ล่าสุด 3 ครั้ง ของ IP นั้นๆ
    # เรียงจาก Timestamp ล่าสุด (sort -1) และดึงมาแค่ 3 รายการล่าสุด (limit 3)
    status_records = list(status_col.find({"ip": ip}).sort("timestamp", -1).limit(3))
    
    return render_template('router_detail.html', ip=ip, status_records=status_records)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
