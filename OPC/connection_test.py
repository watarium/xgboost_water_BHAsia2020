from pymodbus.client.sync import ModbusTcpClient
from datetime import datetime
import requests, time, json

thermometer_url = 'http://192.168.2.119:5000/temperature'
ai_url = 'http://www.watarunrun.com:5001/preds'
controller_address = '10.0.1.10'

def prediction():
    hour = int(datetime.now().strftime('%-H'))
    temperature = float(requests.get(thermometer_url).text)
    water_level = requests.post(ai_url,
                             json.dumps({'hour': hour, 'temperature': temperature}),
                             headers={'Content-Type': 'application/json'}, verify=False)
    return water_level

def control(water_level):
    client = ModbusTcpClient(controller_address, port=502)
    client.connect()

    result = client.read_coils(1,1)
    print('Manual or Auto: ' + str(result.bits[0]))


    result = client.read_coils(5,1)
    print('Plus/Minus sign: ' + str(result.bits[0]))

    Rr = client.read_holding_registers(address=0,count=1,unit=1)
    PV = float(Rr.registers[0])
    print('PV(mm) = %f' % PV)

    client.write_register(address=1,value=water_level,unit=1)

    client.write_register(address=11,value=2000,unit=1)
    client.write_register(address=12,value=0,unit=1)

    time.sleep(1)

    # Read Value
    SVr = client.read_holding_registers(address=1,count=1,unit=1)
    SV= float(SVr.registers[0])
    print('SV(%%) = %f' % SV)

    RHr = client.read_holding_registers(address=11,count=1,unit=1)
    RH = float(RHr.registers[0])
    print('RH(mm) = %f' % RH)

    RLr = client.read_holding_registers(address=12,count=1,unit=1)
    RL = float(RLr.registers[0])
    print('RL(mm) = %f' % RL)

if __name__ == '__main__':
    water_level = prediction()
    print(water_level)
    control(water_level)