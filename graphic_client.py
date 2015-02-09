#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-

from PySide import QtCore, QtGui

import sys

import socket 

import select

class ClientUDP(QtGui.QMainWindow):

	def __init__(self, parent=None):
		super(ClientUDP, self).__init__(parent)
		
		
		self.setWindowTitle("UDP Client")
		
		self.setMaximumSize(500,200)
		self.setMinimumSize(500,200)


		element = QtGui.QWidget()
		self.setCentralWidget(element) # center in window

		self.status = QtGui.QStatusBar()
		
		self.hbox = QtGui.QHBoxLayout()
		self.hbox.addWidget(self.status)

		
		
	 

		############# Buttons ##########################

		self.buttonSave = QtGui.QPushButton('Clear')

		self.buttonSend = QtGui.QPushButton('Send')

		self.buttonExit = QtGui.QPushButton('Exit')
		

		self.buttonSave.clicked.connect(self.clearParam)

		self.buttonSend.clicked.connect(self.sendMessage)

		self.buttonExit.clicked.connect(self.exitAction)


		#############  DAYTIME  #########################
		
		self.daytime = QtGui.QComboBox()

		op = []
		op.append("DAY")
		op.append("TIME")
		op.append("DAYTIME")

		self.daytime.addItems(op)
	  

	  
		self.etiqueta_ip = QtGui.QLabel('IP Address:')

		self.etiqueta_timeout = QtGui.QLabel('Retry time (seg):')

		self.etiqueta_peticion = QtGui.QLabel('Request:')

		
		self.ip_adress=QtGui.QLineEdit()

		regexp = QtCore.QRegExp('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')
		validator = QtGui.QRegExpValidator(regexp)
		self.ip_adress.setValidator(validator)

		self.ip_adress.textChanged.connect(self.check_state)
		self.ip_adress.textChanged.emit(self.ip_adress.text())

		
		self.timeout=QtGui.QLineEdit()

		regexp_t = QtCore.QRegExp('\d{1,2}')
		validator = QtGui.QRegExpValidator(regexp_t)
		self.timeout.setValidator(validator)

		self.timeout.textChanged.connect(self.check_state)
		self.timeout.textChanged.emit(self.timeout.text())			  

		
		########### GRID ###################
		
		grid = QtGui.QGridLayout()

		grid.addWidget(self.etiqueta_ip, 0, 0,5)
		grid.addWidget(self.ip_adress, 0, 1,5)
		

		grid.addWidget(self.etiqueta_timeout, 1, 0,5)
		grid.addWidget(self.timeout, 1, 1,5)        

		grid.addWidget(self.etiqueta_peticion, 2, 0,5)
		grid.addWidget(self.daytime, 2, 1, 5)


		grid.addWidget(self.buttonSave, 3, 0)
		grid.addWidget(self.buttonSend, 3, 1)
		grid.addWidget(self.buttonExit, 3, 2)

		grid.addLayout(self.hbox,4,1,1,1)

		
		element.setLayout(grid)                                                           


# buttons functions 


	def check_state(self):
		sender = self.sender()
		validator = sender.validator()
		state = validator.validate(sender.text(), 0)[0]

		if state == QtGui.QValidator.Acceptable:
				color = '#c4df9b' # green
		elif state == QtGui.QValidator.Intermediate:
				color = '#fff79a' # yellow
		else:
				color = '#f6989d' # red
		sender.setStyleSheet('QLineEdit { background-color: %s }' % color)


	def clearParam(self):
		self.ip_adress.clear()
		self.timeout.clear()



	def sendMessage(self): 	

		if not self.ip_adress.text().strip() or not self.timeout.text().strip():
			
			QtGui.QMessageBox.information(self,'Information', 'Insert ip and retry time before send a request.')

		else:

			try:  
				s_cliente = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # Create socket

			except socket.error:
				print 'Error create socket'
				sys.exit()
	 
			address = self.ip_adress.text() #localhost
			port = 1047; 

			flag = True
			while(True and flag):

			 
				try:
			
					x = 0
					while x < 3:

						s_cliente.sendto(self.daytime.currentText(), (address, port))

						CheckSelect = select.select([s_cliente],[],[],int(self.timeout.text()))
			 

						if not CheckSelect[0]:

							print 'Timeout...'
							x = x + 1
							print 'retry ' + str(x)
							self.status.showMessage("Timeout... wait.",0)

							if x == 3:
								QtGui.QMessageBox.information(self,'Information', 'Fail conection. Maximum number of retries')               
								self.status.clearMessage()
								flag = False
			  
			  
						elif CheckSelect[0]:         
							data_received = s_cliente.recvfrom(1047)
							received = data_received[0]
							address = data_received[1]

							QtGui.QMessageBox.information(self,'Data received', received)
							self.status.clearMessage()


							flag = False
							x = 3

							print 'Successful conection\n\n'
		 
				except socket.error:
							QtGui.QMessageBox.information(self,'Error', 'Error send/receive. \'OK\' to exit.')
							sys.exit()

			s_cliente.close()           


	def exitAction(self):

		response = QtGui.QMessageBox.question(self, 'Message', unicode("Are you sure you want to close the program?",'utf-8'), QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
		if response == QtGui.QMessageBox.Yes:												
			self.close()   																

				
		   
# Main 
def main():

	app = QtGui.QApplication(sys.argv)
	w = ClientUDP()
	w.show()
	
	sys.exit(app.exec_())


if __name__ == '__main__':
	main()