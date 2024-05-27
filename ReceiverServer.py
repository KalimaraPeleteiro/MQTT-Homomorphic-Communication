import paho.mqtt.client as mqtt

# Define broker connection parameters
broker_address = "localhost"
broker_port = 1883

# Define topic to subscribe to
topic = "test/topic"

# Create MQTT client instance
client = mqtt.Client()

# Define callback function for incoming messages
def on_message(client, userdata, message):
    print(f"Received message: '{message.payload.decode('utf-8')}' from topic '{message.topic}'")

# Connect to the broker and subscribe to the topic
client.connect(broker_address, broker_port)
client.subscribe(topic, qos=0)

# Set callback function for incoming messages
client.on_message = on_message

# Start the message loop to process incoming messages
client.loop_forever()
