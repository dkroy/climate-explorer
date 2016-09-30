"""Extremely basic unit tests will need to expand."""
from api import get_weather_stations
from google import bq

def test_ip_to_location():
    assert (44.8309, -93.4599) == get_weather_stations('4.30.114.107')


def test_table_data():
    results = {
        'rows': [{u'f': [{u'v': u'staging demo'},
                 {u'v': u'243423423424'}]},
                 {u'f': [{u'v': u'A Company'}, {u'v': u'23v32v3v23v2v3v'}]},
                 {u'f': [{u'v': u'Another Company'}, {u'v': u'23v23v2v2v2rffff'}]},
                 {u'f': [{u'v': u'A Third Company'}, {u'v': u'dfddgf0fgf0gf0gf'}]}],
        'schema': {
            'fields': [{u'mode': u'NULLABLE', u'name': u'billing_account_id', u'type': u'STRING'},
                       {u'mode': u'NULLABLE', u'name': u'api_key', u'type': u'STRING'}]
        }
    }
    expected_data = [{u'billing_account_id': u'staging demo', u'api_key': u'243423423424'},
                     {u'billing_account_id': u'A Company', u'api_key': u'23v32v3v23v2v3v'},
                     {u'billing_account_id': u'Another Company', u'api_key': u'23v23v2v2v2rffff'},
                     {u'billing_account_id': u'A Third Company', u'api_key': u'dfddgf0fgf0gf0gf'}]
    assert expected_data == list(bq.table_data(results))
