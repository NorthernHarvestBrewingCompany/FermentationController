#!/usr/bin/env python
import os
import time
import datetime
import glob
import MySQLdb
from time import strftime

#connect to the database
db_host="localhost"
db_user="root"
db_pass="password"
db_name='temp_db'



#Get a list of the currently connected thermomters
def get_devices():
    # search for a device file that starts with 28
    sensorlist = glob.glob('/sys/bus/w1/devices/28*')

    if sensorlist=='':
        print "ERROR: No Sensors Found"
        return None
    else:
        # append /w1slave to the device file
        for serialnum in sensorlist:
            print serialnum
            w1devicefile = serialnum + '/w1_slave'


#store the temperature in the database
def log_temperature(temp):
    db = MySQLdb.connect(host=db_host, user=db_user,passwd=db_pass, db=db_name)
    cur = db.cursor()
    
    datetimeWrite = (time.strftime("%Y-%m-%d ") + time.strftime("%H:%M:%S"))
    sql = ("""INSERT INTO tempLog (datetime,temperature) VALUES (%s,%s)""",(datetimeWrite,temp))
    try:
        #Execute the SQL command & commit changes
        cur.execute(*sql)
        db.commit()

    except:
        #Rollback in the case of an error
        db.rollback()
        print "ERROR: Unable to Write To Database"


# display the contents of the database
def display_data():
    db = MySQLdb.connect(host=db_host, user=db_user,passwd=db_pass, db=db_name)
    cur = db.cursor()

    for row in curs.execute("SELECT * FROM temps"):
        print str(row[0])+"	"+str(row[1])

    conn.close()


# returns None on error, or the temperature in C as a float
def get_temp(sensor_list):
    try:
        sensors = open(sensor_list, 'r')
        lines = sensors.readlines()
        sensors.close()
    except:
        return None

    temp_output = lines[1].find('t=')

    if temp_output != -1:
        temp_string = lines[1].strip()[temp_output+2:]
        temp_c = float(temp_string)/1000.0
    return round(temp_c,5)



# main function
# This is where the program starts
def main():

    # enable kernel modules
    os.system('sudo modprobe w1-gpio')
    os.system('sudo modprobe w1-therm')

    #Connect to the MySQL database for use inside the loops
    #function calls, the connection is not closed by the functions
    #directly and will need to be closed when the loop breaks
    db = MySQLdb.connect(host=db_host, user=db_user,passwd=db_pass, db=db_name)
    cur = db.cursor()

    #get a list of currently connected sensors
    sensor_list = get_devices()

    while True:
        # get the temperature from the device file
        temperature = get_temp(sensor_list)

        if temperature != None:
            print "temperature="+str(temperature)
        else:
            # Sometimes reads fail on the first attempt
            # so we need to retry
            temperature = get_temp(sensor_list)

            # Store the temperature in the database
        log_temperature(temperature)
            # display the contents of the database
            # display_data()
        time.sleep(60)


if __name__=="__main__":
    main()
