import paho.mqtt.client as mqtt
import numpy as np
import json
import csv

from Pyfhel import Pyfhel, PyCtxt

def on_message(client, userdata, message):
    global buffer
    
    data = json.loads(message.payload)

    # Reconstruindo as Configurações
    he = Pyfhel()
    he.from_bytes_context(data["Pyfhel_Context"].encode("cp437"))
    he.from_bytes_public_key(data["Pyfhel_Public_Key"].encode("cp437"))

    # Convertendo valor para Bits e Adicionando
    value = PyCtxt(pyfhel = he, bytestring = data["Heart_Rate"].encode("cp437"))
    buffer.append(value)

    if len(buffer) < 3:
        print(f"Message Received. Buffer Length: {len(buffer)}")
    
    # Após 03 envios, cálculo de média e limpar o buffer.
    if len(buffer) == 3:    
        value1, value2, value3 = buffer[0], buffer[1], buffer[2]
        divisor = he.encryptFrac(np.array([1/3],dtype=np.float64))
        mean = (value1 + value2 + value3) * divisor

        data = [list(he.decryptFrac(value1))[0], list(he.decryptFrac(value2))[0], 
                list(he.decryptFrac(value3))[0], list(he.decryptFrac(mean))[0]]

        with open("result.csv", "a", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(data)

        print("03 Values in Buffer. Computing Mean value...")
        print("Cleaning Buffer...")
        buffer = []


if __name__ == "__main__":
    broker_address = "localhost"
    broker_port = 1883

    client = mqtt.Client()

    buffer = []

    client.connect(broker_address, broker_port)
    client.subscribe("test/HeartRate", qos=0)

    client.on_message = on_message

    client.loop_forever()
