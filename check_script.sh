#!/bin/bash

source /opt/venv/bin/activate
# Run each playbook
echo "Checking ping"
ansible-playbook ping.yaml -i inventory

echo "Checking http"
ansible-playbook http.yaml -i inventory

#echo "Running another playbook if needed"
# ansible-playbooak /another_playbook.yaml -i /inventory

echo "Checking https"
ansible-playbook https.yaml -i inventory

echo "Checking Ldaps connection"
ansible-playbook ldap.yaml -i inventory

python3 generate_html_report.py

#cat results_ping.log
cat results_ping.log
cat results_http.log
# cat results_https.log
# cat results_ldap.log
#(cat results_ping.log; echo ""; cat results_http.log) > results.log
