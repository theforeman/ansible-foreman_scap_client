#!/usr/bin/python

import json
try:
    from ConfigParser import SafeConfigParser
except ImportError:
    from configparser import ConfigParser as SafeConfigParser
from ansible.module_utils.basic import AnsibleModule

def subscription_manager_cert_paths():
    """
    Helper function to fetch certificates path from RHSM configuration
    """
    certs = {}
    cert_name = '/cert.pem'
    key_name = '/key.pem'
    try:
        configparser = SafeConfigParser()
        configparser.read('/etc/rhsm/rhsm.conf')
        certs['rh_ca_cert_path'] = configparser.get('rhsm', 'repo_ca_cert')
        certs['rh_consumer_cert_path'] = configparser.get('rhsm', 'consumercertdir') + cert_name
        certs['rh_consumer_key_path'] = configparser.get('rhsm', 'consumercertdir') + key_name
    except Exception: # pylint: disable=broad-except
        pass
    return json.dumps(certs)

def main():
    module_args = dict()
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False,
    )

    results = subscription_manager_cert_paths()
    module.exit_json(changed=False, paths=results)

if __name__ == '__main__':
    main()
