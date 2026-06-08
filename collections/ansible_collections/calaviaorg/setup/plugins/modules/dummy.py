# Ansible Collection Setup
# Copyright (C) 2024  calavia.org

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import absolute_import, division, print_function

DOCUMENTATION = r"""
---
module: dummy
short_description: This is my test module
description: This is my longer description explaining my test module.
version_added: "1.0.0"
author:
    - Your Name (@yourGitHubHandle)
options:
    name:
        description: This is the message to send to the test module.
        required: true
        type: str
    new:
        description:
            - Control to demo if the result of this module is changed or not.
            - Parameter description can be a list as well.
        required: false
        type: bool
        default: False
requirements: []
seealso: []
"""

EXAMPLES = r"""
# Pass in a message
- name: Test with a message
  calaviaorg.setup.dummy:
    name: hello world

# pass in a message and have changed true
- name: Test with a message and changed output
  calaviaorg.setup.dummy:

# fail the module
- name: Test failure of the module
  calaviaorg.setup.dummy:
"""

RETURN = r"""
# These are examples of possible return values
original_message:
    description: The original name param that was passed in.
    type: str
    returned: always
    sample: 'hello world'
message:
    description: The output message that the test module generates.
    type: str
    returned: always
    sample: 'goodbye'
"""

from ansible.module_utils.basic import AnsibleModule  # noqa: E402

__metaclass__ = type


def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        name=dict(type="str", required=True),
        new=dict(type="bool", required=False, default=False),
    )

    # seed the result dict in the object
    # we primarily care about changed and state
    # changed is if this module effectively modified the target
    # state will include any data that you want your module to pass back
    # for consumption, for example, in a subsequent task
    result = dict(changed=False, original_message="", message="")

    # the AnsibleModule object will be our abstraction working with Ansible
    # this includes instantiation, a couple of common attr would be the
    # args/params passed to the execution, as well as if the module
    # supports check mode
    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)

    # if the user is working with this module in only check mode we do not
    # want to make any changes to the environment, just return the current
    # state with no modifications
    if module.check_mode:
        module.exit_json(**result)

    # manipulate or modify the state as needed (this is going to be the
    # part where your module will do what it needs to do)
    result["original_message"] = module.params["name"]
    result["message"] = "goodbye"

    # use whatever logic you need to determine whether or not this module
    # made any modifications to your target
    if module.params["new"]:
        result["changed"] = True

    # during the execution of the module, if there is an exception or a
    # conditional state that effectively causes a failure, run
    # AnsibleModule.fail_json() to pass in the message and the result
    if module.params["name"] == "fail me":
        module.fail_json(msg="You requested this to fail", **result)

    # in the event of a successful module execution, you will want to
    # simple AnsibleModule.exit_json(), passing the key/value results
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
