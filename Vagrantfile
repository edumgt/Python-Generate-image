# -*- mode: ruby -*-
# vi: set ft=ruby :
#
# Vagrantfile — VirtualBox VM for Python-Generate-image on k3s (Ubuntu 24.04)
#
# Prerequisites on the host:
#   - VirtualBox 7.x
#   - Vagrant 2.4+
#
# Usage:
#   vagrant up          # create & provision the VM
#   vagrant ssh         # SSH into the VM
#   vagrant halt        # shut down gracefully
#   vagrant destroy -f  # remove the VM entirely

Vagrant.configure("2") do |config|
  # Ubuntu 24.04 LTS (Noble Numbat) — official Vagrant cloud box
  config.vm.box = "ubuntu/noble64"
  config.vm.box_version = ">= 20240401.0.0"

  config.vm.hostname = "imggen-k8s"

  # -------------------------------------------------------------------
  # Network
  # -------------------------------------------------------------------
  # Port-forward the k3s NodePort so the Studio UI is reachable from
  # the host at http://localhost:30800
  config.vm.network "forwarded_port", guest: 30800, host: 30800, host_ip: "127.0.0.1"

  # Private network so the host can also reach the VM directly
  config.vm.network "private_network", ip: "192.168.56.20"

  # -------------------------------------------------------------------
  # VirtualBox provider settings
  # -------------------------------------------------------------------
  config.vm.provider "virtualbox" do |vb|
    vb.name   = "imggen-k8s-ubuntu24"
    vb.memory = 6144   # 6 GB — diffusers needs at least 4 GB on CPU
    vb.cpus   = 4
    vb.customize ["modifyvm", :id, "--natdnshostresolver1", "on"]
    vb.customize ["modifyvm", :id, "--natdnsproxy1", "on"]
    # Disable audio and USB to keep overhead low
    vb.customize ["modifyvm", :id, "--audio", "none"]
    vb.customize ["modifyvm", :id, "--usb", "off"]
  end

  # -------------------------------------------------------------------
  # Shared folder — mount the repo inside the VM
  # -------------------------------------------------------------------
  config.vm.synced_folder ".", "/home/vagrant/app", type: "virtualbox"

  # -------------------------------------------------------------------
  # Provision — run setup-vm.sh on first boot
  # -------------------------------------------------------------------
  config.vm.provision "shell", path: "scripts/setup-vm.sh", privileged: true

  config.vm.post_up_message = <<~MSG
    ========================================================
    VM is ready!

    SSH:         vagrant ssh
    Studio UI:   http://localhost:30800  (or http://192.168.56.20:30800)

    Inside the VM you can run:
      cd /home/vagrant/app
      python3 moon_test.py        # generate moon-in-space image (CPU)
      kubectl get pods -n imggen  # check k3s deployment status
    ========================================================
  MSG
end
