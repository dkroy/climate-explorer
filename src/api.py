"""Logic to be broken out into api for the application."""
import os
import json
import logging
import geoip2.database

import requests
from redislite import Redis

from config import BASE_DIR, GEOLITE_DATABASE_PATH

db = Redis(os.path.join(BASE_DIR, 'station-locations.db'))  # Should be on a Docker volume.


def ip_to_location(ip_address):
    """Given an ip address and leverage the MaxMind database to return a lat/long."""
    reader = geoip2.database.Reader(GEOLITE_DATABASE_PATH)
    try:
        response = reader.city(ip_address)
        return response.location.latitude, response.location.longitude
    except ValueError as e:
        return {'error': str(e)}


def get_weather(latitude, longitude):
    """Given a latitude and longitude this retrieves the current weather and associated metadata."""
    key = '{0},{1}'.format(latitude, longitude)
    weather = db.get(key)
    if not weather:
        logging.debug("grabbing location for {0},{1} from noaa..".format(latitude, longitude))
        url = 'http://forecast.weather.gov/MapClick.php?lat={0}&lon={1}&FcstType=json'
        weather = requests.get(url.format(latitude, longitude)).json()
        weather = json.dumps(weather)
        db.set(key, unicode(weather))
    return json.loads(weather)


def get_weather_stations(ip_address):
    """
    stations.call == id (May return more than one like KFCM)
    """
    weather_response = get_weather(*ip_to_location(ip_address))
    return weather_response['currentobservation']['id']

if __name__ == '__main__':
    lat_lon = ip_to_location('4.30.114.107')
    print lat_lon
    weather_response = get_weather(*lat_lon)
    print weather_response
