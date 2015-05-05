Vagrant.configure("2") do |config|
  config.vm.define "ubuntu", primary: true do |this|
    this.vm.box = "ubuntu"
    this.vm.box_url = "https://cloud-images.ubuntu.com/vagrant/trusty/current/trusty-server-cloudimg-amd64-vagrant-disk1.box"
    this.vm.provision "shell", path: "scripts/vagrant/default.sh"
  end
end
