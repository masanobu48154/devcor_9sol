# Perform the following test:
# - load initial config
# - get vrfs (should be empty)
# - set 3 vrfs
# - get vrfs (there should be three)

import unittest
import requests
from netmiko import ConnectHandler

def load_router_init():
    # Load init config to the router
    conn = ConnectHandler(
        host='192.168.0.30',
        device_type='cisco_ios',
        username='cisco',
        password='cisco'
    )
    conn.send_command('configure replace bootflash:init.config force')

class AppTest(unittest.TestCase):

    url = 'http://127.0.0.1:5000/vrf'

    def test_01(self):
        """ Test that you can retrieve the
        VRFs from the router and that there are
        no VRFs"""
        response = requests.get(self.url)
        status_code = response.status_code
        content = response.content.decode('ascii')

        exp_out = 'The current configurations are:<br><br>--> csr1kv1:<br><br>'

        self.assertEqual(status_code, 200)
        self.assertEqual(content, exp_out)

    def test_02(self):
        """ Test that you can push the
        VRF configuration to the router"""

        for i in range(1,4):
            data = {
                'vrf_name': f'test0{str(i)}',
                'vrf_id': f'10{str(i)}'
            }
            response = requests.post(self.url, json=data)
            status_code = response.status_code
            self.assertEqual(status_code, 201)

    def test_03(self):
        """ Test that you can retrieve the
        VRFs from the router and that there are
        three entries"""
        response = requests.get(self.url)
        status_code = response.status_code
        content = response.content.decode('ascii')

        self.assertEqual(status_code, 200)
        self.maxDiff = None
        self.assertRegex(content, 'vrf definition test01')
        self.assertRegex(content, 'vrf definition test02')
        self.assertRegex(content, 'vrf definition test03')

if __name__ == "__main__":
    load_router_init()
    unittest.main()
