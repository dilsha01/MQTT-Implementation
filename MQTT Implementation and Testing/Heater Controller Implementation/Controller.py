import paho.mqtt.client as mqtt
import time

# MQTT server details
BROKER = "test.mosquitto.org"
PORT = 1883
PUBLISH_TOPIC = 'TemperatureCommands'
SUBSCRIBE_TOPIC = 'TemperatureStatus'
PUBLISH_QOS = 0
SUBSCRIBE_QOS = 0

# Callback function when a message is received
def on_message(client, userdata, message):
    received_msg = message.payload.decode()
    print(f"Status Update: {received_msg}")

# Initialize MQTT client
client = mqtt.Client()
client.on_message = on_message

# Connect to MQTT broker
client.connect(BROKER, PORT, 60)

# Subscribe to status updates
client.subscribe(SUBSCRIBE_TOPIC, SUBSCRIBE_QOS)
print(f"Subscribed to topic '{SUBSCRIBE_TOPIC}' for status updates")

def send_command(command):
    client.publish(PUBLISH_TOPIC, command, qos=PUBLISH_QOS)
    print(f"Sent command: {command}")

# Start the MQTT client loop
client.loop_start()

# Example interaction loop for sending commands
try:
    while True:
        print("\nCommand Center - Choose an action:")
        print("1. Set Temperature Threshold")
        print("2. Turn Heater ON")
        print("3. Turn Heater OFF")
        print("4. Request Status")
        choice = input("Enter choice: ")

        if choice == '1':
            threshold = input("Enter temperature threshold (°C): ")
            send_command(f"SET_THRESHOLD {threshold}")
        elif choice == '2':
            send_command("HEATER_ON")
        elif choice == '3':
            send_command("HEATER_OFF")
        elif choice == '4':
            send_command("STATUS_REQUEST")
        else:
            print("Invalid choice. Please try again.")

        time.sleep(1)  # Short delay between commands

except KeyboardInterrupt:
    print("Command Center stopped.")

# Stop the MQTT client loop
client.loop_stop()
