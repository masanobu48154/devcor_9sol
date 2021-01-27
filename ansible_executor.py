import subprocess
import os
import json


class AnsibleExecutor:

    def __init__(self, inventory):
        self.inventory = inventory

    def run_playbook(self, playbook, vars=None, check=False):
        command = f'ansible-playbook -i {self.inventory}'
        if vars:
            for k, v in vars.items():
                command += f' -e {k}={v}'
        command += f' {playbook}'
        if check is True:
            command += ' --check'

        process = subprocess.Popen(command.split(), stdout=subprocess.PIPE, env=dict(os.environ, ANSIBLE_STDOUT_CALLBACK='json', ANSIBLE_HOST_KEY_CHECKING='false'))

        # add the code that returns error message if exit code is non-zero
        stdoutput = process.communicate()[0].decode('ascii')

        return json.loads(stdoutput)

    def get_hosts(self):
        with open(self.inventory) as f:
            lines = f.readlines()

        hosts = []
        for line in lines:
            if line.startswith('['):
                continue
            hosts.append(line.split()[0])
        return hosts

    def validate_inventory(self):
        return os.path.isfile(str(self.inventory))