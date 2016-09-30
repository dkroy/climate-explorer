import os

BASE_DIR = os.path.dirname(__file__)
GEOLITE_DATABASE_PATH = os.path.realpath(os.path.join(BASE_DIR, 'GeoLite2-City.mmdb'))
GOOGLE_KEYFILE = os.path.abspath('mazon-io.json')
