# -*- mode: ruby -*-
# vi: set ft=ruby :

# All Vagrant configuration is done below. The "2" in Vagrant.configure
# configures the configuration version (we support older styles for
# backwards compatibility). Please don't change it unless you know what
# you're doing.
Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/xenial64"
  config.vm.provision "shell", path: "vagrant/common.sh"

  config.vm.define "f301" do |f301|
    f301.vm.hostname = "f301"
    f301.vm.provider "virtualbox" do |vb|
      vb.memory = 2048
      vb.cpus = 2

      # override setting in ubuntu/xenial64 box to disable output log file
      vb.customize ["modifyvm", :id, "--uartmode1", "disconnected"]
    end

    f301.vm.provision "shell", path: "vagrant/f301.sh"
    f301.vm.network :forwarded_port, guest: 11300, host: 11300 # beanstalkd
    f301.vm.network :forwarded_port, guest: 3000, host: 3000   # aurora beanstalk dahsboard
  end
end
