#!/usr/bin/python

DOCUMENTATION = r"""
---
module: foreman_scap_client_facts
version_added: 2.0.0
short_description: Gather facts about Red Hat Subscription Manager
description:
    - Gathers facts about Red Hat Subscription Manager from rhsm.conf.
"""

EXAMPLES = r"""
# Gather facts and register to a variable.
- name: Gather foreman_scap_client facts
  foreman_scap_client_facts:
  register: my_foreman_scap_client_facts
"""

RETURN = r"""
paths:
    description: dictionary containing all the facts
    returned: success
    type: complex
    contains:
        rh_ca_cert_path:
            description: Default CA cert to use when generating yum repo configs
            returned: success
            type: str
            sample: /etc/rhsm/ca/katello-server-ca.pem
        rh_consumer_cert_path
            description: Path to the consumer's identity certificate
            returned: success
            type: str
            sample: /etc/pki/consumer/cert.pem
        rh_consumer_key_path
            description: Path to the key for the consumer's identity certificate
            returned: success
            type: str
            sample: /etc/pki/consumer/key.pem
"""

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
