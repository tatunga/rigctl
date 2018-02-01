#!/usr/bin/env python
# coding: utf-8

# RigReles: Controle de relés para resetear RIGS
# usar con sudo

from multiping import MultiPing
from time import sleep
import minimalmodbus
import serial
import curses
import time
from pynput.keyboard import Key, Listener

ipDev1 = "konoba.duckdns.org"
ipDev2 = "depa.duckdns.org"
ipDev3 = "andinitsolar.cl"

tOutGlobal = 15 #seg
numReintento = 3 


RELE10=0
RELE11=1
RELE20=2
RELE21=3
RELE30=4
RELE31=5
RELE40=6
RELE41=7
RELE50=8
RELE51=9
RELE60=10
RELE61=11
RELE70=12
RELE71=13
RELE80=14
RELE81=15
RELE90=16
RELE91=17

instrument = minimalmodbus.Instrument('/dev/ttyUSB0', 1) # port name, slave address (in decimal)



instrument.serial.port ='/dev/ttyUSB0'      		# this is the serial port name
instrument.serial.baudrate = 9600   			# Baud
instrument.serial.bytesize = 8
instrument.serial.parity   = serial.PARITY_NONE
instrument.serial.stopbits = 1
instrument.serial.timeout  = 0.05   			# seconds

instrument.address = 1     # this is the slave address number
instrument.mode = minimalmodbus.MODE_RTU   # rtu or ascii mode

k=0

def RTU(dodi, ch , val):


    if(val == "reset" and dodi == "do"):


	    if(ch==10):
		#do it
		instrument.write_bit(RELE10, 1, 5)
		sleep(10)
		instrument.write_bit(RELE10, 0, 5)

	    if(ch==11):
		#do it
		instrument.write_bit(RELE11, 1, 5)
		sleep(10)
		instrument.write_bit(RELE11, 0, 5)


    return 0

def on_press(key):
    print('{0} pressed'.format(
        key))

def on_release(key):
    print('{0} release'.format(
        key))
    if key == Key.esc:
        # Stop listener
	k = 1        
	print k	
	return False




def main():
  



    while(k == 0):
     
	
        # Crea un objeto Multiping para probar 3 host
	mp = MultiPing(["konoba.duckdns.org", "caca.org", "konoba.duckdns.org"])

	# Envía los pings a las direcciones
	mp.send()

	# With a 1 second timout, wait for responses (may return sooner if all
	# results are received).
	responses, no_responses = mp.receive(tOutGlobal)



	for addr, rtt in responses.items():
	    print "%s responded in %f seconds" % (addr, rtt)
	
	    if rtt >= segUmbral:
		#hace algo
	 	RTU("do", 10 , "reset")


	for addr in no_responses:
    	    print "%s responded in %f seconds" % (addr, rtt)

	if addr == ipDev1:
	    #hace algo
	    RTU("do", 10 , "reset")

	if addr == ipDev2:
            #hace algo
            RTU("do", 11 , "reset")



	if no_responses:
	    print "These addresses did not respond: %s" % ", ".join(no_responses)
	    # Sending pings once more, but just to those addresses that have not
	    # responded, yet.
	    mp.send()
	    responses, no_responses = mp.receive(tOutGlobal)

	    print no_responses
	    print "Ping Tout Alcanzado %i" %tOutGlobal
	    print "Aplicando Reset 10"
	    RTU("do", 10 , "reset")


	# Collect events until released
	with Listener(
            on_press=on_press,
            on_release=on_release) as listener:
	        listener.join()


if __name__ == "__main__":
    main()



























