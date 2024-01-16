import mysql.connector
import json

class db:

    def __init__(self, user, host, password, database):
        try:
            self.db = mysql.connector.connect(user=user, host=host, password=password, database=database)
            self.cursor = self.db.cursor()
            print('[result] Database connected!')

        except Exception as e:
            print('[error] Error connecting to database!')
            print(e)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self):
        self.cursor.close()
        self.db.close()

    def user(self, username, api):
        try:
            query = "SELECT * FROM users WHERE username=%s AND api_key=%s"
            self.cursor.execute(query, (username, api))
            output = self.cursor.fetchall()
            return output[0]
        except Exception as e:
            print('[error] ' + str(e))

    def get_apikeys(self):
        query = 'SELECT api_key FROM users'
        self.cursor.execute(query)
        output = self.cursor.fetchall()
        return [api[0] for api in output]

    def add_user(self, username, password, first_name, last_name, email, phone_number, api_key):
        try:
            query = """
                INSERT INTO users (username, password, first_name, last_name, email, phone_number, last_login, api_key)
                VALUES (%s, %s, %s, %s, %s, %s, NOW(), %s)
            """
            self.cursor.execute(query, (username, password, first_name, last_name, email, phone_number, api_key))
            self.db.commit()
            return "success"
        except Exception as e:
            print(e)

    # def update_values(self, apikey, fieldname, deviceID, temp, humidity, moisture, light):
    #     try:
    #         # Check if API key exists
    #         apikeys = self.get_apikeys()
    #         if apikey not in apikeys:
    #             print("API key not found.")
    #             return

    #         # Insert data into the specified table
    #         query = f"""
    #             INSERT INTO {fieldname} (deviceID, temperature, humidity, moisture, light, date_time)
    #             VALUES (%s, %s, %s, %s, %s, NOW())
    #         """
    #         self.cursor.execute(query, (deviceID, temp, humidity, moisture, light))

    #         # Update the Node table
    #         query = f"""
    #             UPDATE Node
    #             SET temperature=%s, humidity=%s, moisture=%s, light=%s
    #             WHERE deviceID=%s
    #         """
    #         self.cursor.execute(query, (temp, humidity, moisture, light, deviceID))

    #         self.db.commit()
    #         return True

    #     except Exception as e:
    #         print(f"[ERROR!] {e}")


# # Example usage
# with db('aman', '192.168.56.102', 'hacker123', 'ARMS') as mydb:

#     # Get user data
#     user_data = mydb.user('nahidegi', '123456')
#     print(f"User data: {json.dumps(user_data)}")

#     # Add a new user
#     result = mydb.add_user('new_user', 'new_password', 'John', 'Doe', 'john.doe@example.com', '555-123-4567', 'abc123')
#     print(f"Add user result: {result}")

#     # Update values in the database
#     result = mydb.update_values('nahidegi', 'Rosegarden', 'ARMS12012', 10, 10, 10, 10)
#     print(f"Update values result: {result}")