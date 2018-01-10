from __future__ import division
from flask import Flask
from flask import request
import json
import sys
import sqlite3
import time
import datetime
import socket
from StringIO import StringIO

# Run: export FLASK_APP=api.py
#      flask run --host=0.0.0.0

app = Flask(__name__, static_url_path='')
app.config['DEBUG'] = False
DB = "/home/pi/hue_data/hue_data.db"
DB_TABLE = "hue_results"
DEFAULT_CALLBACK_FUNC = "apiCallback"

app.sqlite = sqlite3.connect(DB)

# @app.route('/')
# def base_level():
#   return 'No parameters given'

@app.route('/api', methods=['GET'])
def api_base():
  # Parse callback name. If not found take default
  callbackFunc = DEFAULT_CALLBACK_FUNC

  # return
  return """{0}({{
    "tmp":"mock"
  }});""".format(callbackFunc)

@app.route('/api/sensors', methods=['GET'])
def api_sensors():
  """ Returns all available sensors, their name, ID
  """

  # Parse callback name. If not found take default
  callbackFunc = request.args.get("callback")
  if not callbackFunc:
    callbackFunc = DEFAULT_CALLBACK_FUNC

  # Retrieve sensors
  cur = app.sqlite.cursor()
  query = """
      SELECT 
        DISTINCT('"' || device_uid || '":"' || device_name || '"') AS device
        FROM {0};
    """.format(DB_TABLE)

  # Execute query
  cur.execute(query)      
  rows = cur.fetchall()

  # Parse and return
  sensors = []
  for row in rows:
    sensors.append(row[0])
  return "{0}({{ \"sensors\":{{{1}}} }});".format(callbackFunc, ','.join(sensors))

@app.route('/api/sensors/<sensor_id>', methods=['GET'])
def api_sensor(sensor_id):
  """ Returns all datapoints for given sensor
  """

  # Parse callback name. If not found take default
  callbackFunc = request.args.get("callback")
  if not callbackFunc:
    callbackFunc = DEFAULT_CALLBACK_FUNC

  # Retrieve sensor data
  cur = app.sqlite.cursor()
  query = """
      SELECT 
        device_name,
        value,
        value_timestamp
        FROM {0}
        WHERE device_uid = '{1}';
    """.format(DB_TABLE, sensor_id)

  # Execute query
  cur.execute(query)
  rows = cur.fetchall()

  # Parse and return
  device_name = ""
  sensor_values = []
  for row in rows:
    device_name = row[0]

    # Parse value and special cases
    value = row[1]
    if "temperature" in row[0].lower() or "temperature" in row[2].lower():
      try:
        value = float(value)/100
      except:
        pass
    if "True" in str(value):
      value = 1
    if "False" in str(value):
      value = 0
    if "none" in str(value).lower():
      value = 0
    if "light" in row[0].lower() or "light" in row[2].lower():
      try:
        value = float(value)/1000
      except:
        pass

    # Sensors emit None when turned off. Ignore
    if not "none" in str(row[2]).lower() and value != "":
      sensor_values.append("\"{0}\":{1}".format(row[2], value))

  return """{0}({{
    "sensor_id":"{1}",
    "sensor_name":"{2}",
    "values":{{{3}}}
  }});""".format(callbackFunc, sensor_id, device_name, ','.join(sensor_values))

@app.route('/api/sensors/<sensor_id>/<start>/<end>', methods=['GET'])
def api_sensor_in_timeframe(sensor_id, start, end):
  """ Returns all datapoints for given sensor between unixtime start, end
  """

  # Parse callback name. If not found take default
  callbackFunc = request.args.get("callback")
  if not callbackFunc:
    callbackFunc = DEFAULT_CALLBACK_FUNC

  # Retrieve sensor data
  cur = app.sqlite.cursor()
  query = """
      SELECT 
        device_name,
        value,
        value_timestamp
        FROM {0}
        WHERE device_uid = '{1}'
        AND polling_timestamp BETWEEN {2} AND {3};
    """.format(DB_TABLE, sensor_id, start, end)

  # Execute query
  cur.execute(query)
  rows = cur.fetchall()

  # Parse and return
  device_name = ""
  sensor_values = []
  for row in rows:
    device_name = row[0]

    # Parse value and special cases
    value = row[1]
    if "temperature" in row[0].lower() or "temperature" in row[2].lower():
      try:
        value = float(value)/100
      except:
        pass
    if "True" in str(value):
      value = 1
    if "False" in str(value):
      value = 0
    if "none" in str(value).lower():
      value = 0
    if "light" in row[0].lower() or "light" in row[2].lower():
      try:
        value = float(value)/1000
      except:
        pass

    # Sensors emit None when turned off. Ignore
    if not "none" in str(row[2]).lower() and value != "":
      sensor_values.append("\"{0}\":{1}".format(row[2], value))

  return """{0}({{
    "sensor_id":"{1}",
    "sensor_name":"{2}",
    "values":{{{3}}}
  }});""".format(callbackFunc, sensor_id, device_name, ','.join(sensor_values))