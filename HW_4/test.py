from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)

# 連接 MongoDB 資料庫
client = MongoClient("mongodb://localhost:27017")
db = client["my_database"]
collection = db["my_collection"]

@app.route('/')
def index():
    # 獲取所有資料
    data = list(collection.find())
    return render_template('index.html', data=data)

@app.route('/add', methods=['POST'])
def add_data():
    # 從表單獲取新資料
    name = request.form['name']
    age = int(request.form['age'])
    collection.insert_one({"name": name, "age": age})
    return redirect(url_for('index'))

@app.route('/delete/<id>', methods=['POST'])
def delete_data(id):
    # 刪除指定資料
    collection.delete_one({"_id": ObjectId(id)})
    return redirect(url_for('index'))

@app.route('/edit/<id>', methods=['POST'])
def edit_data(id):
    # 更新資料
    name = request.form['name']
    age = int(request.form['age'])
    collection.update_one({"_id": ObjectId(id)}, {"$set": {"name": name, "age": age}})
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)