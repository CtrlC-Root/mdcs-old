#!/bin/bash

# settings
AURORA_URL="https://github.com/xuri/aurora/releases/download/2.1/aurora_linux_amd64_v2.1.tar.gz"

# install beanstalk daemon
dpkg -l beanstalkd &> /dev/null
if [ $? -ne 0 ]; then
    sudo apt-get install -y beanstalkd
    sudo sed -i -e 's/\(BEANSTALKD_LISTEN_ADDR\)=127.0.0.1/\1=0.0.0.0/' /etc/default/beanstalkd
    sudo systemctl restart beanstalkd.service
fi

# install aurora beanstalkd dashboard
# https://github.com/xuri/aurora
which aurora &> /dev/null
if [ $? -ne 0 ]; then
    # download, extract, and install the binary
    # https://unix.stackexchange.com/a/239745/103130
    wget --quiet -O - "${AURORA_URL}" | tar -xz -C $HOME
    sudo install -o root -g root -m 0755 $HOME/aurora /usr/local/bin
    rm $HOME/aurora
fi

if [ ! -f "/etc/aurora.toml" ]; then
    # install the configuration file
    sudo install -o root -g root -m 0640 /vagrant/vagrant/aurora.toml /etc/
fi

if [ ! -f "/etc/systemd/system/aurora.service" ]; then
    # install the systemd service
    sudo install -o root -g root -m 0644 /vagrant/vagrant/aurora.service /etc/systemd/system/
    sudo systemctl daemon-reload
fi

systemctl is-active aurora.service &> /dev/null
if [ $? -ne 0 ]; then
    # enable and start the service
    sudo systemctl enable aurora.service
    sudo systemctl start aurora.service
fi
