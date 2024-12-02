Govee controller
====

## Introduction
Govee controller is a Python script that allows you to control your Govee lamp devices using the Govee API. 
The script provides a simple interface for triggering actions on your devices and setting brightness, color, and kelvin values.
Controller written in python to control your Govee lamp using the public api provided by Govee. Documentation available at: 
https://govee-public.s3.amazonaws.com/developer-docs/GoveeDeveloperAPIReference.pdf

## Requirements
### Libraries
The module calls standard Python libraries: 
 - requests
 - argparse
 - urllib.parse 

### API key and devices
To control your lamp you will need:
 - an API key
 - the MAC address of your device
 - the model id of your device

* The script uses the Govee API to interact with your devices. You need to obtain an API key from the Govee website and insert it into the script using the `-a` flag. Instruction to get an API key are available from the govee website: https://developer.govee.com/reference/apply-you-govee-api-key
* If you don't know your device MAC address, you can use the script `python3 control_lamp.py -a <your api key>` to retrieve a list of all your devices and their associated MAC addresses.


## Quick how to

* The `-m` flag is used to specify the model number of your device.
* The `-t` flag is used to trigger an action on your device: you can set it to `on` or `off` to turn your device on/off, or use `brightness`, `color`, and `kelvin` flags to adjust the brightness, color, and kelvin values of your device.
* The `-b`, `-c`, and `-k` flags are used to set the brightness, color, and kelvin values of your device respectively.

Some examples:

>Turn on your device:
>
>`python3 control_lamp.py  -a $api_key -d $mac_device -m $model -t on`

> Set the brightness to 30
>
> `python3 control_lamp.py  -a $api_key -d $mac_device -m $model -b30`

> Change color to red:
>
> `python3 control_lamp.py  -a $api_key -d $mac_device -m $model -c "##FF0000"`

> Turn off your device:
>
>`python3 control_lamp.py  -a $api_key -d $mac_device -m $model -t off`




### Notes:
