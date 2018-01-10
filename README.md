# apartmentMonitor
Store and graph Philips Hue Motion, Ambient light, Temperature in combination with outside weather.

### What is it?
Philips sells Hue motion sensors. These sensors collect motion, light and temperature (undocumented). 
- The "get_data" part of this project reads the Hue API, collects the sensor data periodically and saves this in a database.
- In addition to the Hue data, it also collects outside weather data from the Dutch government meteorological institute. This data can be used to compare for example room temperature with outside temperature.
- The server part of this project uses the database to graph and show statistics on the data. Screenshots of a small part of the functionality can be found below.

### Why?
- Collecting data always is fun!
- Knowing if my heating system works correctly
- What is the influence of my curtains on the temperature inside. Should I close them or leave them open?
- Use motion data, ambient light information and outside information to automate my lighting. Learn my behaviour and turn the lights on without me touching it.

### The application
Default graph:

<img src="https://github.com/HyHend/apartmentMonitor/blob/master/img/x_def.png" width="500px" alt="Screenshot">

Graph showing three days:

<img src="https://github.com/HyHend/apartmentMonitor/blob/master/img/x_3d.png" width="500px" alt="Screenshot">

Graph showing temperature and ambient light measurements:

<img src="https://github.com/HyHend/apartmentMonitor/blob/master/img/x_light.png" width="500px" alt="Screenshot">

### Acknowledgements
This project uses:
- Hue API
- Flask
- jsonp.js
- moment.js
- chart.js
- utils.js
- jquery
