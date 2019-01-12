#!/bin/bash

# settings
source /vagrant/vagrant/settings.sh

# update packages
sudo apt-get update
sudo apt-get -y upgrade

# install development tools and utilities
sudo apt-get -y install build-essential vim tmux htop

# install python 3
sudo apt-get -y install python3 python3-dev python3-virtualenv

# configure tmpfiles to create socket directory
if [ ! -f "/etc/tmpfiles.d/mdcs" ]; then
    sudo install -o root -g root -m 0644 "${SRC}/tmpfiles" /etc/tmpfiles.d/mdcs
fi

# manually create socket directory for first boot
if [ ! -d "/run/mdcs" ]; then
    sudo install -o vagrant -g vagrant -m 0755 -d /run/mdcs
fi

# create the virtualenv
if [ ! -d "${MDCS_VENV}" ]; then
    python3 -m virtualenv -p $(which python3) "${MDCS_VENV}"
    chown -R vagrant:vagrant "${MDCS_VENV}"
fi

# create environment file
if [ ! -f "/etc/default/mdcs" ]; then
    echo "MDCS_VENV=${MDCS_VENV}" > /etc/default/mdcs

    chown root:root /etc/default/mdcs
    chmod 0644 /etc/default/mdcs
fi

# install requirements
source "${MDCS_VENV}/bin/activate"
pushd /vagrant
make reqs
popd
