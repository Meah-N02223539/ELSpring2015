#!/usr/bin/python
import os
import time
import sys
import sqlite3 as mydb
"""Log Current Time, Temperature in Celsius and Fahrenheit
    Returns a list of values [time,tempC,tempF] to the next row of a
    known table in a database"""

def readTemp():
    tempfile = open("/sys/bus/w1/devices/28-000006961c7b/w1_slave")
    tempfile_text = tempfile.read()
    currentTime = time.strftime('%x %X %Z')
    tempfile.close()
    tempC = float(tempfile_text.split("\n")[1].split("t=")[1])/1000
    tempF = tempC*9.0/5.0+32.0
    return [currentTime,tempC,tempF]

con = mydb.connect('temperature.db')

with con:
    cur = con.cursor()
    #cur.execute("CREATE TABLE tempData(data TEXT, tempC DOUBLE,tempF DOUBLE)")
    mydata = readTemp()
    myTime = str(mydata[0])
    cels = mydata[1]
    fahr = mydata[2]
    cur.execute('''INSERT INTO tempData(data,tempC,tempF)
                VALUES(?,?,?)''', (myTime,cels,fahr))
    print 'Current Temperature is: ' + str(fahr) + ' F'
    print 'Temperature logged\n'
