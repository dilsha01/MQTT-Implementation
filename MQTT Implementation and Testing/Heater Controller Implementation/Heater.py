import paho.mqtt.client as mqtt
import time

# MQTT server details
BROKER = "test.mosquitto.org"
PORT = 1883
PUBLISH_TOPIC = 'TemperatureStatus'
SUBSCRIBE_TOPIC = 'TemperatureCommands'
PUBLISH_QOS = 0
SUBSCRIBE_QOS = 0

# State variables
heater_status = "OFF"
temperature_threshold = None
temperature = 25  # Dummy current temperature

# Callback function when a message is received
def on_message(client, userdata, message):
    global heater_status, temperature_threshold

    received_msg = message.payload.decode()
    print(f"Received command: {received_msg}")

    # Parse and execute the received command
    if received_msg.startswith("SET_THRESHOLD"):
        _, threshold_str = received_msg.split()
        temperature_threshold = float(threshold_str)
        print(f"Temperature threshold set to {temperature_threshold}°C")
    elif received_msg == "HEATER_ON":
        heater_status = "ON"
        print("Heater turned ON")
        send_status(client)
    elif received_msg == "HEATER_OFF":
        heater_status = "OFF"
        print("Heater turned OFF")
        send_status(client)
    elif received_msg == "STATUS_REQUEST":
        send_status(client)

# Callback function when a message is published
def on_publish(client, userdata, mid):
    print(f"Status message {mid} published.")

# Function to send the current status
def send_status(client):
    status_msg = f"STATUS Heater: {heater_status}, Threshold: {temperature_threshold}, Current Temp: {temperature}"
    client.publish(PUBLISH_TOPIC, status_msg, qos=PUBLISH_QOS)
    print(f"Sent status: {status_msg}")

# Function to handle heating logic
def check_temperature(client):
    global heater_status
    if temperature_threshold is not None:
        if temperature < temperature_threshold and heater_status == "OFF":
            heater_status = "ON"
            client.publish(PUBLISH_TOPIC, "Heater ON", qos=PUBLISH_QOS)
            print(f"Temperature below threshold. Heater turned ON.")
            send_status(client)
        elif temperature >= temperature_threshold and heater_status == "ON":
            heater_status = "OFF"
            client.publish(PUBLISH_TOPIC, "Heater OFF", qos=PUBLISH_QOS)
            print(f"Temperature above threshold. Heater turned OFF.")
            send_status(client)

# Initialize MQTT client
client = mqtt.Client()
client.on_message = on_message
client.on_publish = on_publish

# Connect to MQTT broker
client.connect(BROKER, PORT, 60)

# Subscribe to command topic
client.subscribe(SUBSCRIBE_TOPIC, SUBSCRIBE_QOS)
print(f"Subscribed to topic '{SUBSCRIBE_TOPIC}' for commands")

# Start the MQTT client loop
client.loop_start()

# Main loop for checking temperature and updating status
try:
    while True:
        check_temperature(client)
        time.sleep(1)  # Check every second

except KeyboardInterrupt:
    print("Temperature Controller stopped.")

# Stop the MQTT client loop
client.loop_stop()
