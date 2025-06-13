# Retrieve the list of VCFaaS sites, both single-tenant and multi-tenant, and their pVDCs
# Requires "requests" module: sudo python3 -m pip install requests

import apihelper
import requests, pprint, sys

# Authenticate with IBM Cloud using API key
headers = apihelper.authenticate()

# Iterate through each known region. Not all regions have VCFaaS deployed.
cat = requests.get('https://globalcatalog.cloud.ibm.com/api/v1?q=vmware.directorsite', headers = headers).json()
regions = cat['resources'][0]['geo_tags']

for region in regions :
  sites = requests.get(f"https://api.{region}.vmware.cloud.ibm.com/v1/director_sites", headers = headers).json()
  for site in sites['director_sites'] :
    print(f"Site '{site['name']}', ID {site['id']}, in region {region}")
    for pvdc in site['pvdcs'] :
      provider_type = ', '.join([x['name'] for x in pvdc['provider_types']])
      print(f"  pVDC '{pvdc['name']}', ID {pvdc['id']}, in location {pvdc['data_center_name']} supporting provider types: {provider_type}")

  sites = requests.get(f"https://api.{region}.vmware.cloud.ibm.com/v1/multitenant_director_sites", headers = headers).json()
  for site in sites['multitenant_director_sites'] :
    print(f"Site '{site['name']}', ID {site['id']}, in region {region}")
    for pvdc in site['pvdcs'] :
      provider_type = ', '.join([x['name'] for x in pvdc['provider_types']])
      print(f"  pVDC '{pvdc['name']}', ID {pvdc['id']}, in location {pvdc['data_center_name']} supporting provider types: {provider_type}")

