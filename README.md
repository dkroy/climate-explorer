# Climate Explorer
The climate explorer uses publicly available NOAA GSOD Data to display climate data for the same day each year.

## Install
```
cd scripts
source install.sh
```
## Run
The Docker run instructions are currently disabled, but you can still run the Flask server locally.
```
cd src
python main.py
```

## Deploy
You can deploy this project to the Google Cloud by setting `GOOGLE_KEYFILE`, and `GOOGLE_PROJECT` in the `scripts/deploy.sh` file and running it as shown below.
```
cd scripts
source deploy.sh
```

## Future
* Renable Docker/Docker Compose
* Spark backend leveraging Amazon's new public data in S3.
* Remove depencency on NOAA Web Service for initial Station mapping.
* Use centroids to gather more close weatherstations and average the result to go further back in time for the climate.
* Stitch in current weather.