# -*- mode: ruby -*-
# vi: set ft=ruby :

vagrantDir = File.expand_path("scripts/vagrant", File.dirname(__FILE__)) + "/"

Vagrant.configure("2") do |config|
  config.vm.synced_folder ".", "/vagrant", disabled: false

  config.vm.define "linux" do |this|
    this.vm.box = "trueability/ubuntu-20.04"
    this.vm.hostname = "linux"
    # this.vm.provision "shell", path: "scripts/vagrant/bootstrap.sh"
  end

  config.vm.define "windows" do |this|
    this.vm.box = "senglin/win-10-enterprise-vs2015community"
    this.vm.hostname = "windows"
    # this.vm.provision "shell", path: "scripts/vagrant/bootstrap.ps1"
  end

  config.vm.provider "virtualbox" do |v|
    v.memory = "4192"
    v.cpus = "4"
    v.gui = true
  end

  config.vm.provider "vmware_desktop" do |v|
    v.vmx["memsize"] = "4192"
    v.vmx["numvcpus"] = "4"
    v.gui = true
  end
end
