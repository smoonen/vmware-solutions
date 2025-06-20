# Sample script demonstrating how to login to Cloud Director APIs using your IBM Cloud OAuth token
# This script fetches a list of all vApps in each Cloud Director instance to which you have access
# Requires "requests" module: python3 -m pip install requests

import apihelper
import requests, pprint, sys, urllib.parse
import xml.dom.minidom

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

  # Query the list of vApps at this site
  vapps = requests.get(f"{site[0]}/api/query?type=vApp", headers = director_headers)
  doc = xml.dom.minidom.parseString(vapps.text)
  for vapp in doc.getElementsByTagName('VAppRecord') :
    print(f"  vApp: {vapp.getAttribute('name')}")

