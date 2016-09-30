import os
import datetime

import flask
from flask import request, jsonify, render_template
from flask.ext.cors import CORS

from api import get_weather_stations
from queries import climate_query

ENV = os.environ.get('ENVIRONMENT', 'development')

app = flask.Flask(__name__)
cors = CORS(app)
app.url_map.strict_slashes = False


@app.route("/data.csv", methods=["GET"])
def data():
    ip_address = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    weather_stations = get_weather_stations(ip_address)
    yearly_temps = climate_query(weather_stations, dt=datetime.datetime.now())
    csv = 'Day,Temp\n' + '\n'.join(map(lambda x: ','.join(x), yearly_temps))
    return csv, 200


@app.route("/", methods=["GET"])
def home():
    return render_template('index.html')


@app.route("/info", methods=["GET"])
def info():
    ip_address = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    weather_stations = get_weather_stations(ip_address)
    return jsonify({'ip': ip_address,
                    'weather_stations': weather_stations}), 200

if __name__ == '__main__':
    if ENV == 'production':
        app.run(host='0.0.0.0', debug=False, threaded=True, port=8080)
    else:
        app.run(host='0.0.0.0', debug=True, threaded=True, port=8085)
