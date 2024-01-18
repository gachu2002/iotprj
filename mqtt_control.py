from flask import Flask
from flask_mqtt import Mqtt
import json

app = Flask(__name__)
app.config['MQTT_BROKER_URL'] = 'broker.hivemq.com'
app.config['MQTT_BROKER_PORT'] = 1883
app.config['MQTT_REFRESH_TIME'] = 0.5
mqtt = Mqtt(app)
led_data = {
        "deviceId": "led0",
        "deviceType": "led",
        "status": "off"
    }
def on_message(client, userdata, message):
    print(f"Received message on topic {message.topic}: {message.payload}")
    payload = json.loads(message.payload)
    
    # Add your logic here to handle the received message

@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    mqtt.subscribe('device')

@mqtt.on_message()
def handle_message(client, userdata, message):
    # Modify this section to publish the desired data format
    if(led_data['status'] == "off"):
        led_data['status'] = "on"
    elif (led_data['status'] == "on"):
        led_data['status'] = "off"
    mqtt.publish('command', json.dumps(led_data))
