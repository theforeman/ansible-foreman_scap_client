# Ansible role for Foreman SCAP client [![Build Status](https://travis-ci.org/theforeman/ansible-foreman_scap_client.svg?branch=master)](https://travis-ci.org/theforeman/ansible-foreman_scap_client)

Ansible role for Foreman SCAP client configures foreman_scap_client
to run scans and upload results to foreman proxy.

## Configuration

This role will automatically install foreman_scap_client (if not installed),
it will configure /etc/foreman_scap_client/config.yaml with parameters which are needed for the operation
of foreman_scap_client and create a cron which schedules the client execution.

### Variables

* 'foreman_scap_client_state': state of the rubygem-foreman_scap_client package
* 'foreman_scap_client_server': configures the proxy server
* 'foreman_scap_client_port': configures the proxy server's port
* 'foreman_scap_client_policies': Array of policies that should be configured
* 'foreman_scap_client_ca_cert_path': path to file of certification authority that issued client's certificate
* 'foreman_scap_client_host_cert_path': path to host certificate, may be puppet agent certificate or katello certificate
* 'foreman_scap_client_host_private_key_path': path to host private key, may be puppet agent private key or katello private key
* 'foreman_scap_client_release': Which release to configure a repo for
* 'foreman_scap_client_repo_url': URL for the repository with rubygem-foreman_scap_client
* 'foreman_scap_client_repo_state': state of the repository
* 'foreman_scap_client_repo_key': RPM Key source file for foreman-plugins repo. Note: Currently, packages are not signed.
  Unless set to an alternative file source, URL will be used.
* 'foreman_scap_client_repo_gpg': Enable / disable GPG checks
* 'foreman_scap_client_cron_template': path to the cron template
* 'foreman_scap_client_cron_splay_seed': seed for cron task splay time to generate random but idempotent numbers
* 'foreman_scap_client_cron_splay': upper limit for cron tasks splay time
* 'foreman_scap_client_fetch_remote_resources': Whether to fetch referenced resources from remote location
* 'foreman_scap_client_http_proxy_server': HTTP proxy server
* 'foreman_scap_client_http_proxy_port': HTTP proxy port

### Sample Usage

The following example ensures that every week an SCAP audit is executed and the results
are sent to proxy at proxy.example.com:9090. The example will automatically attempt to install
foreman_scap_client on the system. If you do not wish to use your tailoring file with policy,
just pass empty strings to tailoring variables.

```ansible
---
- hosts: all
  become: true
  roles:
    - theforeman.foreman_scap_client
  vars:
    foreman_scap_client_server: https://proxy.example.com
    foreman_scap_client_port: 9090
    foreman_scap_client_policies: [{
      "id": "1",
      "hour": "12",
      "minute": "1",
      "month": "*",
      "monthday": "*",
      "weekday": "1",
      "profile_id": "",
      "content_path": "/usr/share/xml/scap/ssg/fedora/ssg-fedora-ds.xml",
      "download_path": "/compliance/policies/1/content",
      "tailoring_path": "/var/lib/openscap/ssg-fedora-ds-tailored.xml",
      "tailoring_download_path": "/compliance/policies/1/tailoring"
    }]
}
```

### Usage with foreman_openscap

When using this role together with [foreman_openscap](https://theforeman.org/plugins/foreman_openscap/), no further configuration
 should be necessary as values come from Foreman's ENC. However, verify the values for server, port and policies after
 importing the role; they should have overrides enabled and the policies should be `<%= @host.policies_enc %>`

### Testing
Tests are set up to run in Docker using Molecule and Testinfra. Make sure to install dependencies:

```
pip install -r requirements.txt
```

Check if your current user is able to connect to Docker without sudo. If not, create docker group and add your user. To run tests:

```
molecule test
```


### Releasing on ansible-galaxy

Galaxy imports content from GitHub and uses git tags for [versioning](https://galaxy.ansible.com/docs/contributing/version.html). Galaxy expects tags to have semantic version format.
