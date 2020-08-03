#!/usr/bin/python
"""
Script to print RHSM certificates as JSON output
"""

import json
try:
    from ConfigParser import SafeConfigParser
except ImportError:
    from configparser import ConfigParser as SafeConfigParser

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

print(subscription_manager_cert_paths())
