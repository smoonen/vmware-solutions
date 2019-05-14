# Issue various order verification API calls, printing results and timings
# Compatible with Python2 and Python3
# Requires "requests" module:
#   py2: sudo pip install requests
#   py3: sudo python3 -m pip install requests

from __future__ import print_function
import apihelper
import pprint, random, sys

# Authenticate with IBM Cloud using API key
headers = apihelper.authenticate()

# Get supported DCs
print('Supported data centers')
data_centers = apihelper.timed_json_get('https://api.vmware-solutions.cloud.ibm.com/v1/locations', headers)
pprint.pprint(data_centers); print()

# Get supported CPUs
print('Supported CPU types')
cpus = apihelper.timed_json_get('https://api.vmware-solutions.cloud.ibm.com/v1/server_types', headers)
pprint.pprint(cpus); print()

# Get supported RAM
print('Supported RAM types')
ram = apihelper.timed_json_get('https://api.vmware-solutions.cloud.ibm.com/v1/ram_types', headers)
pprint.pprint(ram); print()

# Get supported disks
print('Spuported disk types')
disks = apihelper.timed_json_get('https://api.vmware-solutions.cloud.ibm.com/v1/disk_types', headers)
pprint.pprint(disks); print()

# Get supported NFS
print('Supported NFS tiers')
nfs = apihelper.timed_json_get('https://api.vmware-solutions.cloud.ibm.com/v1/shared_storage_tiers', headers)
pprint.pprint(nfs); print()

# Get supported vSphere versions
print('Supported vSphere versions')
vers = apihelper.timed_json_get('https://api.vmware-solutions.cloud.ibm.com/v1/vsphere_versions', headers)
pprint.pprint(vers); print()

# Perform an order verification for an NFS instance
print('Verify NFS instance')
# Preselect server and ensure we choose RAM appropriate for that CPU type
server = random.choice(cpus)['id']
server_ram = random.choice([x for x in ram if server in x['supported_server_types']])['id']
# Preselect Endurance tier
shared_storage = random.choice(nfs)
# Build order
instance_request = {
  'name'            : 'test01',
  'subdomain'       : 'test01',
  'root_domain'     : 'example.com',
  'location'        : random.choice(data_centers)['id'],
  'vsphere_version' : random.choice(vers)['version'],
  'dns_type'        : 'vsi',
  'domain_type'     : 'primary',
  'hardware'        : {
      'quantity'            : 2,
      'customized_hardware' : {
          'server'           : server,
          'ram'              : server_ram,
          'disks'            : [],
          'vsan_cache_disks' : []
        },
    },
  'network'         : {
      'private_only' : False,
    },
  'shared_storages' : [ {
      'iops'     : shared_storage['iops'],
      'quantity' : 2,
      'size'     : shared_storage['size'],
      'volume'   : 4000,
    } ],
}
result = apihelper.timed_json_post('https://api.vmware-solutions.cloud.ibm.com/v1/vcenters?verify_only=true', instance_request, headers)
pprint.pprint(result); print()

# If there is a VCS instance in our account, perform an add cluster verification as well
print('Get vCenter instances')
vcenters = apihelper.timed_json_get('https://api.vmware-solutions.cloud.ibm.com/v1/vcenters', headers)
if len(vcenters) == 0 :
  sys.exit(0)
# Build order
print('Verify NFS cluster')
cluster_request = instance_request.copy()
del cluster_request['name']
del cluster_request['subdomain']
del cluster_request['root_domain']
del cluster_request['vsphere_version']
del cluster_request['dns_type']
del cluster_request['domain_type']
cluster_request['cluster_name']   = 'cluster02'
cluster_request['is_default_pod'] = True
result = apihelper.timed_json_post('https://api.vmware-solutions.cloud.ibm.com/v1/vcenters/%s/clusters?verify_only=true' % vcenters[0]['id'], cluster_request, headers)
pprint.pprint(result); print()

# Perform an add host verification
print('Get clusters')
clusters = apihelper.timed_json_get('https://api.vmware-solutions.cloud.ibm.com/v1/vcenters/%s/clusters' % vcenters[0]['id'], headers)
if len(clusters) == 0 :
  sys.exit(0)
print('Verify add host')
addhost_request = {
  'quantity'         : 1,
  'maintenance_mode' : True,
}
result = apihelper.timed_json_post('https://api.vmware-solutions.cloud.ibm.com/v1/vcenters/%s/clusters/%s/hosts?verify_only=true' % (vcenters[0]['id'], clusters[0]['id']), addhost_request, headers)
pprint.pprint(result); print()

