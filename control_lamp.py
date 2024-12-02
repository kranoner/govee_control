import requests
import argparse
import urllib.parse


URL = "https://developer-api.govee.com"
URL_DEVICES = URL + "/v1/devices"
URL_DEVICES_CONTROL = URL + "/v1/devices/control"
URL_DEVICES_STATE = URL_DEVICES + "/state?device=%s&model=%s"


def send_command_to_lamp(api_key, device_mac, device_model, cmd):
    header = {'Govee-API-Key': api_key, 'Content-Type': "application/json", 'Accept': "application/json"}
    lamp_trigger_request_body = {'device': device_mac,'model': device_model}
    lamp_trigger_request_body['cmd'] = cmd

## return a cmd to send to lamp
## options are 
## turn value on / off
## set brightness 0 - 100
## set color 0 - 360
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


def get_state (api_key, device_mac, device_model):
    header = {'Govee-API-Key': api_key,
               'Content-Type': "application/json", 'Accept': "application/json"}

    url = URL_DEVICES_STATE % (urllib.parse.quote(device_mac.replace(":", "")), device_model) 

    response = requests.get(URL_DEVICES_STATE % (device_mac, device_model) , headers=header)
    resp_json = response.json()

    power_state = resp_json['data']['properties'][1]['powerState']
    return power_state


def change_brightness(api_key, device_mac, device_model, brightness):
    header = {'Govee-API-Key': api_key,
                'Content-Type': "application/json", 'Accept': "application/json"}

    
def get_devices(api_key):
    header = {'Govee-API-Key': api_key,
               'Content-Type': "application/json", 'Accept': "application/json"}
    url = URL_DEVICES
    response = requests.get(URL_DEVICES, headers=header)
    resp_json = response.json()
    return (resp_json)

def print_devices_model (devices_json_resp):
    for device in devices_json_resp['data']['devices']:
        mac_address = device['device']
        model_name = device.get('model', '')
        device_name = device['deviceName']

        print("MAC Address: ", mac_address)
        print("Model Name: ", model_name)
        print("Device Name: ", device_name)
        print("---------------")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    #group = parser.add_mutually_exclusive_group(required=True)

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