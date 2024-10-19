import mysql.connector

# Database configuration
db_config = {
   'host': 'localhost',
    'user': 'root',
    'password': 'danny811432',
    'database': 'guan'
}

# Function to fetch data across all three tables using JOIN
def fetch_all_user_data():
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor(dictionary=True)
    
    query = """
        SELECT users.id, users.name, users.age, user_info.workplace, user_info.education, 
               user_details.country, user_details.interests
        FROM users
        LEFT JOIN user_info ON users.id = user_info.id
        LEFT JOIN user_details ON users.id = user_details.id
    """
    
    cursor.execute(query)
    result = cursor.fetchall()
    
    cursor.close()
    connection.close()
    
    return result

# Example usage of fetch_all_user_data
if __name__ == "__main__":
    data = fetch_all_user_data()
    for row in data:
        print(row)
