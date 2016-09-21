import light
import json
import io
from flask import *

app = Flask(__name__)
#light1 = light.Light(False,'0','192.168.15.21')
#lights = {light1.DEVICE_ID:light1}
# lights = {}

DATABASE_FILE_NAME = "dump.js"

def load_database(devices):
    #devices = {}
    try:
        f = open(DATABASE_FILE_NAME)
        dict = json.loads(f.read())
        for key,value in dict.iteritems():
            l = light.Light(False,"","")
            l.DEVICE_ID = value["DEVICE_ID"].encode('ascii')
            l.IP = value["IP"].encode('ascii')
            l.VALUE = value["VALUE"]
            l.FEATURES = value["FEATURES"]
            ascii_key = key.encode('ascii')
            devices[ascii_key] = l
    except IOError:
        print "IOError Reading Database"
        #devices = {}
    except ValueError:
        print "ValueError Reading Database"
        f.close()
    f.close()


def update_database (devices):
    # TODO try to make some simple cacheing treatment
    # maybe a structure with a flag indicating modification made
    print devices
    f = open(DATABASE_FILE_NAME,"w")
    d = {}
    for key, value in devices.iteritems():
        d[key] = value.__dict__
    print d
    dump = json.dumps(d)
    f.write(dump)
    f.close()

# def zero_database ():
#     lights = {}
#     update_database(lights)

def add_device(device_id,ip_str,json_encoded_features):
    l = light.Light(False,device_id,ip_str)
    try:
        l.FEATURES = json.loads(json_encoded_features)
    except IOError:
        l.FEATURES = { 'gpio':'bool' }
    except ValueError:
        l.FEATURES = { 'gpio':'bool' }
    lights[device_id] = l
    update_database(lights)

# Index route
@app.route("/")
def index():
  if lights:
      print "calling lights from index"
      print lights
  else:
      print "lights is null"
      print lights
  # Render the index.html template passing the value of the sensor
  return render_template('index.html', sensors=lights)

# About route
@app.route("/about")
def about():
  # Render the about.html template
  return render_template('about.html')

@app.route("/<string:guid>", methods=['GET'])
def detail(guid):
    light = lights[guid]
    return render_template('device.html', device=light)

@app.route("/update/<string:guid>/<string:variable_name>/<int:status>", methods=['POST','GET'])
def custom_command(guid,variable_name,status):
    print "custom command received: " + str(status)
    return "custom command received: " + str(status) 


# Change LED value POST request.
@app.route("/change_status/<string:guid>/<int:status>", methods=['POST','GET'])
def change_status(guid,status):
  # Check the value of the parameter
  print "guid" + guid
  l = lights[guid]
  if status == 0:
     response = l.change_led(False)
  elif status == 1:
     response = l.change_led(True)
  else:
    return ('Error', 500)
  print l.read_sensor()
  #status = int(response['sts'])
  status = 1
  if status == 1:
      on = True
  else:
      on = False
  return render_template('status.html', value=on, raw=str(response))
  #return ('{sts:'+str(l.read_sensor())+'}', 200)


# Change LED value POST request.
@app.route("/update_status/<string:guid>/<int:status>", methods=['POST','GET'])
def update_status(guid,status):
  # Check the value of the parameter
  print "guid" + guid
  l = lights[guid]
  if status == 0:
     response = l.update_led(False)
  elif status == 1:
     response = l.update_led(True)
  else:
    return ('Error', 500)
  return ('', 200)

@app.route("/subscribe/<string:guid>", methods=['GET','POST'])
def subscribe(guid):
    h = request.environ['REMOTE_ADDR']
    print 'New device:' + guid + '@' + h
    print request.__dict__
    print request.data
    add_device (guid,h,request.data)
    return ('OK', 200)

# Starts the app listening to port 5000 with debug mode
if __name__ == "__main__":
  # read data from file (lights)
  global lights
  lights = {}
  load_database(lights)
  app.run(host="0.0.0.0", debug=True)
