# Alex King
#Server side 
#Handles requests made by the server

import time
import tqdm #used for UPLOAD/DOWNLOAD progess rate
import socketserver
import socket
import sys		
import logging
import threading
import os

#set to default since working on local machine
HOST = '127.0.0.1'
PORT = 42069         
BUFFER = 1024 * 4    # 4KB buffer
SPACER = "<SPACER>"  #used for spliting
#-------------------------------------
#used built in socketserver class to make a TCPHANDLER
#TCP has a typically long timeout this was prefered
class TCPHandler(socketserver.BaseRequestHandler):
	'''
		Handles the request made by the client

	'''
	def handle(self):
		#finds client connected and prints the info
		print("Connected by:", self.client_address[0])
		self.request.send('You are connected'.encode())
		data = self.request.recv(BUFFER).decode()
		if(data == "UPLOAD"):
			#Gets file details such as filename and size
			file_rec = self.request.recv(BUFFER).decode()
			filename, filesize = file_rec.split(SPACER)
			print("Client wants to ",data , filename)
			filename = os.path.basename(filename)
			filesize = int(filesize) 
			f = open(filename, 'wb')
			print('writing file')
			#print(filesize)
			#this does the progess of how fast the upload speed is 
			data_rec  = tqdm.tqdm(range(filesize),f"RECIVEING {filename}", unit="B", unit_scale=True, unit_divisor=1024)
			while (f): # recieves file and writes it
				data = self.request.recv(BUFFER)
				if not (data): #case where file done
					break
				f.write(data)
				data_rec.update(len(data))
				#print(data_rec)
			data_rec.close()
			#notifies the file is written
			print('File was written')
			self.request.close()
			f.close()
		if(data == "DOWNLOAD"):
			#Gets filename 
			file_rec = self.request.recv(BUFFER).decode()
			file_rec = file_rec.rstrip()
			print("Client wants to download:", file_rec)
			#base case for state file DNE
			state = "file does not exist"
			if(os.path.exists(file_rec) == True):
				#changes state to file exists
				state = "file exists"
				print(state)
				state.ljust(BUFFER)
				self.request.send(state.encode())
				filename = os.path.basename(file_rec)
				filesize = os.path.getsize(filename)
				self.request.send(f"{filename}{SPACER}{filesize}".encode())
				f = open(filename, "rb")
				#progess bar for Downloading
				data_rec  = tqdm.tqdm(range(filesize),f"SENDING {filename}", unit="B", unit_scale=True, unit_divisor=1024)
				while (f): #reads file and sends it to client
					l = f.read(BUFFER)
					if not (l): #case if empty
						break
					self.request.sendall(l)
					data_rec.update(len(l))
				data_rec.close()
				f.close()
				#closes this socket when finish
				print("File was sent")
				self.request.close()
			else:
				#case where file doesn't exist
				print(state)
				state.ljust(BUFFER)
				self.request.send(state.encode())
		if(data == "DELETE"):
			#case where Client was to delete a file
			file_rec = self.request.recv(BUFFER).decode()
			print("Client wants to delete: ", file_rec)
			#ack is changed if file is deleted or not
			ack = ''
			ack.ljust(BUFFER)
			if(os.path.exists(file_rec) == True):
				filename = os.path.basename(file_rec)
				os.remove(filename)
				ack = "File was deleted"
				print(ack)
				self.request.send(ack.encode())
			else:
				ack = "No File existed"
				self.request.send(ack.encode())
			self.request.close()
		if(data == "PRINT"):
			print("Client wants to see the Directory")
			path = '.'
			dir = os.listdir(path)
			results = ""
			#goes through the files in the directory to get their attributes
			for file in dir:
				full_path = os.path.join(path, file)
				results = results + file 
				results = results + " Size " + str(os.path.getsize(full_path))	+ "B"
				results = results + " Uploaded " +  str(time.ctime(os.path.getctime(full_path)))
				results = results + "\n"
			print("SENDING DIRECTORY")
			self.request.send(results.encode())
			self.request.close()
			
#sets up the server using the TCP server model
#server is set to run forvever until keyboard interupt
server = socketserver.TCPServer((HOST,PORT) , TCPHandler)
print('Server is active ', HOST ,':', PORT)
server.serve_forever()
print( server.data)
