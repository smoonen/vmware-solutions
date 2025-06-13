# vmware-solutions

Sample Python code and helper routines for invoking IBM Cloud for VMware Solutions APIs.

API documentation for self-managed VMware: https://cloud.ibm.com/apidocs/vmware-solutions

API documentation for VCFaaS: https://cloud.ibm.com/apidocs/vmware-service

Prerequisite: create an IBM Cloud API key and add it to `apikey.py` in the following form:

```
# IBM Cloud API key
APIKEY = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
```

This API key may be a personal one or for a service ID. The ID to which the API key belongs
must be granted appropriate permissions to *VMware Solutions* resources or *VCF as a Service*
resources you wish to view or manage.

