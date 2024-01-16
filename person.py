from database import db
import hashlib
from passlib.hash import sha512_crypt as sha
from datetime import datetime

class user:

    def __init__(self, username, password):
        self.db = db('root', 'localhost', 'Love123bgbg@', 'ARMS')
        self.username = username 
        self.secret = password
        self.authenticated = False
        self.auth()
        self.get_details()
        self.get_devices()
        
    def auth (self):
        #this is the place where user will get authenticated
        try:
            query = 'select password from users where username = "{0}"'.format(self.username)
            self.db.cursor.execute(query)
            output = self.db.cursor.fetchall()
            if self.secret == output[0][0]:
                self.authenticated = True
                
                query = 'update users set last_login = now() where username = "{0}";'.format(self.username)
                self.db.cursor.execute(query)
                self.db.db.commit()

                return True
            else:
                self.authenticated = False
                return False

        except Exception as e:
            print("[ERROR!]")
            print(e)

    def get_details (self):
        
        try:
            if self.authenticated:
                query = 'select * from users where username = "{0}"'.format(self.username)
                self.db.cursor.execute(query)
                output = self.db.cursor.fetchall()
                output = output[0]
                self.first = output[2]
                self.last = output[3]
                self.email = output[4]
                self.phone = output[5]
                self.last_login = output[6].strftime("%d-%b-%Y (%H:%M:%S.%f)")
                self.api = output[7]
                return True

            else:
                print("User not logged in!")
                return False

        except Exception as e:
            print("ERROR!")
            print(e)
    
    def get_devices(self):
        devices = []
        try:
            if self.authenticated:
                query = 'select * from devices where username = "{0}" and register = "yes"'.format(self.username)
                self.db.cursor.execute(query)
                output = self.db.cursor.fetchall()
                devices = []  # Initialize an empty list to store device dictionaries
                for dev in output:
                    deviceID, username, device_type, device_value, register = dev
                    device_info = {
                        "deviceID": deviceID,
                        "username": self.username,
                        "device_type": device_type,
                        "device_value": device_value,
                        "register": register
                    }
                    devices.append(device_info)  # Append the dictionary to the list
                return devices
            else:
                return False

        except Exception as e:
            print("[Error!]")
            print (e)
            
    def get_device_by_id(self, device_id):
        """
        Fetch a device's information from the database by its ID.

        :param device_id: The unique identifier of the device.
        :return: A dictionary containing the device's information or None if not found.
        """
        try:
            if self.authenticated:
                # Assuming self.db.cursor is the database cursor object
                query = 'SELECT * FROM devices WHERE deviceID = %s AND username = %s;'
                self.db.cursor.execute(query, (device_id,self.username))
                device = self.db.cursor.fetchone()

                if device:
                    # Assuming the device information is returned as a tuple, convert it to a dictionary
                    device_info = {
                        'deviceID': device[0],
                        'username': device[1],
                        'device_type': device[2],
                        'device_value': device[3],
                        'register': device[4]
                        # Add other fields as necessary
                    }
                    return device_info
                else:
                    print(f"No device found with ID: {device_id}")
                    return None
            else:
                print("User not authenticated.")
                return None

        except Exception as e:
            print("[Error in get_device_by_id]")
            print(e)
            return None
        
    def get_addable_device(self):
        devices = []
        try:
            if self.authenticated:
                query = 'select * from devices where username = "{0}" and register = "no"'.format(self.username)
                self.db.cursor.execute(query)
                output = self.db.cursor.fetchall()
                devices = []  # Initialize an empty list to store device dictionaries
                for dev in output:
                    deviceID, username, device_type, device_value, register = dev
                    device_info = {
                        "deviceID": deviceID,
                        "username": self.username,
                        "device_type": device_type,
                        "device_value": device_value,
                        "register": register
                    }
                    devices.append(device_info)  # Append the dictionary to the list
                return devices
            else:
                return False

        except Exception as e:
            print("[Error!]")
            print (e)
    
    def check_device_exists(self, device_id):
        try:
            if self.authenticated:
                query = 'SELECT COUNT(*) FROM devices WHERE deviceID = %s AND username = %s;'
                self.db.cursor.execute(query, (device_id, self.username))
                count = self.db.cursor.fetchone()[0]

                if count > 0:
                    return True
                else:
                    return False
            else:
                print("User not authenticated.")
                return False
        except Exception as e:
            print("[Error in check_device_exists]")
            print(e)
            return False

        
    def add_device(self, deviceID, device_type, device_value):
        if not self.authenticated:
            print("User must be authenticated to add a device.")
            return False

        try:
            # Assuming 'Node' is your device table and it has columns for deviceID, deviceName, deviceType, and username
            query = """
                    INSERT INTO devices
                    (deviceID, username, device_type, device_value, register)
                    values (%s,%s,%s,%s,%s);
                """
            self.db.cursor.execute(query, (deviceID, self.username, device_type, device_value, 'yes'))
            self.db.db.commit()
            return True
        except Exception as e:
            print("[Error!] Could not add device.")
            print(e)
            return False
        
    def enable_device(self, deviceID):
        if not self.authenticated:
            print("User must be authenticated to add a device.")
            return False

        try:
            # Assuming 'Node' is your device table and it has columns for deviceID, deviceName, deviceType, and username
            query = """
                    UPDATE devices
                    SET register = 'yes'
                    WHERE deviceID = %s AND username = %s
                """
            self.db.cursor.execute(query, (deviceID, self.username))
            self.db.db.commit()
            return True
        except Exception as e:
            print("[Error!] Could not add device.")
            print(e)
            return False
            
    def update_device_info(self, deviceID, device_type, device_value, register):
        """
        Update the device information in the devices table.

        :param deviceID: The ID of the device to update.
        :param device_type: The new type of the device.
        :param device_value: The new value of the device.
        :return: True if the update was successful, False otherwise.
        """
        try:
            if self.authenticated:
                # Prepare the SQL query to update the device information
                query = """
                    UPDATE devices
                    SET device_type = %s, device_value = %s, register = %s
                    WHERE deviceID = %s AND username = %ss
                """
                # Execute the query with the provided parameters
                self.db.cursor.execute(query, (device_type, device_value, register, deviceID, self.username))
                # Commit the changes to the database
                self.db.commit()
                print(f"Device {deviceID} updated successfully.")
                return True
            else:
                print("User not logged in!")
                return False
        except Exception as e:
            print("[ERROR!]")
            print(e)
            return False

    def disable_device(self, deviceID):
        try:
            if self.authenticated:
                query = """
                    UPDATE devices
                    SET register = 'no'
                    WHERE deviceID = %s AND username = %s
                """
                self.db.cursor.execute(query, (deviceID, self.username))
                self.db.db.commit()
                return True, "Device deleted successfully"
            else:
                return False, "User not authenticated"
        except Exception as e:
            print("[Error!]", e)
            return False, "An error occurred while deleting the device"

    # def dev_info(self, deviceID):
    #     try:
            
    #         if self.authenticated:
    #             self.db.db.commit()
    #             query = 'select * from Node where deviceID="{0}";'.format(deviceID)
    #             self.db.cursor.execute(query)
    #             output = self.db.cursor.fetchall()
    #             print(output)
    #             return output[0]
    #         else:
    #             return False

    #     except Exception as e:
    #         print('[ERROR!]')
    #         print(e)
    
    # def field_values(self, fieldname):
    #     #here we will access all the values of devices according to time
    #     try:
    #         if self.authenticated:
    #             query = 'select * from (select * from {0} order by date_time desc limit 10) dummy order by date_time asc;'.format(fieldname)
    #             self.db.cursor.execute(query)
    #             output = self.db.cursor.fetchall()
    #             return output
    #         else:
    #             return False
    #     except Exception as e:
    #         print('[ERROR!]')
    #         print(e)

    # def device_values(self, fieldname, deviceID):
    #     try:
    #         if self.authenticated:
    #             query = 'select * from (select * from (select * from {0} where deviceID = "{1}") var1 order by date_time desc limit 10) dummy order by date_time asc;'.format(fieldname, deviceID)
    #             self.db.cursor.execute(query)
    #             output = self.db.cursor.fetchall()
    #             # print(output)
    #             return output
    #         else:
    #             return False

    #     except Exception as e:
    #         print('[ERROR!]')
    #         print(e)

#testing side for the class
test = user("amansingh", "password here")
test.get_details()
print(test.get_devices())
print(test.get_addable_device())
# print(test.dev_info("ARMS1112"))
# print(test.field_values('Rosegarden'))
# print(test.device_values("Rosegarden", "ARMS12012"))