#!/bin/bash

# settings
source /vagrant/vagrant/settings.sh
AURORA_URL="https://github.com/xuri/aurora/releases/download/2.1/aurora_linux_amd64_v2.1.tar.gz"

# configure private network (https://netplan.io/)
NETPLAN_CONFIG="/etc/netplan/55-vagrant.yaml"
if [ ! -f "${NETPLAN_CONFIG}" ]; then
    sudo install -o root -g root -m 0644 "${SRC}/netplan-private.yaml" "${NETPLAN_CONFIG}"
    sudo sed -i -e 's|VAGRANTCIDR|192.168.80.10/24|g' "${NETPLAN_CONFIG}"
    sudo sed -i -e 's|VAGRANTIPADDR|192.168.80.10|g' "${NETPLAN_CONFIG}"

    sudo netplan generate
    sudo netplan apply
    # sudo systemctl restart systemd-networkd.service
fi

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
    # https://unix.stackexchange.com/a/239745/103130
    wget --quiet -O - "${AURORA_URL}" | tar -xz -C $HOME
    sudo install -o root -g root -m 0755 $HOME/aurora /usr/local/bin
    rm $HOME/aurora
fi

if [ ! -f "/etc/aurora.toml" ]; then
    sudo install -o root -g root -m 0640 "${SRC}/aurora.toml" /etc/
fi

if [ ! -f "/etc/systemd/system/aurora.service" ]; then
    sudo install -o root -g root -m 0644 "${SRC}/aurora.service" /etc/systemd/system/
    sudo systemctl daemon-reload
fi

systemctl is-active aurora.service &> /dev/null
if [ $? -ne 0 ]; then
    sudo systemctl enable aurora.service
    sudo systemctl start aurora.service
fi

# configure and start MDCS registry service
if [ ! -f "/etc/systemd/system/mdcs-registry.service" ]; then
    # install the systemd service
    sudo install -o root -g root -m 0644 "${SRC}/mdcs-registry.service" /etc/systemd/system/
    sudo systemctl daemon-reload
fi

systemctl is-active mdcs-registry.service &> /dev/null
if [ $? -ne 0 ]; then
    sudo systemctl enable mdcs-registry.service
    sudo systemctl start mdcs-registry.service
fi
