# import the required packages

import time
from pprint import pprint

import RPi.GPIO as GPIO
import requests

# setup the proper raspberry pi board channel
GPIO.setmode(GPIO.BCM)

# initialize the sensor pins

"""
    Gas Sensor is the white cable
    Vibration Sensor is the black cable
    Ground is the grey cable
"""

gas_sensor = 27
GPIO.setup(gas_sensor, GPIO.IN)
vibration_sensor = 22
GPIO.setup(vibration_sensor, GPIO.IN)

# Here is the micro-controller code url
api_url = 'http://gidisecure.herokuapp.com/readings/'

# Set the delay interval
delay_interval = 3


# dummy locations


# Some Helper functions
def convert(x):
    """converts 0 to 1 and 1 to 0
    """
    if x == 0:
        return 1
    if x == 1:
        return 0


def time_stamp():
    time_format = time.strftime('%H:%M:%S')
    date = time.strftime('%d/%m/%Y')
    return (time_format, date)


def get_sensor_data():
    """returns a tuple containing the sensor_states (gas_sensor, vibration_sensor)
        the tuple value is (1, 0) when the sensor is activated and the vibration sensor is
        dormant. the tuple value is (0, 1) when the vibration sensor is activated and the gas sensor is dormant.
        the tuple value is (1, 1) when both sensors is activate
    """
    gas_sensor_value = convert(GPIO.input(gas_sensor))
    vibration_sensor_value = convert(GPIO.input(vibration_sensor))
    time_returned, date = time_stamp()
    return (gas_sensor_value, vibration_sensor_value, time_returned, date)


def main():
    while True:
        try:
            data = dict()
            gas_sensor_value, vibration_sensor_value, time_returned, date = get_sensor_data()

            if gas_sensor_value or vibration_sensor_value:

                if gas_sensor_value and not vibration_sensor_value:
                    print("There is a gas leakage at your house")
                elif vibration_sensor_value and not gas_sensor_value:
                    print("There is an intrusion at your house")
                elif vibration_sensor_value and gas_sensor_value:
                    print("There is an intrusion and also a gas leakage at your house")

                data = {

                    "gas_sensor": gas_sensor_value,
                    "vibration_sensor": vibration_sensor_value,
                    "time_stamp": time_returned,
                    "date_stamp": date,
                }
                # insert record
                resp = requests.post(api_url, data)
                print(resp)
                pprint(data)

                time.sleep(15)  # wait an extra 7 seconds"


            else:
                print("Everything is fine!")
                print("............")


        except Exception as e:
            data["error"] = e
            print("There was an error: the exception is {}".format(e))

        time.sleep(delay_interval)


if __name__ == '__main__':

    time.sleep(60)
    main()
