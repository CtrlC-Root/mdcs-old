#!/bin/bash

# install redis
dpkg -l redis-server &> /dev/null
if [ $? -ne 0 ]; then
    # install the latest version
    sudo add-apt-repository -y ppa:chris-lea/redis-server
    sudo apt-get -y update
    sudo apt-get install -y redis-server

    # enable the service
    sudo systemctl enable redis-server.service
fi
