Govee controller
====

## Introduction
Controller written in pyhton to control your govee lamp using the public api provided by Govee. Documentation available at: 
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

Instruction to get an API key are available from the govee website: https://developer.govee.com/reference/apply-you-govee-api-key

Once your API key received, you can get your device(s) mac address and model by running the script as follows:

`python3 control_lamp.py -a <your api key>`


## Quick how to
To control you device run the script as in the examples:

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
