IF_INET = "wlp1s0"
VAGRANT_EXPERIMENTAL="disks"

Vagrant.configure('2') do |config|
    config.vm.network "public_network", bridge: [IF_INET]
    
    config.vm.provider :virtualbox
    config.vm.disk :disk, size: "10GB", primary: true

    config.vm.define 'openwnms' do |host|
        host.vm.box = 'ubuntu/groovy64'
        host.vm.provider "virtualbox" do |vb|
            vb.memory = 512
            vb.cpus = 1
            vb.name = "openwnms01"
        end

        host.vm.provision 'file',
            source: './files/snmpd.conf' , destination: '/home/vagrant/snmpd.conf'

        host.vm.provision 'shell', 
            inline: 'sudo apt update && \
                     sudo apt install -y snmp snmp-mibs-downloader && \
                     sudo apt install -y snmpd && \
                     sudo cp /home/vagrant/snmpd.conf /etc/snmp/snmpd.conf && \
                     sudo systemctl restart snmpd'
    end
end