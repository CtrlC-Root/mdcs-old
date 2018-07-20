#!/bin/bash

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
