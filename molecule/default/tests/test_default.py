import os
import yaml
import re

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_foreman_scap_client_package(host):
    assert host.package('rubygem-foreman_scap_client.noarch').is_installed


def test_foreman_scap_client_config(host):
    file_path = '/etc/foreman_scap_client/config.yaml'
    file = host.file(file_path)

    assert file.exists
    assert file.contains(':fetch_remote_resources: true')

    config = yaml.load(file.content_string)

    assert config[":port"] == 9090
    assert config[":server"] == 'https://foreman.example.com'
    assert config[":timeout"] == 61

    assert config[':http_proxy_server'] == 'https://proxy.example.com'
    assert config[':http_proxy_port'] == 7475
    assert (config[1][":profile"] is None)

    assert (config[1][":content_path"] ==
            "/usr/share/xml/scap/ssg/fedora/ssg-fedora-ds.xml")
    assert (config[1][":download_path"] ==
            "/compliance/policies/1/content")
    assert (config[1][":tailoring_path"] ==
            "/var/lib/openscap/ssg-fedora-ds-tailored.xml")
    assert (config[1][":tailoring_download_path"] ==
            "/compliance/policies/1/tailoring")
    assert config[':ca_file'] == '/etc/rhsm/ca/redhat-uep.pem'
    assert config[':host_certificate'] == '/etc/pki/consumer/cert.pem'
    assert config[':host_private_key'] == '/etc/pki/consumer/key.pem'


def test_foreman_scap_client_cron(host):
    file_path = '/etc/cron.d/foreman_scap_client_cron'
    file = host.file(file_path)

    assert file.exists

    cron = file.content_string

    assert re.match(
        r'1 12 \* \* 1 root /bin/sleep \d+; /usr/bin/foreman_scap_client 1 2>&1 | logger -t foreman_scap_client',
        cron.split('\n')[-1]
    )
