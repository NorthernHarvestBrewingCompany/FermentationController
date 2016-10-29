#Simple Raspberry Pi Temprature Sensor Script

Be sure to install the below on your Pi before running the sensor python script
sudo apt-get install mysql-server mysql-client php5-mysql python-mysqldb

and setup your mySQL database as defined in the script. 


###### Some code snippets taken from the below sources
[Harry's Developer Blog](https://wingoodharry.wordpress.com/2015/01/05/raspberry-pi-temperature-sensor-web-server-part-2-setting-up-and-writing-to-a-mysql-database/)

[Building an SQLite temperature logger](http://raspberrywebserver.com/cgiscripting/rpi-temperature-logger/building-an-sqlite-temperature-logger.html)

## RPi Setup
Edit the /boot/config.txt file and add dtoverlay=w1-gpio
*sudo nano /boot/config.txt
*dtoverlay=w1-gpio

## Work in progress plans
- MQTT to publish temprature data to AWS IoT in real-time
- Migration or Replication of the local device MySQL DB to centralized Amazon Aurora DB
- TLS 1.2 support for MQTT Connection
- Multi-threaded Sensor Reading to utlize all 4 Raspberry Pi cores
- MQTT Subscribe intergration for responsive control & feedback
- Onboard PID controller to control actuated Glycol Valves
