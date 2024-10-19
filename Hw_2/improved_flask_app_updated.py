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

# Route to fetch data from the database using JOIN across users, user_info, and user_details
@app.route('/data', methods=['GET'])
def get_data():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    query = """
        SELECT users.id, users.name, users.age, user_info.workplace, user_info.education, 
               user_details.country, user_details.interests
        FROM users
        LEFT JOIN user_info ON users.id = user_info.id
        LEFT JOIN user_details ON users.id = user_details.id
    """
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    connection.close()
    return jsonify(results)

# Route to handle form submission and insert data into the three tables
@app.route('/add', methods=['POST'])
def add_data():
    name = request.form.get('name')
    age = request.form.get('age')
    workplace = request.form.get('workplace')
    education = request.form.get('education')
    country = request.form.get('country')
    interests = request.form.get('interests')

    connection = get_db_connection()
    cursor = connection.cursor()

    # Insert into users table
    insert_user_query = "INSERT INTO users (name, age) VALUES (%s, %s)"
    cursor.execute(insert_user_query, (name, age))
    user_id = cursor.lastrowid

    # Insert into user_info table
    insert_user_info_query = "INSERT INTO user_info (id, workplace, education) VALUES (%s, %s, %s)"
    cursor.execute(insert_user_info_query, (user_id, workplace, education))

    # Insert into user_details table
    insert_user_details_query = "INSERT INTO user_details (id, country, interests) VALUES (%s, %s, %s)"
    cursor.execute(insert_user_details_query, (user_id, country, interests))

    connection.commit()
    cursor.close()
    connection.close()

    return redirect(url_for('index'))

# Update functionality across all three tables
@app.route('/update', methods=['POST'])
def update_data():
    data = request.json
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Update users table
        update_user_query = "UPDATE users SET name = %s, age = %s WHERE id = %s"
        cursor.execute(update_user_query, (data['name'], data['age'], data['id']))

        # Update user_info table
        update_user_info_query = "UPDATE user_info SET workplace = %s, education = %s WHERE id = %s"
        cursor.execute(update_user_info_query, (data['workplace'], data['education'], data['id']))

        # Update user_details table
        update_user_details_query = "UPDATE user_details SET country = %s, interests = %s WHERE id = %s"
        cursor.execute(update_user_details_query, (data['country'], data['interests'], data['id']))

        conn.commit()
        message = {'message': 'Data updated successfully!'}
    except mysql.connector.Error as err:
        message = {'error': f"Error updating data: {err}"}
    finally:
        cursor.close()
        conn.close()

    return jsonify(message)

# Delete functionality across all three tables
@app.route('/delete', methods=['POST'])
def delete_data():
    data = request.json
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Delete from user_details and user_info first due to foreign key constraints
        delete_user_details_query = "DELETE FROM user_details WHERE id IN (%s)" % ','.join(['%s'] * len(data['ids']))
        cursor.execute(delete_user_details_query, tuple(data['ids']))

        delete_user_info_query = "DELETE FROM user_info WHERE id IN (%s)" % ','.join(['%s'] * len(data['ids']))
        cursor.execute(delete_user_info_query, tuple(data['ids']))

        # Delete from users table
        delete_user_query = "DELETE FROM users WHERE id IN (%s)" % ','.join(['%s'] * len(data['ids']))
        cursor.execute(delete_user_query, tuple(data['ids']))

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
