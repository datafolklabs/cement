# -*- mode: ruby -*-
# vi: set ft=ruby :

targets = [
  'centos-7',
  'ubuntu-16.04',
  'windows-server-2012-r2'
]

vagrantDir = File.expand_path("scripts/vagrant", File.dirname(__FILE__)) + "/"

Vagrant.configure("2") do |config|
  config.vm.synced_folder ".", "/vagrant", disabled: false

  config.vm.define "linux" do |this|
    this.vm.box = "addle/ubuntu-16.04"
    this.vm.hostname = "linux"
    this.vm.provision "shell", path: "scripts/vagrant/bootstrap.sh"
  end

  config.vm.define "windows" do |this|
    this.vm.box = "addle/windows-server-2012-r2"
    this.vm.hostname = "windows"
    this.vm.provision "shell", path: "scripts/vagrant/bootstrap.ps1"
  end

  targets.each do |name|
    config.vm.define name do |this|
      this.vm.box = "addle/#{name}"
      this.vm.hostname = name

      if name.start_with?('windows')
          this.vm.provision "shell", path: "scripts/vagrant/bootstrap.ps1"
      else
          this.vm.provision "shell", path: "scripts/vagrant/bootstrap.sh"
      end

    end
  end

  config.vm.provider "virtualbox" do |v|
    v.memory = "1024"
    v.cpus = "1"
    v.gui = true
  end

  config.vm.provider "vmware_desktop" do |v|
    v.vmx["memsize"] = "1024"
    v.vmx["numvcpus"] = "1"
    v.gui = true
  end
end
