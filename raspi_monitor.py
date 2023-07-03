print("Hello World")
import pyembedded
from pyembedded.raspberry_pi_tools.raspberrypi import PI
import paho.mqtt.publish as publish
import paho.mqtt.client as mqtt
import time
import json
import os

# get node name this script runs on
hostname = os.environ["NODE_NAME"]
# hostname = 'node4'
mqtt_broker = 'mosquitto-1687368643' # Mosquitto broker HostName is the kubernetes service name : mosquitto-1687368643, Port: 1883
mqtt_port: 1883

# mqtt_port: 31500
pi = PI()

def get_data():
    
    # Get parameters(cpu, ram, disk, temp) from raspberry via pymbedded
    ram_raw = pi.get_ram_info()
    disk_raw = pi.get_disk_space()
    cpu_raw = pi.get_cpu_usage()
    temperatur_raw=pi.get_cpu_temp()

    # Create dicts/json objects
    temperature = {
        "name": "temperature",
        "value": temperatur_raw,
        "unit": "°C",
        "node": hostname
    }
    ram = {
        "name": "ram",
        "value": {
            "total": round(int(ram_raw[0])/1000000,1),
            "used": round(int(ram_raw[1])/1000000,1),
            "free": round(int(ram_raw[2])/1000000,1),
        },
        "unit": "GB",
        "node": hostname
    }
    disk = {
        "name": "disk",
        "value": {
            "total": disk_raw[0],
            "used": disk_raw[1],
            "free": disk_raw[2],
        },
        "unit": "GB",
        "node": hostname
    }
    cpu = {
        "name": "cpu",
        "value": cpu_raw,
        "unit": "Percent",
        "node": hostname
    }
    print("-----------------------------------")
    print("Node: ", hostname)
    print("temperature: ",temperature)
    print("ram: ",ram)
    print("disk: ",disk)
    print("cpu: ",cpu)

    return temperature, ram, disk, cpu
#---------------------------------------------------------

# Connect to the MQTT Broker
mqtt_client = mqtt.Client('raspberry_monitor')
mqtt_client.connect(mqtt_broker, mqtt_port, 60)   
mqtt_client.loop_start()

while True:
    temperature, ram, disk, cpu = get_data()
    print("temperature: ", temperature)
    print("ram: ", ram)
    print("disk: ", disk)
    print("cpu: ", cpu)
    
    # Publish to MQTT broker
    mqtt_client.publish("raspi/" + hostname + "/temperature", str(temperature))
    mqtt_client.publish("raspi/" + hostname + "/ram" , json.dumps(ram))
    mqtt_client.publish("raspi/" + hostname + "/disk", json.dumps(disk))
    mqtt_client.publish("raspi/" + hostname + "/cpu" , json.dumps(cpu))
    
    time.sleep(5) # sleep for 5 seconds before next call