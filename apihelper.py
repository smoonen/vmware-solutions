# Issue various VCS GET API calls, printing results and timings
# Requires "requests" module: sudo python3 -m pip install requests

import apikey
import requests, sys, timeit

# Helper for checking response code
def check_results(resp, uri) :
  if resp.status_code not in (200, 202) :
    print("Error %d invoking %s" % (resp.status_code, uri))
    print(resp.text)
    sys.exit(1)
# Helpers for timing and checking a request
def timed_json_get(uri, headers) :
  start = timeit.default_timer()
  resp = requests.get(uri, headers = headers)
  end = timeit.default_timer()
  check_results(resp, uri)
  print('Elapsed: %f' % (end - start))
  return resp.json()
def timed_json_post(uri, params, headers) :
  h2 = headers.copy()
  h2['Content-Type'] = 'application/json'
  start = timeit.default_timer()
  resp = requests.post(uri, json = params, headers = h2)
  end = timeit.default_timer()
  check_results(resp, uri)
  print('Elapsed: %f' % (end - start))
  return resp.json()
def timed_json_patch(uri, params, headers) :
  h2 = headers.copy()
  h2['Content-Type'] = 'application/json'
  start = timeit.default_timer()
  resp = requests.patch(uri, json = params, headers = h2)
  end = timeit.default_timer()
  check_results(resp, uri)
  print('Elapsed: %f' % (end - start))
  return resp.json()
def timed_json_delete(uri, headers) :
  start = timeit.default_timer()
  resp = requests.delete(uri, headers = headers)
  end = timeit.default_timer()
  check_results(resp, uri)
  print('Elapsed: %f' % (end - start))
  return resp.json()

# Authenticate; returning header dictionary
def authenticate() :
  # Exchange API key for access and refresh token; populate header dictionary with this
  headers = { 'Accept' : 'application/json' }
  params = {
    'grant_type' : 'urn:ibm:params:oauth:grant-type:apikey',
    'apikey'     : apikey.APIKEY,
  }
  resp = requests.post('https://iam.bluemix.net/identity/token', data = params, headers = headers)
  check_results(resp, 'https://iam.bluemix.net/identity/token')
  json = resp.json()
  headers['Authorization'] = 'Bearer %s' % json['access_token']
  headers['X-Auth-Refresh-Token'] = json['refresh_token']
  return headers

