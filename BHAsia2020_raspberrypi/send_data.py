from pymodbus.client.sync import ModbusTcpClient
from datetime import datetime
import requests, json, re, pprint

controller_address = '10.0.1.10'
# If you use modify from http to https.
result_collector = 'http://www.watarunrun.com:5000/result'

def get_temperature():
    data = open('/sys/bus/w1/devices/28-01131b863d3e/w1_slave', 'r')
    readdata= data.read()
    t = re.findall('t=.*', readdata)
    temperature = float(t[0].strip('t='))/1000
    data.close()
    return str(temperature)

def get_water_level():
    client = ModbusTcpClient(controller_address, port=502)
    # client.connect()
    # Rr = client.read_holding_registers(address=0, count=1, unit=1)
    # PV = float(Rr.registers[0])
    PV = 50
    return PV

def send_data():
    hour = int(datetime.now().strftime('%-H'))
    temperature = get_temperature()
    water_level = get_water_level()
    print('Data to be submitted. \nhour: ' + str(hour) + ', temperature: ' + str(temperature) + ', water: ' + str(water_level) + '\n')

    response = requests.post(result_collector,
        json.dumps({'hour': hour, 'temperature': temperature, 'water': water_level}),
        headers={'Content-Type': 'application/json'}, verify=False)
    # If you use https and ignore certification verify, remove comment out below.
    # response = requests.post(result_collector,
    #     json.dumps({'hour': hour, 'temperature': temperature, 'water': water_level}),
    #     headers={'Content-Type': 'application/json'}, verify=False)
    print(response.text.decode('utf-8'))

if __name__ == '__main__':
    send_data()