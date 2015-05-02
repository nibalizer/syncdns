syncyaml
--------


This is a simple script to administrate dns from a yaml file.


Usage:

Export the typical openstack environment variables. If using hp dns use 
export OS_DNS_SERVICE_TYPE=hpext:dns
as well.

Create a dns_config.yaml file, or set DNS_CONFIG_FILE. See example_dns_config.yaml. The top level entry is the name of your domain. The rest are entries.

python syndns.py --noop

If everything looks good:

python syndns.py --noop


