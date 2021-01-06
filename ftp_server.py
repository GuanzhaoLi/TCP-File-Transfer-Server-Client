from socket import *
import os
import sys
import signal 
import time

FILE_PATH = './'

class FtpServer(object):
	def __init__(self, connfd):
		self.connfd = connfd

	def do_list(self):
		file_list = os.listdir(FILE_PATH)
		
		# server check whether can be done
		if not file_list or file_list == None:
			self.connfd.send(b"Fail")
		self.connfd.send(b"OK")
		time.sleep(0.1)
		
		for filename in file_list:
			if filename[0] != '.' and os.path.isfile(FILE_PATH+ filename):
				self.connfd.send(filename.encode())
				time.sleep(0.1)

		self.connfd.send(b"##") # send complete code
		print('send list completed')
		return

	def do_get(self, filename):
		print(filename)
		try:
			fd = open(FILE_PATH + filename, 'rb')
		except:
			self.connfd.send(b"Fail")
		
		self.connfd.send(b"OK")
		time.sleep(0.1)
		for line in fd:
			self.connfd.send(line)

		fd.close()
		time.sleep(0.1)
		self.connfd.send(b"##")
		print("file send completed")
		return

	def do_put(self, filename):
		try:
			fd = open(FILE_PATH + filename, 'w')
		except:
			self.connfd.send(b"FALL")
		self.connfd.send(b'OK')
		
		while True:
			data = self.connfd.recv(1024).decode()
			if data == "##":
				break
			fd.write(data)
		fd.close()
		print("receive file completed")


def main():
	if len(sys.argv) != 3:
		print("argv is error")
		sys.exit(1)

	HOST = sys.argv[1]
	PORT = int(sys.argv[2])
	ADDR = (HOST, PORT)
	BUFFERSIZE = 1024

	sockfd = socket()
	sockfd.bind(ADDR)
	sockfd.listen(5)
	signal.signal(signal.SIGCHLD, signal.SIG_IGN)
	
	while True:
		try:
			connfd, addr = sockfd.accept()
		except KeyboardInterrupt:
			sockfd.close()
			sys.exit(0)

		except Exception:
			continue

		print("client login: ", addr)
		pid = os.fork()
		
		if pid <0:
			print("fail to fork child process")
			continue
		elif pid == 0:
			sockfd.close()
			ftp = FtpServer(connfd)
			# listen for client request
			while True:
				data = connfd.recv(BUFFERSIZE).decode()
				if data == 'L':
					ftp.do_list()
				
				elif data[0] == 'G':
					filename = data.split(" ")[-1]
					ftp.do_get(filename)

				elif data[0] == 'P':
					filename = data.split(" ")[-1]
					ftp.do_put(filename)
				
				elif data[0] == 'Q':
					print("client quit")
		else:
			connfd.close()
			continue


if __name__ == "__main__":
	main()