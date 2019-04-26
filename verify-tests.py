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

# Perform a verification for an NFS instance
print('Verify NFS instance')
# Preselect server and ensure we choose RAM appropriate for that CPU type
server = random.choice(cpus)['id']
server_ram = random.choice([x for x in ram if server in x['supported_server_types']])['id']
# Preselect Endurance tier
shared_storage = random.choice(nfs)
request = {
  'name'            : 'test01',
  'subdomain'       : 'test01',
  'root_domain'     : 'example.com',
  'location'        : random.choice(data_centers)['id'],
  'vsphere_version' : random.choice(vers)['version'],
  'dns_type'        : 'vsi',
  'domain_type'     : 'primary',
  'hardware'        : {
      'template_id'         : "1",
      'quantity'            : 2,
      'customized_hardware' : {
          'server'           : server,
          'ram'              : server_ram,
          'disks'            : [],
          'vsan_cache_disks' : []
        },
    },
  'shared_storages' : [ {
      'iops'     : shared_storage['iops'],
      'quantity' : 2,
      'size'     : shared_storage['size'],
      'volume'   : 4000,
    } ],
}
result = apihelper.timed_json_post('https://api.vmware-solutions.cloud.ibm.com/v1/vcenters?verify_only=true', request, headers)
pprint.pprint(result); print()
sys.exit(0)
#curl -i -H "Content-Type:application/json" -H "Authorization: $TOKEN" -H "ibm_id:smoonen@us.ibm.com" -X POST -d '{"dns_type": "vsi","domain_type":"primary","hardware":{"customized_hardware":{"disks":[],"ram":"RAM_64_GB_DDR4_2133_ECC_NON_REG","server":"INTEL_INTEL_XEON_4110_2_10"},"template_id": "1","quantity": 2},"host_prefix": "host","license_keys":{"nsx":{"key":"","license_type":"base"},"vcenter":{"key":""},"vsphere":{"key":""}}, "location":"dal10","name":"vcs01dal","root_domain":"example.com","shared_storage":{"iops": "LOW_INTENSITY_TIER_Max_12000","quantity": 1,"size": "STORAGE_SPACE_FOR_025IOPS_PER_GB_Max_100","volume":1000},"subdomain":"vcs01dal","vsphere_version":"6.7"}' https://api.vmware-solutions.cloud.ibm.com/v1/vcenters?verify_only=true

# Get vcenters
print('vCenters')
json = apihelper.timed_json_request('https://api.vmware-solutions.cloud.ibm.com/v1/vcenters', headers)
pprint.pprint(json); print()
if len(json) == 0 :
  # No vCenters in account
  sys.exit(0)
vcenter_id = json[0]['id']

print('vCenter[0] details')
json = apihelper.timed_json_request('https://api.vmware-solutions.cloud.ibm.com/v1/vcenters/%s' % vcenter_id, headers)
pprint.pprint(json); print()

print('vCenter[0] clusters')
json = apihelper.timed_json_request('https://api.vmware-solutions.cloud.ibm.com/v1/vcenters/%s/clusters' % vcenter_id, headers)
pprint.pprint(json); print()
if len(json) == 0 :
  # No clusters in instance
  sys.exit(0)
cluster_id = json[0]['id']

print('vcenter[0] clusters[0]')
json = apihelper.timed_json_request('https://api.vmware-solutions.cloud.ibm.com/v1/vcenters/%s/clusters/%s' % (vcenter_id, cluster_id), headers)
pprint.pprint(json); print()

