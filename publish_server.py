import paho.mqtt.client as mqtt
import numpy as np
import time
import json

from random import uniform
from Pyfhel import Pyfhel


# Configuration
broker_address = "localhost"
broker_port = 1883

he = Pyfhel()
ckks_params = {
    'scheme': 'CKKS',   
    'n': 2**14,        
    'scale': 2**30,   
    'qi_sizes': [60, 30, 30, 30, 60] 
}
he.contextGen(**ckks_params)  
he.keyGen()   

client = mqtt.Client()
client.connect(broker_address, broker_port)

# Pyfhel Parameters
pyfhel_context = he.to_bytes_context()
pyfhel_public_key = he.to_bytes_public_key()


# Message Loop
while True:

    # Random Heart Rate is created and encrypted
    heart_rate = uniform(60.0, 150.0)
    heart_rate = he.encryptFrac(np.array([heart_rate], dtype = np.float64))

    # JSON doesn't accepy Bytes. Must decode to cp437 before sending.
    object_json = json.dumps({
        "Heart_Rate": heart_rate.to_bytes().decode('cp437'),
        "Pyfhel_Context": pyfhel_context.decode('cp437'),
        "Pyfhel_Public_Key": pyfhel_public_key.decode('cp437')
    })

    # Paho doesn't allow to pass dictionaries. Must use json to send structured data.
    client.publish("test/HeartRate", object_json)
    print("...Message Sent")
    time.sleep(2)