
from flask import Flask, request, jsonify, render_template, redirect, url_for
import mysql.connector

app = Flask(__name__)

# Database configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'danny811432',
    'database': 'guan'
}

# Establish a database connection
def get_db_connection():
    connection = mysql.connector.connect(**db_config)
    return connection

# Route to render the HTML page
@app.route('/')
def index():
    return render_template('index.html')

# Route to fetch data from the database
@app.route('/data', methods=['GET'])
def get_data():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users")
    results = cursor.fetchall()
    cursor.close()
    connection.close()
    return jsonify(results)

# Route to handle form submission and insert data into the database
@app.route('/add', methods=['POST'])
def add_data():
    name = request.form.get('name')
    age = request.form.get('age')

    connection = get_db_connection()
    cursor = connection.cursor()
    query = "INSERT INTO users (name, age) VALUES (%s, %s)"
    cursor.execute(query, (name, age))
    connection.commit()
    cursor.close()
    connection.close()
    return redirect(url_for('index'))

# Update functionality with improved error handling
@app.route('/update', methods=['POST'])
def update_data():
    data = request.json
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        update_query = "UPDATE users SET name = %s, age = %s WHERE id = %s"
        cursor.execute(update_query, (data['name'], data['age'], data['id']))
        conn.commit()
        message = {'message': 'Data updated successfully!'}
    except mysql.connector.Error as err:
        message = {'error': f"Error updating data: {err}"}
    finally:
        cursor.close()
        conn.close()

    return jsonify(message)

# Delete functionality with improved error handling
@app.route('/delete', methods=['POST'])
def delete_data():
    data = request.json
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        delete_query = "DELETE FROM users WHERE id IN (%s)" % ','.join(['%s'] * len(data['ids']))
        cursor.execute(delete_query, tuple(data['ids']))
        conn.commit()
        message = {'message': 'Selected data deleted successfully!'}
    except mysql.connector.Error as err:
        message = {'error': f"Error deleting data: {err}"}
    finally:
        cursor.close()
        conn.close()

    return jsonify(message)

if __name__ == '__main__':
    app.run(debug=True)
