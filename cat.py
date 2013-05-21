#!/usr/bin/python

import socket
import threading
global_values = {'exit_status':0, 'remote_port':49152,'local_port':49153}
class sender (threading.Thread):
	
	def __init__ (self,global_values):
		threading.Thread.__init__ (self)
		
	def run (self):
		print "Starting sender thread"
		self.messenger_sender ()
		print "Exiting sender thread"
	def messenger_sender (self):
		print "-----------p2pMessenger 1.0-----------"
		print "\n\n"
		receiver_address = raw_input ("Enter reciever address to begin:")
		print "Establishing connection to peer"
		try:
			sender_socket = socket.socket ()
			host = receiver_address
			port = global_values['remote_port']
			sender_socket.connect ((host,port))
			sender_socket.send("*/ignore")
		except:
			print "Unable to create a connection to address specified"
		else:
			msg_string = " "
			print "Connected to ",receiver_address
			print "Connection established, use */quit to exit"
			while global_values['exit_status'] == 0:
				msg_string = raw_input (":")
				if msg_string == "*/quit":
					global_values['exit_status'] = 1
				sender_socket.send (msg_string)
					
class receiver (threading.Thread):
	
	def __init__ (self,global_values):
		threading.Thread.__init__ (self)
		
	
	def run (self):					 	
		print "Starting receiver thread"
		self.messenger_receiver ()
		print "Exiting receiver thread"
	
	def messenger_receiver (self):
		receiver_socket = socket.socket ()
		host = '' 
		port = global_values['local_port']
		receiver_socket.bind ((host,port))
		receiver_socket.listen (2)
		while global_values['exit_status'] == 0:
			sender_socket,sender_address = receiver_socket.accept ()
			
			while global_values['exit_status'] == 0:
				received_string = sender_socket.recv (1024)
				if received_string == "*/ignore":
					continue
				print "%s:%s" %(sender_address,received_string)
				
		receiver_socket.close ()

thread_sender = sender(global_values)
thread_receiver = receiver(global_values)
thread_sender.start()
thread_receiver.start()

