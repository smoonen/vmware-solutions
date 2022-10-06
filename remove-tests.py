# Demonstrate (without invoking) API calls to remove various resources.
# Requires "requests" module: sudo python3 -m pip install requests

from __future__ import print_function
import apihelper
import pprint, random, sys, uuid

# Authenticate with IBM Cloud using API key
headers = apihelper.authenticate()

# Search for first instance, first cluster, and obtain its details so that we can enumerate its NFS storage and its hosts.
headers['x-global-transaction-id'] = str(uuid.uuid4())
print('Get vCenter instances (%s)' % headers['x-global-transaction-id'])
vcenters = apihelper.timed_json_get('https://api.vmware-solutions.cloud.ibm.com/v1/vcenters', headers)
if len(vcenters) == 0 :
  sys.exit(0)
headers['x-global-transaction-id'] = str(uuid.uuid4())
print('Get clusters for first instance (%s)' % headers['x-global-transaction-id'])
clusters = apihelper.timed_json_get('https://api.vmware-solutions.cloud.ibm.com/v1/vcenters/%s/clusters' % vcenters[0]['id'], headers)
headers['x-global-transaction-id'] = str(uuid.uuid4())
print('Get cluster details for first cluster of first instance (%s)' % headers['x-global-transaction-id'])
cluster_details = apihelper.timed_json_get('https://api.vmware-solutions.cloud.ibm.com/v1/vcenters/%s/clusters/%s' % (vcenters[0]['id'], clusters[0]['id']), headers)

# Removal of shared storage
print('Shared storage for cluster:')
pprint.pprint(cluster_details['shared_storage']); print()
# Select a known datastore for deletion and then remove it
#selected_datastore = [x for x in cluster_details['shared_storage'] if 'gU5iD' in x['datastore_name']][0]
#nfs_remove_payload = {
#  'action'      : 'delete',
#  'storage_ids' : [selected_datastore['storage_id']],
#}
#headers['x-global-transaction-id'] = str(uuid.uuid4())
#print('Remove NFS datastore (%s)' % headers['x-global-transaction-id'])
#result = apihelper.timed_json_patch('https://api.vmware-solutions.cloud.ibm.com/v1/vcenters/%s/clusters/%s/shared_storages' % (vcenters[0]['id'], clusters[0]['id']), nfs_remove_payload, headers)
#pprint.pprint(result); print()

# Removal of host
print('Hosts for cluster:')
pprint.pprint(cluster_details['hosts']); print()
# Select a known host for removal and then remove it
#selected_host = [x for x in cluster_details['hosts'] if x['name']['hostname'] == 'host004'][0]
#host_remove_payload = {
#  'action' : 'delete',
#  'hosts'  : [selected_host['id']],
#}
#headers['x-global-transaction-id'] = str(uuid.uuid4())
#print('Remove host (%s)' % headers['x-global-transaction-id'])
#result = apihelper.timed_json_patch('https://api.vmware-solutions.cloud.ibm.com/v1/vcenters/%s/clusters/%s/hosts' % (vcenters[0]['id'], clusters[0]['id']), host_remove_payload, headers)
#pprint.pprint(result); print()

# Removal of cluster
#headers['x-global-transaction-id'] = str(uuid.uuid4())
#print('Remove cluster (%s)' % headers['x-global-transaction-id'])
#result = apihelper.timed_json_delete('https://api.vmware-solutions.cloud.ibm.com/v1/vcenters/%s/clusters/%s' % (vcenters[0]['id'], clusters[0]['id']), headers)
#pprint.pprint(result); print()

# Removal of instance
#headers['x-global-transaction-id'] = str(uuid.uuid4())
#print('Remove instance (%s)' % headers['x-global-transaction-id'])
#result = apihelper.timed_json_delete('https://api.vmware-solutions.cloud.ibm.com/v1/vcenters/%s' % vcenters[0]['id'], headers)
#pprint.pprint(result); print()

