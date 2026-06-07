# Ansible Collection - jcalavia_org.setup

[![codecov](https://codecov.io/gh/calavia-org/ansible-collection-setup/branch/main/graph/badge.svg?token=T5NUI2U885)](https://codecov.io/gh/calavia-org/ansible-collection-setup)
[![Test collection](https://github.com/calavia-org/ansible-collection-setup/actions/workflows/pr.yml/badge.svg)](https://github.com/calavia-org/ansible-collection-setup/actions/workflows/pr.yml)

This Ansbile collection is intended to be used in order to setup:

* git
* vim
* tmux

## Supported platforms

* MacOS
* Ubuntu / Debian

## Development

### Usefull commands

* tox -e unit-py3.12-2.17 --ansible --conf tox-ansible.ini -- junit-xml=tests/reports/unit.xml
* tox -e integration-py3.12-2.17 --ansible --conf tox-ansible.ini -- junit-xml=tests/reports/integration.xml

## Testing Auto-Release
