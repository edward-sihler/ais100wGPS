import serial
import time
import getopt
import sys
import os
from gps import *
from time import *
import threading
import subprocess
 
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
    while gpsd.running:
      gpsd.next() #this will continue to loop and grab EACH set of gpsd info to clear the buffer


def main (argv) :

  usbPort = subprocess.check_output("dmesg | grep \"FTDI.*now attached to ttyUSB\"", shell=True)
  i = usbPort.rfind("ttyUSB")
  usbPort = '/dev/' + usbPort[i:].strip()
  ttyIs = usbPort
  #ttyIs = '/dev/ttyUSB0'
  logfile = ''

  try:
    opts, args = getopt.getopt(argv, "hl", ["help", "logfile="])
  except getopt.GetoptError:
    print ('ais100.py --logfile=<logfile>')
    sys.exit(2)

  for opt, arg in opts:
    if opt in ("-l", "--logfile"):
      logfile = arg
    elif opt in ('-h', "--help"):
      print ('ais100.py --logfile=<logfile>')
      sys.exit(2)
    #print (logfile)
    #sys.exit(2)

  #setup GPS
  global gpsp
  gpsp = GpsPoller() # create the thread

  try:
    gpsp.start()
    os.system('clear')
    
    ais = serial.Serial(ttyIs, 38400, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE)
    ais.flush()
    msg = ''
    print ("Off and Running " +  ttyIs )
    foo = 0
    while True:
      utc = str(gpsd.utc)
      foo += 1
      #os.system('clear')
      print("UTC ["+ utc +"]" )
      msg = ''
      try:
        #msg = ais.readline().strip()
        msg += ", " + str(gpsd.fix.time)
        msg += ", " + gpsd.utc
        msg += ", " + str(gpsd.fix.longitude)
        msg += ", " + str(gpsd.fix.altitude)
        print (msg)
      except serial.SerialException:
        print ("no signals found at UTC: " + fixTime)
        time.sleep(5)
  except (KeyboardInterrupt, SystemExit):
    gpsp.running= False
    gpsp.join()

    #print msg
    #msgSplit = msg.split(',')
    #if msgSplit[0] == '!AIVDM' or msgSplit[0] == '!SAVDM':
    #    ais = msgSplit[5]


if __name__=='__main__':
    main(sys.argv[1:])
