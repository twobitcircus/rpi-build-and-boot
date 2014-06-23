# -*- mode: ruby -*-
# vi: set ft=ruby :

# Vagrantfile API/syntax version. Don't touch unless you know what you're doing!
VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  config.vm.box = "ubuntu/precise32"

  config.vm.network "public_network", bridge: 'en5: Thunderbolt Ethernet', ip: "10.0.0.1"
  #config.vm.network "private_network", type: "dhcp"
  #if Vagrant.has_plugin?("vagrant-cachier")
  #  config.cache.scope = :box
  #  #config.cache.synced_folder_opts = {
  #  #  type: :nfs,
  #  #  mount_options: ['rw', 'vers=3', 'tcp', 'nolock']
  #  #}
  #end


  # If true, then any SSH connections made will enable agent forwarding.
  # Default value: false
  # config.ssh.forward_agent = true

  # Share an additional folder to the guest VM. The first argument is
  # the path on the host to the actual folder. The second argument is
  # the path on the guest to mount the folder. And the optional third
  # argument is a set of non-required options.
  # config.vm.synced_folder "../data", "/vagrant_data"

  # Provider-specific configuration so you can fine-tune various
  # backing providers for Vagrant. These expose provider-specific options.
  # Example for VirtualBox:
  #
   config.vm.provider "virtualbox" do |vb|
     vb.gui = false
  
     ## Use VBoxManage to customize the VM. For example to change memory:
     #vb.customize ["modifyvm", :id, "--memory", "1024"]
   end
  
  config.vm.provision "ansible" do |ansible|
    ansible.playbook = "playbook.yml"
  end

end
