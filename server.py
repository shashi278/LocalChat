
'''
The Server Script:
	Must be kept running on a system to keep server up all the time
'''

import socket
import sys
import types
import select
import re
from _thread import *

#create an IvP4 server
server= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

class Server():
	
	def __init__(self, host, port):
		self.host= host
		self.port= port
		self.addr= (self.host, self.port)
		self.client_list= []
	
	def clientThread(self, data):
		conn, addr, name= data.conn, data.addr, data.name
	
		conn.send(bytes("\t\tYou joined chat room",'utf-8'))
		
		#keep reading for msgs from the connected client
		while True:
			try:
				message= conn.recv(2048)
				if message:
					brodMsg= bytes("<{}>: {}".format(name,message.decode('utf-8')), 'utf-8')
					selfMsg= bytes("<You>: {}".format(message.decode('utf-8')),'utf-8')
					conn.send(selfMsg)
					self.broadcast(conn, brodMsg)
				
				else:
					#if no msgs, close the connection
					#it's not working though
					if conn in self.client_list:
						msg= bytes("\t\t{} left the chat".format(name), 'utf-8')
						self.broadcast(conn, msg)
						conn.close()
						self.client_list.remove(conn)
			except:
				continue
	
	def broadcast(self, conn, msg):
		'''
		args:
			conn: connection object
			msg: message to be broadcasted
			
		Sends the msg to all clients in the client_list except the sender itself
		'''
		for client in self.client_list:
			if client.conn != conn:
				client.conn.send(msg)
	
	def filter_text(self, text):
		'''
		args:
			text: Text of type str
		return:
			For now, it just truncates the ending newline char
			More filteration can be added later 
		'''
		return re.sub('\n$', '', text)
	
	def run(self):
		
		server.bind((self.host, self.port))
		
		#Listen to maximum of 100 clients
		server.listen(100)
		
		print('listening on....{}'.format(self.addr))
		
		'''
		Run the script for forever and keep looking for any
		incoming connection from the client
		'''
		while True:
			try:
				conn, addr= server.accept()
				conn.send(bytes("Please enter your name: ", 'utf-8'))
				name= conn.recv(1024)
				if not name:
					name= ''
				else:
					name= self.filter_text(name.decode('utf-8'))
			except:
				break
			
			# simple object to bundle up few attributes of a connection
			data= types.SimpleNamespace(
				conn= conn,
				addr= addr,
				name= name
			)
			
			#add the client data to the list
			self.client_list.append(data)
			
			#send a msg to everyone that someone has joined
			msg= bytes("\t\t{} joined".format(name),'utf-8')
			self.broadcast(conn, msg)
			
			#And finally create a new thread for every connection
			start_new_thread(self.clientThread, (data,))
		

if __name__=='__main__':
	
	host, port= '127.0.0.1', 54321
	if len(sys.argv) ==3:
		host, port= sys.argv[1], int(sys.argv[2])
		
	s= Server(host, port)
	s.run()

server.close()