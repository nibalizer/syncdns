import os
import yaml

from designateclient.v1 import Client

# get credentials from environment
auth_url = os.environ.get("OS_AUTH_URL")
username = os.environ.get("OS_USERNAME")
password = os.environ.get("OS_PASSWORD")
tenant_id = os.environ.get("OS_TENANT_ID")
service_type = os.environ.get("OS_DNS_SERVICE_TYPE") # this is probably hpext:dns

# read yaml configuration file
config_file = os.environ.get("DNS_CONFIG_FILE")
if config_file is None:
    config_file = "dns_config.yaml"
with open(config_file) as f:
    config = yaml.load(f.read())
f.closed



# Create an instance of the client, providing the necessary credentials
client = Client(
    auth_url=auth_url,
    username=username,
    password=password,
    tenant_id=tenant_id,
    service_type=service_type
)

# Fetch a list of the domains this user/tenant has access to
domains = client.domains.list()

# Iterate the list, printing some useful information
for domain in domains:
    print "Domain ID: %s, Name: %s" % (domain.id, domain.name)
    if config.get(domain.name) is not None:
        print "Found Domain in Config"
    else:
        break
    print "Printing Records found in designate"
    records = client.records.list(domain.id)
    for record in records:
        print "Type: %s, Data: %s, Name: %s" % (record.type, record.data, record.name)
    print "Printing Records found in config"
    records = config.get(domain.name)
    for record in records:
        print "Type: %s, Data: %s, Name: %s" % (record['type'], record['data'], record['name'])




