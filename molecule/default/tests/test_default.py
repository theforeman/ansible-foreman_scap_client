import os
# import yaml

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


# def test_hosts_file(host):
#     f = host.file('/etc/hosts')

#     assert f.exists
#     assert f.user == 'root'
#     assert f.group == 'root'

def test_foreman_scap_client_config(host):
    file = host.file('/etc/foreman_scap_client/config.yaml')

    assert file.exists

    # with open('/etc/foreman_scap_client/config.yaml') as stream:
    #     config = yaml.safe_load(stream)

    # config["foreman_scap_client_port"]
    # assert len(config["foreman_scap_client"]) == 2
