# Read and save wifi signal strength
# Downloaded from https://github.com/s7jones/Wifi-Signal-Plotter/blob/master/WifiSignalPlotter.py
# To install libraries at the command line:
# pip3 install matplotlib

import subprocess
import re
import time
import datetime
import platform
import csv
import numpy as np

CONST_TIME_INTERVAL = 10
CONST_NUM_SAMPLES = 100
MEASURING_ERROR_LINUX = 0.5
MEASURING_ERROR_WINDOWS = 0.5


def main():
    while True:
        m = read_data_from_cmd()
        dttm = datetime.datetime.now()
        signal = m[0][1]
        with open('WifiData.csv', 'a') as f:
            filewriter = csv.writer(f, delimiter = ' ')
            filewriter.writerow([signal, dttm])
        time.sleep(5)


def read_data_from_cmd():
    if platform.system() == 'Linux':
        p = subprocess.Popen("iwconfig", stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    elif platform.system() == 'Windows':
        p = subprocess.Popen("netsh wlan show interfaces", stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    else:
        raise Exception('Could not read platform')
    out = p.stdout.read().decode()

    if platform.system() == 'Linux':
        m = re.findall('(wlan[0-9]+).*?Signal level=(-[0-9]+) dBm', out, re.DOTALL)
    elif platform.system() == 'Windows':
        m = re.findall('Name.*?:.*?([A-z0-9 ]*).*?Signal.*?:.*?([0-9]*)%', out, re.DOTALL)
    else:
        raise Exception('Could not find wifi data')

    p.communicate()

    return m



if __name__ == "__main__":
    main()