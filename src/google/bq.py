import logging

import httplib2
from apiclient.discovery import build
from oauth2client.client import GoogleCredentials
from oauth2client.service_account import ServiceAccountCredentials

credentials = None


def get_client(keyfile=None):
    credentials = GoogleCredentials.get_application_default()
    if keyfile:
        scopes = [
            'https://www.googleapis.com/auth/bigquery'
        ]
        credentials = ServiceAccountCredentials.from_json_keyfile_name(keyfile, scopes)

    http = httplib2.Http()
    http = credentials.authorize(http)

    return build('bigquery', 'v2', http=http)


def table_data(results):
    schema = results['schema']['fields']
    rows = [map(lambda x:x['v'], x['f']) for x in results['rows']]
    for row in rows:
        a = {}
        for index, col_dict in enumerate(schema):
            a[col_dict['name']] = row[index]
        yield a


def get_table_data(job, client=None):
    if not client:
        client = get_client()
    if job['status'].get('state') == 'DONE' and not job['status'].get('errors'):
        results = client.jobs().getQueryResults(**job['jobReference']).execute()
        return list(table_data(results))


def query_job(query, project_id='mazon-io', client=None):
    if not client:
        client = get_client()
    job = {
        'projectId': project_id,
        'configuration': {
            'query': {
                'query': query
            }
        }
    }
    current_job = client.jobs().insert(projectId=project_id, body=job).execute()
    job_id = current_job['jobReference']['jobId']
    return job_id


def get_job(job_id, project_id='mazon-io', client=None):
    if not client:
        client = get_client()
    return client.jobs().get(projectId=project_id, jobId=job_id).execute()

