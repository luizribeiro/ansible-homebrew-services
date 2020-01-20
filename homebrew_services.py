#!/usr/bin/python

# Copyright: (c) 2020, Luiz Ribeiro <luizribeiro@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from ansible.module_utils.basic import *
from ansible.module_utils.urls import open_url
import json
import tarfile
import os
import os.path
import tempfile
import urllib.parse


DOCUMENTATION = '''
---
module: homebrew_services
short_description: Manage services from Homebrew
description:
    - Manage services from Homebrew (brew services)
author:
    - Luiz Ribeiro <luizribeiro@gmail.com>
options:
    name:
        description:
            - Name or the service(s) to start or stop.

    state:
        description:
            - started/stopped are idempotent actions that will not run commands unless necessary.
        default: auto
        choices: [ started, stopped ]
'''


EXAMPLES = '''
- name: collectd service is enabled
  homebrew_services:
    name: collectd
    state: started
  become: yes
'''


def get_services(module):
    _rc, stdout, _stderr = module.run_command(['brew', 'services', 'list'], check_rc=True)
    services = {}
    for line in stdout.split("\n")[1:-1]:
        name, status, user, plist = (line.split() + [None]*2)[:4]
        services[name] = {
            "state": status,
            "user": user,
            "plist": plist,
            "enabled": plist and "/Library/" in plist,
        }
    return services


SERVICE_COMMANDS = {
    'started': ['brew', 'services', 'start'],
    'stopped': ['brew', 'services', 'stop'],
}


def main():
    module = AnsibleModule(
        argument_spec={
            'name': {
                'type': 'str',
            },
            'state': {
                'choices': ['started', 'stopped'],
            },
        },
        supports_check_mode=True
    )

    service_name = module.params['name']
    desired_state = module.params['state']
    services = get_services(module)
    service = services[service_name]

    if service['state'] == desired_state:
        module.exit_json(changed=False)

    module.run_command(SERVICE_COMMANDS[desired_state] + [service_name])

    module.exit_json(changed=True)


if __name__ == '__main__':
    main()
