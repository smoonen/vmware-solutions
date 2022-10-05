# Add Endurance file storage (NFS) to the first cluster of the first instance
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

# Add storage to the first cluster (verify and price check only; remove verify parameter to perform actual order)
# First obtain the list of available storage types
print('Get storage tier details')
nfs = apihelper.timed_json_get('https://api.vmware-solutions.cloud.ibm.com/v2/shared_storage_tiers', headers)
nfs = nfs['shared_storage_tiers']
# Select 4 IOPS/GB tier
print('Verify add storage')
shared_storage = [x for x in nfs if x['size'] == 'STORAGE_SPACE_FOR_4_IOPS_PER_GB'][0]
addstorage_request = {
  'shared_storages' : [ {
      'iops'     : shared_storage['iops'],
      'quantity' : 2,
      'size'     : shared_storage['size'],
      'volume'   : 4000,
  } ],
}
result = apihelper.timed_json_post('https://api.vmware-solutions.cloud.ibm.com/v1/vcenters/%s/clusters/%s/shared_storages?verify_only=true&check_price=true' % (vcenters[0]['id'], clusters[0]['id']), addstorage_request, headers)
pprint.pprint(result); print()

