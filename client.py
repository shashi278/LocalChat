'''
The Client Script:
	Every client must run this script at the same
	address as the server is online at, to get
	connected
'''

import socket
import sys
import re
import select

server= socket.socket(socket.AF_INET, socket.SOCK_STREAM)

class Client():
	
	def __init__(self, host, port):
		self.host= host
		self.port= port
		self.addr= (self.host, self.port)
	
	def filter_text(self,text):
		'''
		args:
			Text of type str
		return:
			For now, it just truncates the ending newline char
			More filteration can be added later 
		'''
		return re.sub('\n$', '',text)
	
	def connect(self):
		
		server.connect(self.addr)
		
		#Runs forever and looks for messages exchange
		while True:
			
			#list out the reading/writing streams
			sock_list=[sys.stdin, server]
			
			read_soc, write_sock, excep_sock= select.select(sock_list, [], [])
			
			for sock in read_soc:
				
				if sock == server:
					#If its server, It's ready to receive msgs
					msg= sock.recv(2048)
					if msg:
						print(self.filter_text(msg.decode('utf-8')))
				else:
					#else it's ready to write, hence get input
					msg= sys.stdin.readline()
					server.send(bytes(msg, 'utf-8'))
					sys.stdout.flush()

if __name__ == '__main__':
	
	host, port= '127.0.0.1', 54321
	if len(sys.argv)==3:
		host, port= sys.argv[1], int(sys.argv[2])
		
	c= Client(host, port)
	c.connect()

server.close()