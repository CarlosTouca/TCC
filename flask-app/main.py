import light
from flask import *

app = Flask(__name__)
#light1 = light.Light(False,'0','192.168.15.21')
#lights = {light1.DEVICE_ID:light1}
lights = {}

def add_device(device_id,ip_str):
    l = light.Light(False,device_id,ip_str)
    lights[device_id] = l

# Index route
@app.route("/")
def index():
  # TODO list lights
  # Render the index.html template passing the value of the sensor
  return render_template('index.html', sensors=lights)

# About route
@app.route("/about")
def about():
  # Render the about.html template
  return render_template('about.html')

# Change LED value POST request.
@app.route("/change_status/<string:guid>/<int:status>", methods=['POST'])
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
@app.route("/change_led_status/<int:status>", methods=['POST'])
def change_led_status(status):
  # Check the value of the parameter
  if status == 0:
      print "not implemented!"
     #light1.change_led(False)
  elif status == 1:
      print "not implemented!"
     #light1.change_led(True)
  else:
    return ('Error', 500)
  return ('', 200)


# Change LED value POST request.
@app.route("/update_led/<int:status>", methods=['GET'])
def update_led(status):
  # Check the value of the parameter
  if status == 0:
      print "not implemented!"
     #light1.update_led(False)
  elif status == 1:
      print "not implemented!"
     #light1.update_led(True)
  else:
    return ('Error', 500)
  return ('', 200)

@app.route("/subscribe/<string:guid>", methods=['GET'])
def subscribe(guid):
    h = request.environ['REMOTE_ADDR']
    print 'New device:' + guid + '@' + h
    add_device (guid,h)
    return ('OK', 200)

# Starts the app listening to port 5000 with debug mode
if __name__ == "__main__":
  app.run(host="0.0.0.0", debug=True)
