import requests
import board
import adafruit_dht
import time
import datetime

MAX_TEMP = 25
MIN_TEMP = 20



dhtDevice = adafruit_dht.DHT22(board.D4, use_pulseio=False)

def main():

    temperature = 22 #dhtDevice.temperature

    print(temperature)

    if temperature > MAX_TEMP:

        response = requests.request(
        method='POST',
        url='https://maker.ifttt.com/trigger/turn_off_heat_mat/with/key/FVAsbOvb-3AFltHMc_hEp')

        r = response.status_code

        if r != 200:
            raise Exception('could not post to ifttt')
        else:
            print('Max temp reached - turned mat off')

    elif temperature < MIN_TEMP:

        response = requests.request(
        method='POST',
        url='https://maker.ifttt.com/trigger/turn_on_heat_mat/with/key/FVAsbOvb-3AFltHMc_hEp')

        if response.status_code != 200:
            raise Exception('could not post to ifttt')
            print(response.status_code)
        else:
            print('Min temp reached - turned mat on')

    time.sleep(60)

if __name__ == "__main__":
    main()