"""
Add the cloud favicons to the chart also.
"""
import time
import datetime
from google import bq

from config import GOOGLE_KEYFILE

climate_query_template = """\
SELECT * FROM (SELECT * FROM TABLE_QUERY([bigquery-public-data:noaa_gsod], 'table_id LIKE "gsod%"'))
WHERE mo = '{1:%m}'
AND da = '{1:%d}'
AND wban in (SELECT wban FROM [bigquery-public-data:noaa_gsod.stations] stations
  WHERE stations.call = '{0}')
AND stn IN (SELECT usaf stn FROM [bigquery-public-data:noaa_gsod.stations] stations
  WHERE stations.call = '{0}')
ORDER BY year DESC
"""


def climate_query(station_call, dt=None):
    """
    Retreives GSOD Data from the BigQuery Public dataset. (About $0.12 a day to cache if queried)
    """
    dt = dt if dt else datetime.datetetime.now()
    climate_query = climate_query_template.format(station_call, dt)
    client = bq.get_client(keyfile=GOOGLE_KEYFILE)
    job_id = bq.query_job(climate_query, client=client)
    job = bq.get_job(job_id, client=client)
    while not bq.get_table_data(job, client=client):
        job = bq.get_job(job_id, client=client)
        time.sleep(5)
    d = bq.get_table_data(job, client=client)
    yearly_temps = map(lambda x: ('{0}-{1}-{2}'.format(x['year'], x['mo'], x['da']), x['temp']), d)
    return yearly_temps

if __name__ == '__main__':
    climate_query("ENSO", dt=datetime.datetime.now())
