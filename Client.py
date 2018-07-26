import socket
#from thread import *
import sys
import threading
from threading import Thread
import pickle

s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sListen=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sListen.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

portL = pickle.load(open("port","rb"))
pickle.dump(portL+1,open("port","wb"))

try:
	sListen.bind(('127.0.0.1',portL))
	print "sokect created with port",portL
except socket.error, msg:
	print 'Bind failed. Error Code: ' + str(msg[0]) + ' Message: ' + msg[1]
	sys.exit()
sListen.listen(5)
print "Socket now listening"




def obtain (s,filename , filepath) :


				queryMessage = 'DOWNLOAD\n' + filename + '\n' + filepath
				try:
					s.sendall(queryMessage)
				except socket.error:
					print 'Send failed'
					sys.exit()
				fw = open("Downloads/" + filename,'wb+')
				file_content = s.recv(100)
				fw.write(file_content)
				print "File Downloded"
				fw.close()
				s.close()




def client(host, port, s, portL):
	try:
		ip = socket.gethostbyname(host)
	except socket.gaierror:
		print 'Hostname couldn\'t be resolved. Exiting'
		sys.exit()
	
	
	
	
	s.connect((ip, port))
	reply = s.recv(4096)

	print reply
	try:
		portL = str(portL)
		s.sendall(portL)
	except socket.error:
		print 'Send local port  failed'
		sys.exit()


	while 1:
		input = raw_input(">>>>>")
		#input = input.lstrip()
		#input = input.rstrip()
		if not input:
			continue

		elif input[0] is '1':
			nickname = raw_input('Enter peer name: ')
			message = 'REGISTER\n' + nickname


		elif input[0] is '2':
			fileName = raw_input('file name: ')
			filePath = raw_input('file path: ')
			message = 'register_file\n'+fileName+','+filePath


		elif input[0] is '3':
			fileName = raw_input('file name : ')
			message = 'SEARCH\n'+fileName
			try:
				s.sendall(message)
			except socket.error:
				print 'Send failed'
				sys.exit()
			reply = s.recv(4096)
			if reply.split('\n')[0] == 'ERROR':
				print reply.split('\n')[1]
				sys.exit()

			usersHavingFile = eval(reply)
			if not usersHavingFile:
				s.sendall('File not found Or thats no active peers ')
				continue

			message = ' users have the file:\n'
			for user in usersHavingFile.keys():
				#print 'hi'
				print "peer : "+ usersHavingFile[user]['nick'] +', ip : '+usersHavingFile[user]['ip'] +' , FilePath :' + usersHavingFile[user]['filePath'] + ', port :',usersHavingFile[user]['port']



			s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			peerIP = raw_input("enter peerIP :")
			peerport = int(raw_input("enpter peerPort: "))
			print "ip:  " +peerIP + " /peerPort :",peerport;

			s1.connect((peerIP, peerport))
			obtain(s1, fileName,usersHavingFile[peerport]['filePath'])
		elif input is '4':
			break

		else:
			print 'Unknown command'
			continue
	
		try:
			s.sendall(message)
		except socket.error:
			print 'Send failed'
			sys.exit()
		
		#print 'Message sent successfully'
		
		reply = s.recv(4096)
		
		print reply
	
	s.close()


def peer_as_server(s):

	while 1:
		conn, addr = s.accept()

		print "connected with  Ip : "+addr[0]+" , Port : ",addr[1]
		data = conn.recv(4096)
		if data.split('\n')[0]=='DOWNLOAD':
			fileName = data.split('\n')[1]
			filePath = data.split('\n')[2]

			try:
				fr = open(filePath,'rb')
			except:
				conn.sendall('ERROR\nThe File Path Dosent Exsist')
				continue
			file_content = fr.read()
			conn.send(file_content)
	s.close()
###########################################


try:
	host = '127.0.0.1'
	port = 55555
	#host = 'localhost'
	#port = 55555 
	print host
	print port


	if __name__ == '__main__':
	    Thread(target = client, args = (host,port,s,portL,) ).start()
	    Thread(target = peer_as_server, args = (sListen,) ).start()
except:
	sListen.close()

###########################

