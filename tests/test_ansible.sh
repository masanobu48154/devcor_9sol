#!/bin/bash

echo "Starting Ansible test"

INVENTORY=inventory
echo "Using inventory file: $INVENTORY"

echo "Executing Ansible script that gets VRFs"
ansible-playbook -i $INVENTORY playbooks/vrf_get.yml | grep "ok=2"
EXIT_CODE=$?
echo "Exit code of the test was: $EXIT_CODE"


if [[ $EXIT_CODE -ne 0 ]]; then
    echo "Failed to execute the vrf_get.yml playbook."
    exit $EXIT_CODE
fi

echo "Executing Ansible script that configures VRFs"
VRF_NAME=test_vrf
VRF_ID=100

ansible-playbook -i $INVENTORY playbooks/vrf_set.yml --check -e vrf_name=$VRF_NAME -e vrf_id=$VRF_ID -vvv > ./.tmp_output


if [[ `cat ./.tmp_output | grep "vrf definition $VRF_NAME" | wc -l` -ne 1 ]]; then
    echo "The VRF definition not found in the output."
    echo "Failed to execute vrf_set.yml."
    exit 1
fi

if [[ `cat ./.tmp_output | grep "rd 65001:$VRF_ID" | wc -l` -ne 1 ]]; then
    echo "The RD config not found in the output."
    echo "Failed to execute vrf_set.yml."
    exit 1
fi

if [[ `cat ./.tmp_output | grep -e "route-target.*65001:$VRF_ID" | wc -l` -ne 2 ]]; then
    echo "The route-target configuration not found in output."
    echo "Failed to execute vrf_set.yml."
    exit 1
fi

rm ./.tmp_output
