from sklearn.externals import joblib
import pandas as pd
import json
from flask import Flask, request

app = Flask(__name__)

@app.route('/preds', methods=['POST'])
def preds():
    regressor = joblib.load('water_supply.pkl')
    data = request.data.decode('utf-8')
    data = json.loads(data)

    hour = data['hour']
    temperature = data['temperature']

    input = pd.DataFrame([[hour, temperature]], columns=['hour', 'temperature'])

    result = regressor.predict(input)
    result = str(result[0])
    return result

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)