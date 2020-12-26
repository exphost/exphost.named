#!/bin/bash
result=0
trap 'result=1' ERR
yamllint roles/tested_role

ansible-lint dummy_playbook.yml --exclude $(ls roles/exphost.* -d|paste -s -d ,|sed 's/,/ --exclude /g')
exit $result

