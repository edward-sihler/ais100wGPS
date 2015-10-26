import serial
import time
import getopt
import sys
import os
import subprocess
 
def main (argv) :

    usbPort = subprocess.check_output("dmesg | grep \"FTDI.*now attached to ttyUSB\"", shell=True)
    i = usbPort.rfind("ttyUSB")
    usbPort = '/dev/' + usbPort[i:].strip()
    ttyIs = usbPort
    #ttyIs = '/dev/ttyUSB2'
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
    ais = serial.Serial(ttyIs, 38400, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE)
    ais.flush()
    msg = ''
    while True: 
        try:
          msg = ais.readline().strip()
          print (msg)
        except serial.SerialException:
            time.sleep(5)

#except (KeyboardInterrupt, SystemExit):
#          gpsd.running= False
#          gpsd.join()

    #print msg
    #msgSplit = msg.split(',')
    #if msgSplit[0] == '!AIVDM' or msgSplit[0] == '!SAVDM':
    #    ais = msgSplit[5]


if __name__=='__main__':
    main(sys.argv[1:])
