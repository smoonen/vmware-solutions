# Sample script demonstrating how to login to Cloud Director APIs using your IBM Cloud OAuth token
# This script generates a Director API token for each Director site which you could use for subsequent automation like Terraform
# Requires "requests" module: python3 -m pip install requests

import apihelper
import requests, pprint, sys, urllib.parse

# Authenticate with IBM Cloud using API key
headers = apihelper.authenticate()

# Iterate through each known region. Not all regions have VCFaaS deployed.
cat = requests.get('https://globalcatalog.cloud.ibm.com/api/v1?q=vmware.directorsite', headers = headers).json()
regions = cat['resources'][0]['geo_tags']

# Collect all orgs (site URLs) in all regions by first locating all VDCs
sites = set()
for region in regions :
  vdcs = requests.get(f"https://api.{region}.vmware.cloud.ibm.com/v1/vdcs", headers = headers).json()
  for vdc in vdcs['vdcs'] :
    url = urllib.parse.urlparse(vdc['director_site']['url'])

    # Extract the Director base URL and the org name from the tenant URL
    siteurl = url._replace(path='').geturl()
    org = url.path.replace('/tenant/', '')

    sites.add((siteurl, org))

# Iterate through the sites/orgs
for site in sites :
  print(f"Site: '{site[0]}' / Organization '{site[1]}'")

  # Generate a Cloud Director set of login headers from the IBM Cloud bearer token
  # See: https://techdocs.broadcom.com/us/en/vmware-cis/cloud-director/vmware-cloud-director/10-6/-vcloud-api-programming-guide-for-service-providers-10-6/exploring-the-cloud-api/create-a-session-container-api/create-a-session-oauth-api.html

  login_headers = { 'Accept' : 'application/*;version=39.0',
                    'Authorization' : f"{headers['Authorization']}; org={site[1]}" }
  login = requests.post(f"{site[0]}/cloudapi/1.0.0/sessions", headers = login_headers)

  # The result should have a bearer token we can use on subsequent calls
  director_headers = { 'Accept' : 'application/*;version=39.0',
                       'Authorization' : f"{login.headers['X-VMWARE-VCLOUD-TOKEN-TYPE']} {login.headers['X-VMWARE-VCLOUD-ACCESS-TOKEN']}" }

  # Create a Director API token for this site; first register a client
  json = { 'client_name' : 'mytoken' }
  client = requests.post(f"{site[0]}/oauth/tenant/{site[1]}/register", json = json, headers = director_headers).json()

  if 'error' in client :
    print(f"  Error creating OAuth client: {client['error_description']}")
  else :
    # Generate a refresh token for this client; note this is form encoded rather than JSON
    data = { 'grant_type' : 'urn:ietf:params:oauth:grant-type:jwt-bearer',
             'client_id' : client['client_id'],
             'assertion' : login.headers['X-VMWARE-VCLOUD-ACCESS-TOKEN'] }
    token = requests.post(f"{site[0]}/oauth/tenant/{site[1]}/token", data = data, headers = director_headers).json()
    print(f"  token: {token['refresh_token']}")

