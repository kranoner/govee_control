import requests
import argparse
import urllib.parse

URL = "https://developer-api.govee.com"
URL_DEVICES = URL + "/v1/devices"
URL_DEVICES_CONTROL = URL + "/v1/devices/control"
URL_DEVICES_STATE = URL_DEVICES + "/state?device=%s&model=%s"

## return a command object to send to lamp
## options are 
## turn value on / off
## set brightness 0 - 100
## set color in hexadecimal
def build_command(action, brightness=0, color=None, kelvin=None):
    if action == 'on':
        return {'name': 'turn', 'value': 'on'}
    elif action == 'off':
        return {'name': 'turn', 'value': 'off'}
    elif action == 'brighten' or action == 'dim':
        if brightness < 0 or brightness > 100:
            raise ValueError('Brightness must be between 0 and 100')
        return {'name': 'brightness', 'value': brightness}
    elif action == 'set_color':  # hue only for now
        rgb = hex_to_rgb(color)
        return  {'name': 'color', 'value': {'r': rgb[0], 'g': rgb[1], 'b': rgb[2]}}
    elif action == 'setKelvin':  # hue only for now
        return  {'name': 'colorTem', 'value': kelvin}
    else:
        raise ValueError('Invalid action')

def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

# Control a Govee smart lamp using the API. 
# The function allows you to set various parameters such as the trigger state (on/off), brightness, color, and Kelvin temperature.
# Parameters:
#   api_key: A string representing your Govee API key.
#   device_mac: A string representing the MAC address of the device.
#   device_model: A string representing the model of the device.
#   trigger: A string indicating the desired state ('on' or 'off'). If None, no trigger action will be performed.
#   brightness: An integer representing the brightness level (0-100). If None, no brightness change will occur.
#   color: A string representing the color in hexadecimal format (e.g., "#FFFFFF"). If None, no color change will occur.
#   kelvin: An integer representing the temperature in Kelvin (2700-6500). If None, no temperature change will occur.
def control_lamp(api_key, device_mac, device_model, trigger, brightness, color, kelvin):
    header = {'Govee-API-Key': api_key,
               'Content-Type': "application/json", 'Accept': "application/json"}
    
    lamp_trigger_request_body = {}

    lamp_trigger_request_body['model'] = device_model
    lamp_trigger_request_body['device'] =device_mac

    print (trigger)
    #switch on off
    if trigger != None and (trigger == 'on' or trigger == "off") :
        lamp_trigger_request_body['cmd'] = build_command(action=trigger)
    elif trigger != None:
        print("Invalid state. Please use 'on' or 'off'.")
        return

    if brightness:
        lamp_trigger_request_body['cmd'] = build_command(action = 'brighten', brightness=brightness)
    if color:
        lamp_trigger_request_body['cmd'] = build_command(action='set_color', color=color)
    if kelvin:
        lamp_trigger_request_body['cmd'] = build_command(action='setKelvin', kelvin=kelvin)
    print (lamp_trigger_request_body)

    #send request
    response = requests.put(URL_DEVICES_CONTROL, headers=header, json=lamp_trigger_request_body)

    print(response.content)

# Fetches the current power state of a Govee device.
# Parameters:
#   api_key (str): The API key for authentication with the Govee API.
#   device_mac (str): The MAC address of the device, formatted as 'XX:XX:XX:XX:XX:XX'. This function automatically removes the colons when making the request.
#   device_model (str): The model number or identifier of the Govee device.
# Returns:
#   A string indicating the power state of the device, either 'on' or 'off'.
# Raises:
# requests.exceptions.RequestException: If an error occurs during the HTTP request to the Govee API.
def get_state (api_key, device_mac, device_model):
    header = {'Govee-API-Key': api_key,
               'Content-Type': "application/json", 'Accept': "application/json"}

    url = URL_DEVICES_STATE % (urllib.parse.quote(device_mac.replace(":", "")), device_model) 

    response = requests.get(URL_DEVICES_STATE % (device_mac, device_model) , headers=header)
    resp_json = response.json()

    power_state = resp_json['data']['properties'][1]['powerState']
    return power_state

# Gets a list of devices associated with the given API key.
# Parameters: 
#   api_key: The API key to use for authentication.
# Returns:
#    A list of dictionaries containing information about each device.
def get_devices(api_key):
    header = {'Govee-API-Key': api_key,
               'Content-Type': "application/json", 'Accept': "application/json"}
    url = URL_DEVICES
    response = requests.get(URL_DEVICES, headers=header)
    resp_json = response.json()
    return (resp_json)

# This function prints the devices in a JSON response.
# Parameters:
#     devices_json_resp (dict): A dictionary containing the devices information. 
# Returns:
#     None
def print_devices_model (devices_json_resp):
    for device in devices_json_resp['data']['devices']:
        mac_address = device['device']
        model_name = device.get('model', '')
        device_name = device['deviceName']

        print("MAC Address: ", mac_address)
        print("Model Name: ", model_name)
        print("Device Name: ", device_name)
        print("---------------")

# control_lamp is a Python script that allows you to control your Govee lamp devices using the Govee API. 
# The script provides a simple interface for triggering actions on your devices and setting brightness, color, and kelvin values.
### Arguments:
# -h, --help: show this help message and exit.
# -a API_KEY, --api-key API_KEY: Govee API key.
# -d DEVICE_MAC, --device-mac DEVICE_MAC: Device MAC address.
# -m MODEL, --model MODEL: Device model.
# -t TRIGGER, --trigger TRIGGER: Trigger action: on / off.
# -b BRIGHTNESS, --brightness BRIGHTNESS: Brightness value (0-100).
# -c COLOR, --color COLOR: Color in RGB in hexadecimal.
# -k KELVIN, --kelvin KELVIN: kelvin: An integer representing the temperature in Kelvin (2700-6500).
if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("-a", "--api-key", required=True, help="Govee API key")
    parser.add_argument("-d", "--device-mac", required=False, help="Device MAC address")
    parser.add_argument("-m", "--model", required=False, help="Device model")
    parser.add_argument("-t", "--trigger", required=False, help="Trigger action: on / off")
    parser.add_argument("-b", "--brightness", required=False, type=int, help="Brightness value (0-100)")
    parser.add_argument('-c', '--color', required=False, type=str, help='Color in RGB in hexadecimal')
    parser.add_argument('-k', '--kelvin', required=False, type=int, help='Color in RGB in hexadecimal')
    
    args = parser.parse_args()
    if args.device_mac :
        control_lamp(args.api_key, args.device_mac, args.model, args.trigger, args.brightness, args.color, args.kelvin)
    else: 
        print_devices_model(get_devices(args.api_key))