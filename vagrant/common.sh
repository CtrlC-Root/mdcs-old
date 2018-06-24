#!/bin/bash

# update packages
sudo apt-get update
sudo apt-get -y upgrade

# install development tools and utilities
sudo apt-get -y install build-essential vim tmux htop
