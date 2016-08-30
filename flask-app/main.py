import light
from flask import *

app = Flask(__name__)
light1 = light.Light(False,'0','192.168.15.21')
lights = {'0':light1}


# Index route
@app.route("/")
def index():
  # Read the value of the sensor
  value = light1.read_sensor()
  # TODO list lights
  # Render the index.html template passing the value of the sensor
  return render_template('index.html', sensor_value=value)

# About route
@app.route("/about")
def about():
  # Render the about.html template
  return render_template('about.html')

# Change LED value POST request.
@app.route("/change_status/<string:guid>/<int:status>", methods=['GET'])
def change_status(guid,status):
  # Check the value of the parameter
  print "guid" + guid
  l = lights[guid]
  if status == 0:
     l.change_led(False)
  elif status == 1:
     l.change_led(True)
  else:
    return ('Error', 500)
  return ('', 200)


# Change LED value POST request.
@app.route("/change_led_status/<int:status>", methods=['POST'])
def change_led_status(status):
  # Check the value of the parameter
  if status == 0:
     light1.change_led(False)
  elif status == 1:
     light1.change_led(True)
  else:
    return ('Error', 500)
  return ('', 200)


# Change LED value POST request.
@app.route("/update_led/<int:status>", methods=['GET'])
def update_led(status):
  # Check the value of the parameter
  if status == 0:
     light1.update_led(False)
  elif status == 1:
     light1.update_led(True)
  else:
    return ('Error', 500)
  return ('', 200)

@app.route("/subscribe/<string:guid>", methods=['GET'])
def subscribe(guid):
    h = request.environ['REMOTE_ADDR']
    print 'New device:' + guid + '@' + h
    l = light.Light(False,guid,h)
    lights[guid] = l
    print lights
    return ('OK', 200)

# Starts the app listening to port 5000 with debug mode
if __name__ == "__main__":
  app.run(host="0.0.0.0", debug=True)
