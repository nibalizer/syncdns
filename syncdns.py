import sys
import os
import yaml

from designateclient.v1 import Client
from designateclient.v1.records import Record


def sync_record(config_record, domain_id, records_map, noop):
    c = config_record
    # Handle existence
    if records_map.get(config_record['name']) is None:
        print "Record does not exist, creating"

        new_record = Record(name=c['name'], type=c['type'], data=c['data'])
        if noop:
            print "Would have created a new record: {0}".format(new_record)
        else:
            print "Creating a new record: {0}".format(new_record)
            new_record = client.records.create(domain_id, new_record)
        return;

    # Handle update
    designate_record = client.records.get(domain.id, records_map[config_record['name']])
    d = designate_record
    if (d.type == c['type'] and d.data == c['data']):
        print "Record is already in sync, noop"
    else:
        print "Record is not in sync, updating"
        d.type = c['type']
        d.data = c['data']
        if noop:
            print "Would have pushed an update to the record: {0}".format(d)
        else:
            print "Pushing an update to the record: {0}".format(d)
            d  = client.records.update(domain_id, d)




if __name__ == "__main__":

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

    # proccess command line ops
    if '--noop' in sys.argv:
        print "Running in noop mode"
        noop = True
    else:
        noop = False

    # Create an instance of the client
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
        records_map = {}
        records = client.records.list(domain.id)
        for record in records:
            print "Type: %s, Data: %s, Name: %s" % (record.type, record.data, record.name)
            records_map[record.name] = record.id
        print "Printing Records found in config"
        records = config.get(domain.name)
        for record in records:
            print "Type: %s, Data: %s, Name: %s" % (record['type'], record['data'], record['name'])
        print "Syncing DNS with Config file"
        config_records = config.get(domain.name)
        for config_record in config_records:
            c = config_record
            print "Type: %s, Data: %s, Name: %s" % (c['type'], c['data'], c['name'])
            sync_record(config_record, domain.id, records_map, noop=noop)





