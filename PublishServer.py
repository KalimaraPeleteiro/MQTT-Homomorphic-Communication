import paho.mqtt.client as mqtt

# Define broker connection parameters
broker_address = "localhost"
broker_port = 1883

# Define topic to publish messages
topic = "test/topic"

# Create MQTT client instance
client = mqtt.Client()

# Connect to the broker
client.connect(broker_address, broker_port)

# Send messages to the topic
while True:
    message = input("Enter message to publish: ")
    client.publish(topic, message)
    print(f"Message '{message}' published to topic '{topic}'")
