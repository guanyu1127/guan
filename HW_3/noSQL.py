from flask import Flask, request, render_template, redirect
from pymongo import MongoClient

# 初始化 Flask 應用程式
app = Flask(__name__)

# 連接 MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["mydatabase"]
collection = db["mycollection"]

# 首頁及表單頁面
@app.route("/")
def index():
    return render_template("index.html")

# 新增資料到 MongoDB
@app.route("/add_data", methods=["POST"])
def add_data():
    # 從表單中取得資料
    name = request.form.get("name")
    age = request.form.get("age")

    # 將資料新增至 MongoDB
    if name and age:
        data = {"name": name, "age": age}
        collection.insert_one(data)
        return redirect("/")

    return "請填寫完整的表單資訊", 400

if __name__ == "__main__":
    app.run(debug=True)
