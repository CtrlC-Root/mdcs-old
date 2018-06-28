#!/bin/bash

# update packages
sudo apt-get update
sudo apt-get -y upgrade

# install development tools and utilities
sudo apt-get -y install build-essential vim tmux htop

# install python 3
sudo apt-get -y install python3 python3-dev python3-virtualenv
