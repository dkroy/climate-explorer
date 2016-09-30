cd ../src
# Download and unzip the maxmind database
wget -N http://geolite.maxmind.com/download/geoip/database/GeoLite2-City.mmdb.gz \
    && gzip -d GeoLite2-City.mmdb.gz
pip install -r requirements.txt
