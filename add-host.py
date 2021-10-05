# Add a host to the first cluster of the first instance
# Requires "requests" module: sudo python3 -m pip install requests

from __future__ import print_function
import apihelper
import pprint, random, sys

# Authenticate with IBM Cloud using API key
headers = apihelper.authenticate()

# Retrieve the list of VCS instances
print('Get vCenter instances')
vcenters = apihelper.timed_json_get('https://api.vmware-solutions.cloud.ibm.com/v1/vcenters', headers)
if len(vcenters) == 0 :
  sys.exit(0)

# Retrieve the list of clusters for the first instance
print('Get clusters')
clusters = apihelper.timed_json_get('https://api.vmware-solutions.cloud.ibm.com/v1/vcenters/%s/clusters' % vcenters[0]['id'], headers)
if len(clusters) == 0 :
  sys.exit(0)

# Add a host to the first cluster (verify and price check only; remove verify parameter to perform actual order)
print('Verify add host')
addhost_request = {
  'quantity'         : 1,
  'maintenance_mode' : True,
}
result = apihelper.timed_json_post('https://api.vmware-solutions.cloud.ibm.com/v1/vcenters/%s/clusters/%s/hosts?verify_only=true&check_price=true' % (vcenters[0]['id'], clusters[0]['id']), addhost_request, headers)
pprint.pprint(result); print()

