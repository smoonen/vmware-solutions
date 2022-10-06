# Issue various order verification API calls, printing results and timings
# Requires "requests" module: sudo python3 -m pip install requests

from __future__ import print_function
import apihelper
import pprint, random, sys, uuid

# Authenticate with IBM Cloud using API key
headers = apihelper.authenticate()

# Get supported DCs
headers['x-global-transaction-id'] = str(uuid.uuid4())
print('Supported data centers (%s)' % headers['x-global-transaction-id'])
data_centers = apihelper.timed_json_get('https://api.vmware-solutions.cloud.ibm.com/v2/locations', headers)
pprint.pprint(data_centers); print()
data_centers = data_centers['locations']

# Get supported CPUs
headers['x-global-transaction-id'] = str(uuid.uuid4())
print('Supported CPU types (%s)' % headers['x-global-transaction-id'])
cpus = apihelper.timed_json_get('https://api.vmware-solutions.cloud.ibm.com/v2/server_types', headers)
pprint.pprint(cpus); print()
cpus = cpus['server_types']

# Get supported RAM
headers['x-global-transaction-id'] = str(uuid.uuid4())
print('Supported RAM types (%s)' % headers['x-global-transaction-id'])
ram = apihelper.timed_json_get('https://api.vmware-solutions.cloud.ibm.com/v2/ram_types', headers)
pprint.pprint(ram); print()
ram = ram['ram_types']

# Get supported disks
headers['x-global-transaction-id'] = str(uuid.uuid4())
print('Spuported disk types (%s)' % headers['x-global-transaction-id'])
disks = apihelper.timed_json_get('https://api.vmware-solutions.cloud.ibm.com/v2/disk_types', headers)
pprint.pprint(disks); print()
disks = disks['disk_types']

# Get supported NFS
headers['x-global-transaction-id'] = str(uuid.uuid4())
print('Supported NFS tiers (%s)' % headers['x-global-transaction-id'])
nfs = apihelper.timed_json_get('https://api.vmware-solutions.cloud.ibm.com/v2/shared_storage_tiers', headers)
pprint.pprint(nfs); print()
nfs = nfs['shared_storage_tiers']

# Get supported vSphere versions
headers['x-global-transaction-id'] = str(uuid.uuid4())
print('Supported vSphere versions (%s)' % headers['x-global-transaction-id'])
vers = apihelper.timed_json_get('https://api.vmware-solutions.cloud.ibm.com/v2/vsphere_versions', headers)
pprint.pprint(vers); print()
vers = vers['vsphere_versions']

# Perform an order verification for an NFS instance
headers['x-global-transaction-id'] = str(uuid.uuid4())
print('Verify NFS instance (%s)' % headers['x-global-transaction-id'])
# Preselect server, RAM, and storage
server = 'INTEL_INTEL_XEON_5218_2_30'
assert(server in [cpu['id'] for cpu in cpus])
server_ram = 'RAM_192_GB_DDR4_2133_ECC_REG'
assert(server_ram in [x['id'] for x in ram])
shared_storage = [x for x in nfs if x['size'] == 'STORAGE_SPACE_FOR_4_IOPS_PER_GB'][0]

# Build order
instance_request = {
  'name'            : 'test01',
  'host_prefix'     : 'host',
  'root_domain'     : 'test1.example.com',
  'vsphere_version' : '7.0',
  'dns_type'        : 'vsi',
  'domain_type'     : 'primary',
  'vcs_type'        : 'vcs_nsx_t',
  'management'      : {
      'cluster_name'        : 'cluster01',
      'quantity'            : 3,
      'location'            : random.choice(data_centers)['id'],
      'networking'          : { 'private_only' : False, },
      'customized_hardware' : {
          'server'      : server,
          'ram'         : server_ram,
          'disk_groups' : [ ],
        },
      'shared_storages' : [ {
          'iops'     : shared_storage['iops'],
          'quantity' : 2,
          'size'     : shared_storage['size'],
          'volume'   : 4000,
        } ],
    },
  'license_keys' : { 'nsx' : { 'license_type' : 'dc_professional' } },
}
result = apihelper.timed_json_post('https://api.vmware-solutions.cloud.ibm.com/v1/vcenters/nsxt?verify_only=true&check_price=true', instance_request, headers)
pprint.pprint(result); print()

# If there is a VCS instance in our account, perform an add cluster verification as well
headers['x-global-transaction-id'] = str(uuid.uuid4())
print('Get vCenter instances (%s)' % headers['x-global-transaction-id'])
vcenters = apihelper.timed_json_get('https://api.vmware-solutions.cloud.ibm.com/v1/vcenters', headers)
if len(vcenters) == 0 :
  sys.exit(0)
# Get instance cluster detail
headers['x-global-transaction-id'] = str(uuid.uuid4())
print('Get network details for first existing cluster (%s)' % headers['x-global-transaction-id'])
vcenter_cluster0_networks = apihelper.timed_json_get('https://api.vmware-solutions.cloud.ibm.com/v1/vcenters/%s/clusters/%s/vlans' % (vcenters[0]['id'], '0'), headers)
# Build order
headers['x-global-transaction-id'] = str(uuid.uuid4())
print('Verify NFS cluster (%s)' % headers['x-global-transaction-id'])
private_vlan            = [x for x in vcenter_cluster0_networks if x['id'] == 'private_vlan'][0]['number']
additional_private_vlan = [x for x in vcenter_cluster0_networks if x['id'] == 'additional_private_vlan'][0]['number']
public_vlan             = [x for x in vcenter_cluster0_networks if x['id'] == 'public_vlan'][0]['number']
cluster_request = {
  'cluster_name'    : 'cluster02',
  'location'        : vcenters[0]['location'],
  'host_prefix'     : 'host',
  'license_keys'    : { },
  'network'         : { 'private_only' : False },
  'networking'      : {
      'private_vlan'            : { 'num': str(private_vlan) },
      'additional_private_vlan' : { 'num': str(additional_private_vlan) },
      'public_vlan'             : { 'num': str(public_vlan) },
  },
  'hardware'        : {
      'quantity'            : 2,
      'customized_hardware' : instance_request['management']['customized_hardware'],
  },
  'shared_storages' : instance_request['management']['shared_storages'],
}
result = apihelper.timed_json_post('https://api.vmware-solutions.cloud.ibm.com/v1/vcenters/%s/clusters?verify_only=true&check_price=true' % vcenters[0]['id'], cluster_request, headers)
pprint.pprint(result); print()

# Perform an add host verification
headers['x-global-transaction-id'] = str(uuid.uuid4())
print('Get clusters (%s)' % headers['x-global-transaction-id'])
clusters = apihelper.timed_json_get('https://api.vmware-solutions.cloud.ibm.com/v1/vcenters/%s/clusters' % vcenters[0]['id'], headers)
if len(clusters) == 0 :
  sys.exit(0)
headers['x-global-transaction-id'] = str(uuid.uuid4())
print('Verify add host (%s)' % headers['x-global-transaction-id'])
addhost_request = {
  'quantity'         : 1,
  'maintenance_mode' : True,
}
result = apihelper.timed_json_post('https://api.vmware-solutions.cloud.ibm.com/v1/vcenters/%s/clusters/%s/hosts?verify_only=true&check_price=true' % (vcenters[0]['id'], clusters[0]['id']), addhost_request, headers)
pprint.pprint(result); print()

# Perform an add storage verification
headers['x-global-transaction-id'] = str(uuid.uuid4())
print('Verify add storage (%s)' % headers['x-global-transaction-id'])
addstorage_request = {
  'shared_storages' : instance_request['management']['shared_storages']
}
result = apihelper.timed_json_post('https://api.vmware-solutions.cloud.ibm.com/v1/vcenters/%s/clusters/%s/shared_storages?verify_only=true&check_price=true' % (vcenters[0]['id'], clusters[0]['id']), addstorage_request, headers)
pprint.pprint(result); print()

