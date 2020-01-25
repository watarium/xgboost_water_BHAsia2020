import re
from flask import Flask

app = Flask(__name__)

@app.route('/temperature')

def temperature():
    data = open("/sys/bus/w1/devices/28-01131b863d3e/w1_slave", "r")
    readdata= data.read()
    t = re.findall('t=.*', readdata)
    temperature = float(t[0].strip('t='))/1000
    data.close()
    return str(temperature)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)