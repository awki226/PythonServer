#Alex King 
#Client.py
#Implementaion does the functions for the client
#

import tqdm  #used for the upload/download progress bar 
import socket 
import sys
import os
import time

#SET the HOST to default since I'm connecting
HOST = '127.0.0.1'
SPACER = "<SPACER>"
BUFFER = 1024 * 4
#-------------------------------------------------
#Uplaod handle the uploading of a file 
#from the client side
def upload(filename, filesize):	
	#sends the filename and filesize to server
	s.send(f"{filename}{SPACER}{filesize}".encode())
	
	f = open(filename, "rb")
	#This is the progess bar for upload inlcudes the MB/s,time passed and filesize
	datarate = tqdm.tqdm(range(filesize), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024)
	#reads though file
	while (f):
		l = f.read(BUFFER)
		if not (l): #case where no more data is sent
			break
		s.sendall(l)
		datarate.update(len(l))
	datarate.close()
	#closes socket and file
	f.close()
	s.close()
	return
#------------------------------------------------
#Handles the downloading of files 
def download(fn):
	#Gets the filename and filesize
	file_rec = s.recv(BUFFER).decode()
	filename, filesize = file_rec.split(SPACER)
	filename = os.path.basename(filename)
	filesize = int(filesize)
	f = open(filename, 'wb')
	#progress bar
	data_rec = tqdm.tqdm(range(filesize), f"Recieving {filename}", unit="B", unit_scale=True, unit_divisor=1024)
	#recieves the data
	while (f):	
		data = s.recv(BUFFER)
		if not (data):
			break
		f.write(data)
		data_rec.update(len(data))
	data_rec.close()
	#states if file was written
	print("file was written")
	f.close()
	s.close()
	return 
#---------------------------------------------------

#main function of the client
while(True):
	#socket using SOCK_STREAM for TCP
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	pt = input('What port would you like to connect to(42069)? ')
	PORT = int(pt)
	s.connect((HOST,int(PORT)))
	data = s.recv(BUFFER).decode()
	#Acknowledges that it is connected
	print('Received', data)	
	print('What would you like to do UPLOAD a file, DOWNLOAD a file,')
	print('DOWNLOAD file, DELETE file on server, PRINT server contents')
	request = input()
	request.ljust(BUFFER)
	#These conditions redirect requests made by the client
	if(request == 'UPLOAD'):
		s.send(request.encode()) 
		filename = input("filename:")
		filesize = os.path.getsize(filename)
		upload(filename, filesize)
	elif (request == 'DOWNLOAD'):
		s.send(request.encode())
		fn = input("Filename:")
		fn.ljust(BUFFER)
		s.send(fn.encode())
		#State makes sure the file exists
		state = s.recv(BUFFER)
		if(state.decode() == "file exists"):
			print(state.decode())
			filename = download(fn)
			print('Filename:', filename)
		else:
			print(state.decode())
			s.close()
	elif (request == 'DELETE'):
		#sends file to be deleted
		s.send(request.encode())
		filename = input("Filename:")
		s.send(filename.encode())
		#acknowledges if file has been deleted or
		#not
		ack = s.recv(BUFFER)
		print(ack.decode())
		s.close()
	elif (request == 'PRINT'):
		#send request and 
		s.send(request.encode())
		print("File directory of Server", HOST, "", PORT, "\n")
		dir = s.recv(BUFFER)
		print(dir.decode())
		s.close()
	elif (request == 'QUIT'):
		#Exit request
		print("ENDING CONNECTION")
		s.close()
		break

	
