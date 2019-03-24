import paho.mqtt.client as mqtt
import time as timer1
import json
import csv
import ast
import pandas as pd
import os

new_path = "abcd.txt"
new_days = open(new_path, 'w')

count=0
name_array = {}
start_SSID_list = []

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("we")

def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))
    data_store_csv(msg.payload)


def data_store_csv(data1):
    # Define result array
    result = {"UoM_Wireless1": -100, "UoM_Wireless6": -100, "UoM_Wireless11": -100, "eduroam1": -100, "eduroam6": -100,
              "eduroam11": -100, "Jungle Book10": -100, "PROLINK_H5004NK_8766E11": -100, "UNIC-wifi11": -100}

    # Define csv file path
    filename = "wifi_data11.csv"

    try:
        # Get data as this format : {"id" : "1","UoM_Wireless1" : "-58","eduroam1" : "-89","UoM_Wireless1" : "-89","eduroam1" : "-57"}
        data = ast.literal_eval(data1.decode("utf-8"))
        print(data)

        for key, value in data.items():
            if key in result and result[key] == -100:
                result[key] = float(value)

        result["id"] = int(data["id"])

        # Create one row of csv file
        df = pd.Series(result).to_frame().T

        print(df)

        # Write to csv file
        df.to_csv(filename, index=False, mode='a', header=(not os.path.exists(filename)))

    except Exception as e:
        print(e)
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("iot.eclipse.org", 1883, 60)
client.loop_forever()