from socket import *
import sys
import time

FILE_PATH = './'

class FtpClient(object):
	def __init__(self, sockfd):
		self.sockfd = sockfd
	
	def do_list(self):
		self.sockfd.send(b"L")

		data = self.sockfd.recv(1024).decode()
		if data == 'OK':
			while True:
				data = self.sockfd.recv(1024).decode()
				if data == '##':
					break
				else:
					print(data)
			print("file transfer completed!")

		else:
			print("file transfer failed")
			return
	
	def do_get(self, filename):
		self.sockfd.send( ("G "+ filename).encode())
		data = self.sockfd.recv(1024).decode()
		if data == 'OK':
			fd = open(filename, 'w')
			while True:
				data = self.sockfd.recv(1024).decode()
				if data == "##":
					break
				fd.write(data)
			fd.close()
			print("%s download completed"% filename)
			return

		else:
			print("download failed")
			return

	def do_put(self, filename):
		try:
			fd = open(FILE_PATH + filename, 'rb') # read as binary format
		except:
			print("input file not exist")
			return

		self.sockfd.send(("P "+ filename).encode())
		data = self.sockfd.recv(1024).decode()

		if data == 'OK':
			for line in fd:
				self.sockfd.send(line)
			time.sleep(0.1)
			fd.close()
			self.sockfd.send(b"##")
			print("upload %s completed"%filename)
			return

		else:
			print("upload failed")
			return

	def do_quit(self):
		self.sockfd.send(b"Q")
		sys.exit(0)

def main():
	if len(sys.argv) != 3:
		print("argv is error")
		sys.exit(1)

	HOST = sys.argv[1]
	PORT = int(sys.argv[2])
	ADDR = (HOST, PORT)
	BUFFERSIZE = 1024

	sockfd = socket()
	
	sockfd.connect(ADDR)
	ftp = FtpClient(sockfd)

	while True:
		print("*************** You can do ***************")
		print("*************** list ***************")
		print("*************** get file ***************")
		print("*************** put file ***************")
		print("*************** quit ***************")
		
		data = input("Please input command: ")
		if  data[:4] == "list":
			ftp.do_list()

		elif data[:3] == 'put':
			filename = data.split(" ")[-1]
			ftp.do_put(filename)

		elif data[:3] == 'get':
			filename = data.split(" ")[-1]
			ftp.do_get(filename)

		elif data[:4] == 'quit':
			ftp.do_quit()
			sockfd.close()
			sys.exit(0)

		else:
			print("Please input one of four commands")
			continue



if __name__ == "__main__":
	main()
