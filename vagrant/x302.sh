#!/bin/bash

# settings
source /vagrant/vagrant/settings.sh

# configure private network (https://netplan.io/)
NETPLAN_CONFIG="/etc/netplan/55-vagrant.yaml"
if [ ! -f "${NETPLAN_CONFIG}" ]; then
    sudo install -o root -g root -m 0644 "${SRC}/netplan-private.yaml" "${NETPLAN_CONFIG}"
    sudo sed -i -e 's|VAGRANTCIDR|192.168.80.30/24|g' "${NETPLAN_CONFIG}"
    sudo sed -i -e 's|VAGRANTIPADDR|192.168.80.30|g' "${NETPLAN_CONFIG}"

    sudo netplan generate
    sudo netplan apply
    # sudo systemctl restart systemd-networkd.service
fi

# activate virtualenv
source "${MDCS_VENV}/bin/activate"

# install gunicorn for running the remote web application
if [ ! -f "${MDCS_VENV}/bin/gunicorn" ]; then
    pip install --upgrade gunicorn
fi

# create the remote sqlite database
# TODO: we should make a separate copy on the VM
if [ ! -f "${PKG}/remote/remote.db" ]; then
    pushd "${PKG}/remote"
    alembic upgrade head
    popd
fi

# deactivate virtualenv to avoid any pollution
deactivate

# install and start MDCS remote service
# TODO: customize settings to use local remote.db copy
if [ ! -f "/etc/systemd/system/mdcs-remote.service" ]; then
    # install the systemd service
    sudo install -o root -g root -m 0644 "${SRC}/mdcs-remote.service" /etc/systemd/system/
    sudo systemctl daemon-reload
fi

systemctl is-active mdcs-remote.service &> /dev/null
if [ $? -ne 0 ]; then
    sudo systemctl enable mdcs-remote.service
    sudo systemctl start mdcs-remote.service
fi

# install and start MDCS remote worker service
# TODO: customize settings to use local remote.db copy
if [ ! -f "/etc/systemd/system/mdcs-remote-worker.service" ]; then
    sudo install -o root -g root -m 0644 "${SRC}/mdcs-remote-worker.service" /etc/systemd/system/
    sudo systemctl daemon-reload
fi

systemctl is-active mdcs-remote-worker.service &> /dev/null
if [ $? -ne 0 ]; then
    sudo systemctl enable mdcs-remote-worker.service
    sudo systemctl start mdcs-remote-worker.service
fi

# install nginx
dpkg -l nginx-light &> /dev/null
if [ $? -ne 0 ]; then
    sudo apt-get install -y nginx-light
fi

systemctl is-active nginx.service &> /dev/null
if [ $? -ne 0 ]; then
    sudo systemctl enable nginx.service
    sudo systemctl start nginx.service
fi
