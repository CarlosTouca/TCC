import sys
import socket
import requests

# deprecated
def sendToLightClientSocket (command):
	print command
	HOST = '192.168.15.201'    # The remote host
	PORT = 80              # The same port as used by the server
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((HOST, PORT))
	s.sendall(command)
	data = s.recv(1024)
	s.close()
	print 'Received', repr(data)

def sendToLightClient (ip,command):
	print command
	HOST = ip    	# The remote host
	PORT = '80'              		# The same port as used by the server
	url = 'http://' + HOST + ':' + PORT + '/gpio/' + command
	r = requests.get(url);
	print r

class Light(object):

  #id do sensor
  SENSOR_ID = '0'
  VALUE = 0
  IP = '192.168.15.21'

  def __init__(self, value, id, ip):
    #set sensor initial value and id
    self.VALUE = value
    self.SENSOR_ID = id
    self.IP = ip

  def read_sensor(self):
    #http GET no id do sensor
    return self.VALUE

  def update_led(self, value):
    self.VALUE = value

  def change_led(self, value):
    if value:
       sendToLightClient(self.IP,'0')
    else:
       sendToLightClient(self.IP,'1')
    self.update_led(value)
