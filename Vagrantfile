# -*- mode: ruby -*-
# vi: set ft=ruby :

targets = [
  'centos-7',
  'ubuntu-16.04',
  'windows-server-2012-r2'
]

Vagrant.configure("2") do |config|
  config.vm.synced_folder ".", "/vagrant", disabled: false
  targets.each do |name|
    config.vm.define name do |this|
      this.vm.box = "addle/#{name}"
      this.vm.hostname = name
    end
  end

 config.vm.provider "virtualbox" do |v|
    v.memory = "2048"
    v.cpus = "2"
    v.gui = true
  end

  config.vm.provider "vmware_desktop" do |v|
    v.vmx["memsize"] = "2048"
    v.vmx["numvcpus"] = "2"
    v.gui = true
  end

  config.vm.provider "vmware_desktop" do |v|
    v.vmx["memsize"] = "2048"
    v.vmx["numvcpus"] = "2"
    v.gui = true
  end
end
