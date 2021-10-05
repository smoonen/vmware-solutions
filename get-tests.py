# Issue various VCS GET API calls, printing results and timings
# Requires "requests" module: sudo python3 -m pip install requests

from __future__ import print_function
import apihelper
import pprint, sys

# Authenticate with IBM Cloud using API key
headers = apihelper.authenticate()

# Get vcenters
print('vCenters')
json = apihelper.timed_json_get('https://api.vmware-solutions.cloud.ibm.com/v1/vcenters', headers)
pprint.pprint(json); print()
if len(json) == 0 :
  # No vCenters in account
  sys.exit(0)
vcenter_id = json[0]['id']

print('vCenter[0] details')
json = apihelper.timed_json_get('https://api.vmware-solutions.cloud.ibm.com/v1/vcenters/%s' % vcenter_id, headers)
pprint.pprint(json); print()

print('vCenter[0] instance history')
json = apihelper.timed_json_get('https://api.vmware-solutions.cloud.ibm.com/v1/vcenters/%s/history' % vcenter_id, headers)
pprint.pprint(json); print()

print('vCenter[0] clusters')
json = apihelper.timed_json_get('https://api.vmware-solutions.cloud.ibm.com/v1/vcenters/%s/clusters' % vcenter_id, headers)
pprint.pprint(json); print()
if len(json) == 0 :
  # No clusters in instance
  sys.exit(0)
cluster_id = json[0]['id']

print('vcenter[0] clusters[0]')
json = apihelper.timed_json_get('https://api.vmware-solutions.cloud.ibm.com/v1/vcenters/%s/clusters/%s' % (vcenter_id, cluster_id), headers)
pprint.pprint(json); print()

print('vcenter[0] clusters[0] network details')
json = apihelper.timed_json_get('https://api.vmware-solutions.cloud.ibm.com/v1/vcenters/%s/clusters/%s/vlans' % (vcenter_id, cluster_id), headers)
pprint.pprint(json); print()

