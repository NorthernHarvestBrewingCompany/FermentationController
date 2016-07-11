#!/usr/bin/env python
import os
import time
import datetime
import glob
import MySQLdb
from time import strftime

#connect to the database
def db_connect():
    db_host="localhost"
    db_user="root"
    db_pass="password"
    db_name='temp_db'

    db = MySQLdb.connect(host=db_host, user=db_user,passwd=db_password, db=db_name)
    cur = db.cursor()

#Get a list of the currently connected thermomters
def get_devices():
    # search for a device file that starts with 28
    devicelist = glob.glob('/sys/bus/w1/devices/28*')
    if devicelist=='':
        return None
    else:
        # append /w1slave to the device file
        w1devicefile = devicelist[0] + '/w1_slave'


#store the temperature in the database
def log_temperature(temp):
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
    db_connect()

    for row in curs.execute("SELECT * FROM temps"):
        print str(row[0])+"	"+str(row[1])

    conn.close()


# get temerature
# returns None on error, or the temperature as a float
def get_temp(devicefile):

    try:
        fileobj = open(devicefile,'r')
        lines = fileobj.readlines()
        fileobj.close()
    except:
        return None

    # get the status from the end of line 1
    status = lines[0][-4:-1]

    # is the status is ok, get the temperature from line 2
    if status=="YES":
        temp_output = lines[1].find('t=')
        if temp_output != -1:
            temp_str = lines[1].strip()[temp_output+2:]
            temp_c = float(temp_str)/1000.0
        return round(temp_c,4)


        print status
        tempstr= lines[1][-6:-1]
        tempvalue=float(tempstr)/1000
        print tempvalue
        return tempvalue
    else:
        print "There was an error."
        return None



# main function
# This is where the program starts
def main():

    # enable kernel modules
    os.system('sudo modprobe w1-gpio')
    os.system('sudo modprobe w1-therm')

    #Connect to the MySQL database for use inside the loops
    #function calls, the connection is not closed by the functions
    #directly and will need to be closed when the loop breaks
    db_connect()

    #get a list of currently connected sensors
    sensors = get_devices()

while True:
    # get the temperature from the device file
    temperature = get_temp(sensors)
    if temperature != None:
        print "temperature="+str(temperature)
    else:
        # Sometimes reads fail on the first attempt
        # so we need to retry
        temperature = get_temp(sensors)
        print "temperature="+str(temperature)

        # Store the temperature in the database
    log_temperature(temperature)
        # display the contents of the database
        # display_data()

        time.sleep(60)


if __name__=="__main__":
    main()
