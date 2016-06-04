# Echo client program
import socket
import sys


class Client(object):

	def sendToLightClient (command):
		print command
		HOST = '192.168.15.201'    # The remote host
		PORT = 80              # The same port as used by the server
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect((HOST, PORT))
		s.sendall(command)
		data = s.recv(1024)
		s.close()
		print 'Received', repr(data)


if __name__ == "__main__":
	client = Client()
	client.sendToLightClient(sys.argv[1])
