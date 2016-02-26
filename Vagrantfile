Vagrant.configure("2") do |config|
  config.vm.define "ubuntu", primary: true do |this|
    this.vm.box = "ubuntu"
    this.vm.hostname = "ubuntu"
    this.vm.box_url = "https://cloud-images.ubuntu.com/vagrant/trusty/current/trusty-server-cloudimg-amd64-vagrant-disk1.box"
    this.vm.provision "shell", inline: "/vagrant/scripts/vagrant/up.sh"
  end

  config.vm.define "ubuntu-12.04", autostart: false do |this|
    this.vm.box = "ubuntu-12.04"
    this.vm.hostname = "ubuntu-12.04"
    this.vm.box_url = "https://cloud-images.ubuntu.com/vagrant/precise/current/precise-server-cloudimg-amd64-vagrant-disk1.box"
    this.vm.provision "shell", inline: "/vagrant/scripts/vagrant/up.sh"
  end

  config.vm.define "ubuntu-14.04", autostart: false do |this|
    this.vm.box = "ubuntu-14.04"
    this.vm.hostname = "ubuntu-14.04"
    this.vm.box_url = "https://cloud-images.ubuntu.com/vagrant/trusty/current/trusty-server-cloudimg-amd64-vagrant-disk1.box"
    this.vm.provision "shell", inline: "/vagrant/scripts/vagrant/up.sh"
  end

  config.vm.define "windows-server-2012-r2", autostart: false do |this|
    this.vm.box = "opentable/win-2012r2-standard-amd64-nocm"
    this.vm.hostname = "windows-server-2012-r2"
    this.vm.box_url = "opentable/win-2012r2-standard-amd64-nocm"
  end

  config.vm.provider "virtualbox" do |vb|
    vb.memory = 2048 
    vb.cpus = 2
    vb.gui = true
  end
end
