#!/bin/bash

# configure private network (https://netplan.io/)
NETPLAN_CONFIG="/etc/netplan/55-vagrant.yaml"
if [ ! -f "${NETPLAN_CONFIG}" ]; then
    sudo install -o root -g root -m 0644 /vagrant/vagrant/netplan-private.yaml "${NETPLAN_CONFIG}"
    sudo sed -i -e 's|VAGRANTCIDR|192.168.80.20/24|g' "${NETPLAN_CONFIG}"
    sudo sed -i -e 's|VAGRANTIPADDR|192.168.80.20|g' "${NETPLAN_CONFIG}"

    sudo netplan generate
    sudo netplan apply
    # sudo systemctl restart systemd-networkd.service
fi

# configure and start MDCS node service
if [ ! -f "/etc/systemd/system/mdcs-node.service" ]; then
    # install the systemd service
    sudo install -o root -g root -m 0644 /vagrant/vagrant/mdcs-node.service /etc/systemd/system/
    sudo systemctl daemon-reload
fi

systemctl is-active mdcs-node.service &> /dev/null
if [ $? -ne 0 ]; then
    # enable and start the service
    sudo systemctl enable mdcs-node.service
    sudo systemctl start mdcs-node.service
fi
