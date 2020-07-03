#!/usr/bin/python
#encoding:utf-8
import Adafruit_DHT
import time
import RPi.GPIO as GPIO
from linkkit import linkkit

isConnect = False

# Set sensor type : Options are DHT11,DHT22 or AM2302
sensor = Adafruit_DHT.DHT11

# Set GPIO sensor is connected to
GPIO.setmode(GPIO.BCM)
GPIO.setup(17,GPIO.IN)
GPIO.setup(20,GPIO.IN)
GPIO.setup(26,GPIO.IN)
GPIO.setup(4,GPIO.IN) 
GPIO.setup(12, GPIO.OUT)  

def on_connect(session_flag, rc, userdata):
    print("on_connect:%d,rc:%d,userdata:" % (session_flag, rc))
    isConnect = True
    pass


def on_disconnect(rc, userdata):
    print("on_disconnect:rc:%d,userdata:" % rc)


def on_thing_prop_post(self, request_id, code, data, message, userdata):
    print("on_thing_prop_post request id:%s, code:%d, data:%s message:%s" %
          (request_id, code, str(data), message))


lk = linkkit.LinkKit(
    host_name="cn-shanghai",
    product_key="a19p1YLPpnV",
    device_name="rIOBSrQGXRnIQVfhoMD4",
    device_secret="nAZnLkF9m6RSt5n5mLJlRyZ36xn0yCwV")


	


lk.on_connect = on_connect
lk.on_disconnect = on_disconnect
lk.on_thing_prop_post = on_thing_prop_post
lk.thing_setup("tsl.json")
lk.connect_async()



while True:

    # Use read_retry method. This will retry up to 15 times to
    # get a sensor reading (waiting 2 seconds between each retry).
    humidity, temperature = Adafruit_DHT.read_retry(sensor, 17)
    if(temperature>28):
        for i in range(5):
            GPIO.output(12, GPIO.HIGH)  
            time.sleep(0.05)  
            GPIO.output(12, GPIO.LOW)
            time.sleep(0.5)  
    hw = GPIO.input(20)    
    yw = GPIO.input(4)
    gz = GPIO.input(26)
    # Reading the DHT11 is very sensitive to timings and occasionally
    # the Pi might fail to get a valid reading. So check if readings are valid.

    if humidity is not None and temperature is not None and hw is not None:
        print('Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(temperature, humidity))
	
        prop_data = {
            "CurrentTemperature":  round(temperature, 2),
            "CurrentHumidity":  round(humidity, 2),
	    "MotionAlarmState":  hw,
	    "SmokeSensorState":  yw,
	    "light":  gz
        }
        try:
            rc, request_id = lk.thing_post_property(prop_data)
            print(rc, request_id)
        except Exception as e:
            print('发生了异常：', e)
    else:
        print('Failed to get reading. Try again!')
    #GPIO.cleanup()
    time.sleep(1)
    