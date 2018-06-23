# -*- mode: ruby -*-
# vi: set ft=ruby :

vagrantDir = File.expand_path("scripts/vagrant", File.dirname(__FILE__)) + "/"

Vagrant.configure("2") do |config|
  config.vm.synced_folder ".", "/vagrant", disabled: false

  config.vm.define "linux" do |this|
    this.vm.box = "trueability/ubuntu-16.04"
    this.vm.hostname = "linux"
    # this.vm.provision "shell", path: "scripts/vagrant/bootstrap.sh"
  end

  config.vm.define "ubuntu-16.04" do |this|
    this.vm.box = "trueability/ubuntu-16.04"
    this.vm.hostname = "ubuntu-1604"
    # this.vm.provision "shell", path: "scripts/vagrant/bootstrap.sh"
  end

  config.vm.define "centos-7" do |this|
    this.vm.box = "trueability/centos-7"
    this.vm.hostname = "centos-7"
    # this.vm.provision "shell", path: "scripts/vagrant/bootstrap.sh"
  end

  config.vm.define "windows" do |this|
    this.vm.box = "senglin/win-10-enterprise-vs2015community"
    this.vm.hostname = "windows"
    # this.vm.provision "shell", path: "scripts/vagrant/bootstrap.ps1"
  end

  config.vm.define "windows-10-enterprise" do |this|
    this.vm.box = "senglin/win-10-enterprise-vs2015community"
    this.vm.hostname = "windows"
    # this.vm.provision "shell", path: "scripts/vagrant/bootstrap.ps1"
  end

  config.vm.define "windows-server-2012-r2" do |this|
    this.vm.box = "opentable/win-2012r2-standard-amd64-nocm"
    this.vm.hostname = "windows"
    # this.vm.provision "shell", path: "scripts/vagrant/bootstrap.ps1"
  end

  config.vm.provider "virtualbox" do |v|
    v.memory = "2048"
    v.cpus = "1"
    v.gui = true
  end

  config.vm.provider "vmware_desktop" do |v|
    v.vmx["memsize"] = "2048"
    v.vmx["numvcpus"] = "1"
    v.gui = true
  end
end
