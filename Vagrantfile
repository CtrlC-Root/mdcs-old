# -*- mode: ruby -*-
# vi: set ft=ruby :

# All Vagrant configuration is done below. The "2" in Vagrant.configure
# configures the configuration version (we support older styles for
# backwards compatibility). Please don't change it unless you know what
# you're doing.
Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/bionic64"
  config.vm.provision "shell", path: "vagrant/common.sh"

  config.vm.define "f301" do |f301|
    f301.vm.hostname = "f301"
    f301.vm.provider "virtualbox" do |vb|
      vb.memory = 1536
      vb.cpus = 2
    end

    f301.vm.provision "shell", path: "vagrant/f301.sh"
    f301.vm.network "private_network", ip: "192.168.80.10", auto_config: false
    f301.vm.network :forwarded_port, guest: 11300, host: 11300 # beanstalkd
    f301.vm.network :forwarded_port, guest: 3000, host: 3000   # aurora beanstalk dahsboard
    f301.vm.network :forwarded_port, guest: 5520, host: 5520   # Registry HTTP API
    f301.vm.network :forwarded_port, guest: 8080, host: 8080   # Remote API and Web UI
  end

  config.vm.define "x301" do |x301|
    x301.vm.hostname = "x301"
    x301.vm.provider "virtualbox" do |vb|
      vb.memory = 768
      vb.cpus = 1
    end

    x301.vm.provision "shell", path: "vagrant/x301.sh"
    x301.vm.network "private_network", ip: "192.168.80.20", auto_config: false
    x301.vm.network :forwarded_port, guest: 5510, host: 5510 # Node HTTP API
    x301.vm.network :forwarded_port, guest: 5511, host: 5511 # Node TCP API
  end
end
