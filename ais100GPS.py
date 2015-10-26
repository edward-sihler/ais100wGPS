#! /usr/bin/python
# by edward silher for collecting gps data in conjuction with AIS data
# edwardsihler@ursusonline.net

import serial
import subprocess
import os
from gps import *
from time import *
import time
import threading
 
gpsd = None #seting the global variable
 
os.system('clear') #clear the terminal (optional)
 
class GpsPoller(threading.Thread):
  def __init__(self):
    threading.Thread.__init__(self)
    global gpsd #bring it in scope
    gpsd = gps(mode=WATCH_ENABLE) #starting the stream of info
    self.current_value = None
    self.running = True #setting the thread running to true
 
  def run(self):
    global gpsd
    while gpsp.running:
      gpsd.next() #this will continue to loop and grab EACH set of gpsd info to clear the buffer

#  def utc(self):
#    return gpsd.utc
 
def main (argv):
  
  #find the port with the AIS reciver on it
  usbPort = subprocess.check_output("dmesg | grep \"FTDI.*now attached to ttyUSB\"", shell=True)
  i = usbPort.rfind("ttyUSB")
  aisPort = '/dev/' + usbPort[i:].strip()
  #aisPort = '/dev/ttyUSB0'

  ais = serial.Serial(aisPort, 38400, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE)

  global gpsp
  gpsp = GpsPoller() # create the thread
  try:
    gpsp.start() # start it up
    while True:
      #It may take a second or two to get good data
      #print gpsd.fix.latitude,', ',gpsd.fix.longitude,'  Time: ',gpsd.utc
 
      #os.system('clear')
      msg = ''
      msg = str(gpsd.utc)
      msg += ", " + str(gpsd.fix.latitude) 
      msg += ", " + str(gpsd.fix.longitude )
      try:
        msg += ", " + ais.readline().strip()
        print(msg)
      except serial.SerialException:
        time.sleep(5)
      print (msg)
      #time.sleep(5) #set to whatever
 
  except (KeyboardInterrupt, SystemExit): #when you press ctrl+c
    print "\nKilling Thread..."
    gpsp.running = False
    gpsp.join() # wait for the thread to finish what it's doing
  print "Done.\nExiting."


if __name__ == '__main__':
  main(sys.argv[1:])
