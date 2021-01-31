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
	t, times, avg, err, interfaceDict = initialize_data()
	while True:
		m = read_data_from_cmd()
		dttm = datetime.datetime.now()
        wifiData = []
        with open(filename, 'a') as f:
            filewriter = csv.writer(f, delimiter = ' ')
            filewriter.writerow(wifiData)
		dataArray.append(m)
		time.sleep(CONST_TIME_INTERVAL/CONST_NUM_SAMPLES)

def initialize_data():
	interfaceDict = dict()
	t = datetime.datetime.now()
	m = read_data_from_cmd()
	interfaceDict = sort_regex_results(m, interfaceDict)
	times = np.empty(shape=(0))
	avg = np.empty(shape=(len(interfaceDict), 0))
	err = np.empty(shape=(len(interfaceDict), 0))
	return t, times, avg, err, interfaceDict

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

def get_data(t, times, avg, err, interfaceDict):
	dataArray = []


	counts = np.zeros(len(interfaceDict))

	sortedData = []
	for i in range(0, len(interfaceDict)):
		sortedData.append([])

	if len(sortedData) != len(interfaceDict):
		raise Exception('data table and number of devices not in agreement')

	for dataTuples in dataArray:
		for data in dataTuples:
			switchResult = interfaceDict.get(data[0])
			#currentCount = counts[switchResult]
			sortedData[switchResult].append(data[1])
			counts[switchResult] += 1

	numArray = []
	for i in range(0, len(interfaceDict)):
		numArray.append([])

	index = 0
	for dataSet in sortedData:
		for sdata in dataSet:
			numArray[index].append(int(sdata))
		index += 1

	if platform.system() == 'Linux':
		measuringError = MEASURING_ERROR_LINUX
	elif platform.system() == 'Windows':
		measuringError = MEASURING_ERROR_WINDOWS
	else:
		raise Exception('reached else of if statement')

	index = 0
	avgCurrent = np.zeros((len(interfaceDict), 1))
	errCurrent = np.zeros((len(interfaceDict), 1))
	for numSet in numArray:
		avgCurrent[index] = np.mean(numSet)
		combinedErr = np.sqrt(np.std(numSet)**2 + measuringError**2)
		errCurrent[index] = combinedErr
		index += 1

	avg = np.append(avg, avgCurrent, axis=1)
	err = np.append(err, errCurrent, axis=1)

	times = np.append(times, elapsed)

	return times, avg, err, interfaceDict

def sort_regex_results(m, interfaceDict):
	#if type(m) is not list:
	#	raise Exception('not a list')
	for mTuple in m:
		if type(mTuple) is not tuple:
			raise Exception('not a tuple')
		if len(mTuple) != 2:
			raise Exception('number of regex matches not 2')
		if len(mTuple) % 2 != 0:
			# useful if the regex results for multiple interfaces is in a single tuple
			raise Exception('number of regex matches not divisible by 2')
		interfaceName = mTuple[0]
		if interfaceName not in interfaceDict:
			interfaceDict[interfaceName] = len(interfaceDict)

	return interfaceDict

if __name__ == "__main__":
	main()