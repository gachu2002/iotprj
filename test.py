import person

# Replace 'your_username' and 'your_password' with the actual username and password
username = 'amansingh'
password = 'password here'

# Create an instance of the user class
user_instance = person.user(username, password)

# Authenticate the user if necessary (this step depends on your implementation)
# For example, if there's a method to authenticate, you might call it like this:
# user_instance.authenticate()

# Now, assuming the user is authenticated, print out the device list
device_list = user_instance.get_devices()
print(user_instance.devices)