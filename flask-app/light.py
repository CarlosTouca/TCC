import sys
import socket
import requests
import json

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

def sendToLightClient (ip,command,value):
	print "send command to client"
	print command
	HOST = ip    	# The remote host
	PORT = '8080'              		# The same port as used by the server
	url = 'http://' + HOST + ':' + PORT + '/' +command+ '/' + str(value)
	r = requests.get(url);
	print r
	print r.content
	response_data = r.content
	#response_data = json.loads(r.content)
	return response_data

def as_light(dct):
  if '__light__' in dct:
    return Light(dct['value'], dct['id'], dct['ip'])
  return dct


#class ComplexEncoder(json.JSONEncoder):
#  def default(self, obj):
#    if isinstance(obj, complex):
#    return [obj.real, obj.imag]
#  return json.JSONEncoder.default(self, obj)

class Light(object):

	#id do sensor
	DEVICE_ID = '0'
	VALUE = 0
	IP = 'localhost'
	FEATURES = {}

	def __init__(self, value, id, ip):
		#set sensor initial value and id
		self.VALUE = value
		self.DEVICE_ID = id
		self.IP = ip

	def read_sensor(self):
		#http GET no id do sensor
		return self.VALUE

	def update_led(self, value):
		self.VALUE = value

	def update_status(self, status):
		# TODO create a generic parser
		sts = int(status['sts'])
		print sts
		if sts == 1:
			self.update_led(1)
		else:
			self.update_led(0)

	def change_led(self, value):
		if value:
			response = sendToLightClient(self.IP, 'gpio','0')
		else:
			response = sendToLightClient(self.IP, 'gpio','1')
			#self.update_status (response)
		return response

	def request(self,variable_name, value):
		response = sendToLightClient(self.IP,variable_name,value)
		#self.update_from_response(response)
		return response

	def update_from_response(self,response):
		dict = json.loads(response)
		for key,value in dict.iteritems():
			#self.FEATURES
			print key + ">" + value


	def __str__(self):
		return '{ \'value\':'+ str(self.VALUE) + ',' +'}'
