#Libraries
import Adafruit_DHT as dht
from time import sleep

#Set DATA pin
DHT = 4
print(DHT)
while True:
    #Read Temp and Hum from DHT22
    h,t = dht.read_retry(dht.DHT22, DHT)
    print(h)
    print(t)
    #Print Temperature and Humidity on Shell window
    print('Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(t,h))
    sleep(5) #Wait 5 seconds and read again