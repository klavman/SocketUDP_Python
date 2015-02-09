#!/usr/bin/python

import socket
import sys
from time import strftime, localtime
import locale

def menu():
	print '\n', '\n'
	print "#################################################################"
	print "#############              SERVER             ###################"
	print "#################################################################\n"
 
address = ''   # default localhost
port = 1047   

locale.setlocale(locale.LC_ALL,""); # set languague local machine

menu()
 

try :
	s_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

except socket.error:
	print 'Error create socket'
	sys.exit()
 

try:
	s_server.bind((address, port))
except socket.error:
	print 'Error port/address'
	sys.exit()

 
# Client conection

while True:
	# data received
	data_received = s_server.recvfrom(1047)
	received = data_received[0]
	address = data_received[1]
	send = ""

	if received == "DAY":
		send = strftime("%A, %d de %B de %Y", localtime())
	elif received == "TIME":
		send = strftime("%H:%M:%S", localtime())
	elif received == "DAYTIME":
		send = strftime("%A, %d de %B de %Y; %H:%M:%S", localtime())
	else:
		send = 'Error send.'
	 
	 
	s_server.sendto(send , address)
	print 'message send: ' + send 
	print 'message send by: ' + address[0]

	 
s_server.close()
