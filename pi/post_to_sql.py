
import requests
import time
import datetime
import numpy as np

CONST_TIME_INTERVAL = 10

def main():

    temp = 22

    url='https://vegbot.io/api/writedata.php?loc=3&temp='+str(temp)+'&humidity=99'

    response = requests.request(
    method='POST',
    url=url)

    r = response.status_code
    print(r)

    time.sleep(60)

if __name__ == "__main__":
    main()