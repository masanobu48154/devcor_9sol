# pylint: disable=C0103


'''Simple Flask application'''

import os
import sys
import argparse
from flask import Flask
from flask import request
from flask import abort
from flask import Response
from ansible_executor import AnsibleExecutor

INVENTORY = os.environ.get('APP_INVENTORY', 'inventory')

ans_exec = AnsibleExecutor(INVENTORY)
if not ans_exec.validate_inventory():
    print(f'Inventory file "{INVENTORY}" does not exist.')
    sys.exit(1)
hosts = ans_exec.get_hosts()

app = Flask(__name__)


@app.route('/vrf', methods=['GET', 'POST'])
def get_vrfs():
    """ Function that handles GET and POST method for the /vrf path """
    if request.method == 'GET':
        playbook = 'playbooks/vrf_get.yml'
        vrf = ans_exec.run_playbook(playbook=playbook)

        output = 'The current configurations are:<br><br>'
        for host in hosts:
            output += f'--> {host}:<br>'
            for line in vrf['plays'][0]['tasks'][0]['hosts'][host]['stdout'][0].splitlines():
                output += f'{line}<br>'
            output += '<br>'
        return output
    if request.method == 'POST':
        data = request.get_json(force=True)
        playbook = 'playbooks/vrf_set.yml'
        if 'vrf_name' not in data and 'vrf_id' not in data:
            abort(400)
        vrf = ans_exec.run_playbook(playbook=playbook, vars=data)
        return Response(data, status=201, mimetype='application/json')

    return abort(404)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all():
    """ Function that catches all other paths """
    abort(404)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', action='store_true', default=False)
    args = parser.parse_args()
    app.run(debug=args.debug, host='0.0.0.0')
