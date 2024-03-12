def deploy_honeypot(config, name, box, memory_size, host_path, port_vm, port_host, port_id, tap, mac_tap, ip_address_tap, routes,ip_address_route)
config.vm.define name do |vm|
  vm.vm.box = box
  vm.vm.provider "virtualbox" do |vb|
    vb.memory = memory_size
  end
  vm.vm.synced_folder "./#{host_path}", "/home/claudio/ubuntu/#{host_path}"
  vm.vm.network :forwarded_port, guest: port_vm, host: port_host, id: port_id
  vm.vm.network "public_network", bridge: tap, mac: mac_tap, ip: ip_address_tap

  routes.each do |route|
    vm.vm.provision "shell",
  run: "always",
  inline: "ip route add #{route} via #{ip_address_route} dev enp0s8"
  end

  vm.vm.provision "shell", path: "./configurations/#{name}.sh"
  vm.vm.provision "shell", path: "./#{host_path}/start.sh"
end
end

def deploy_honeypot2(config, name, box, memory_size, host_path, port_vm, port_host, port_id, tap, mac_tap, ip_address_tap, routes,ip_address_route)
config.vm.define name do |vm|
  vm.vm.box = box
  vm.vm.provider "virtualbox" do |vb|
    vb.memory = memory_size
  end
  vm.vm.synced_folder "./#{host_path}", "/home/claudio/ubuntu/#{host_path}"
  vm.vm.network :forwarded_port, guest: port_vm, host: port_host, id: port_id
  vm.vm.network "public_network", bridge: tap, mac: mac_tap, ip: ip_address_tap

  routes.each do |route|
    vm.vm.provision "shell",
  run: "always",
  inline: "ip route add #{route} via #{ip_address_route} dev enp0s8"
  end

  vm.vm.provision "shell", path: "./configurations/int_heralding.sh"
  vm.vm.provision "shell", path: "./#{host_path}/start.sh"
end
end  

def deploy_service(config, name, box, memory_size, host_path, port_vm, port_host, port_id, tap, mac_tap, ip_address_tap, routes,ip_address_route)
    config.vm.define name do |vm|
      vm.vm.box = box
      vm.vm.provider "virtualbox" do |vb|
        vb.memory = memory_size
      end
      vm.vm.synced_folder "./#{host_path}", "/home/claudio/ubuntu/#{name}"
      vm.vm.network :forwarded_port, guest: port_vm, host: port_host, id: port_id
      vm.vm.network "public_network", bridge: tap, mac: mac_tap, ip: ip_address_tap
    
      routes.each do |route|
        vm.vm.provision "shell",
      run: "always",
      inline: "ip route add #{route} via #{ip_address_route} dev enp0s8"
      end
    
      vm.vm.provision "shell", path: "./configurations/#{name}.sh"
    end
    end  

def deploy_honeyfarm(config, name, box, memory_size, host_path, port_vm, port_host, port_id, tap, mac_tap, ip_address_tap, routes,ip_address_route)
    config.vm.define name do |vm|
      vm.vm.box = box
      vm.vm.provider "virtualbox" do |vb|
        vb.memory = memory_size
      end
      vm.vm.synced_folder "./#{host_path}", "/home/claudio/ubuntu/#{host_path}"
      vm.vm.network :forwarded_port, guest: port_vm, host: port_host, id: port_id
      vm.vm.network "public_network", bridge: tap, mac: mac_tap, ip: ip_address_tap
    
      routes.each do |route|
        vm.vm.provision "shell",
      run: "always",
      inline: "ip route add #{route} via #{ip_address_route} dev enp0s8"
      end
    
      vm.vm.provision "shell", path: "./configurations/#{name}.sh"
      vm.vm.provision "shell", path: "./#{host_path}/start.sh"
      vm.vm.provision "shell", inline: <<-SHELL
    cd /home/claudio/ubuntu/#{name}/docker/docker-build

    docker-compose up -d
  SHELL
    end
    end

def deploy_honeyfarm_runtime(config, name, box, memory_size, host_path, port_vm, port_host, port_id, tap, mac_tap, ip_address_tap, routes,ip_address_route)
    config.vm.define name do |vm|
      vm.vm.box = box
      vm.vm.provider "virtualbox" do |vb|
        vb.memory = memory_size
      end
      vm.vm.synced_folder "./#{host_path}", "/home/claudio/ubuntu/#{host_path}"
      vm.vm.network :forwarded_port, guest: port_vm, host: port_host, id: port_id
      vm.vm.network "public_network", bridge: tap, mac: mac_tap, ip: ip_address_tap
    
      routes.each do |route|
        vm.vm.provision "shell",
      run: "always",
      inline: "ip route add #{route} via #{ip_address_route} dev enp0s8"
      end
    
      vm.vm.provision "shell", path: "./configurations/#{host_path}.sh"
      vm.vm.provision "shell", path: "./#{host_path}/start.sh"
      
    end
    end
        
def deploy_honeyfarm2(config, name, box, memory_size, host_path, port_vm, port_host, port_id, tap, mac_tap, ip_address_tap, routes,ip_address_route)
    config.vm.define name do |vm|
      vm.vm.box = box
      vm.vm.provider "virtualbox" do |vb|
        vb.memory = memory_size
      end
      vm.vm.synced_folder "./#{host_path}", "/home/claudio/ubuntu/#{name}"
      vm.vm.network :forwarded_port, guest: port_vm, host: port_host, id: port_id
      vm.vm.network "public_network", bridge: tap, mac: mac_tap, ip: ip_address_tap
    
      routes.each do |route|
        vm.vm.provision "shell",
      run: "always",
      inline: "ip route add #{route} via #{ip_address_route} dev enp0s8"
      end
    
      vm.vm.provision "shell", path: "./configurations/#{name}.sh"
      vm.vm.provision "shell", inline: <<-SHELL
    cd /home/claudio/ubuntu/host2/docker/docker-build

    docker-compose up -d
  SHELL
    end
    end    

def deploy_elk(config, name, box, memory_size, host_path, port_vm, port_host, port_id, tap1, tap2, mac_tap1, mac_tap2, ip_address_tap1, ip_address_tap2, routes1, routes2, ip_address_route1, ip_address_route2)
      config.vm.define name do |vm|
        vm.vm.box = box
        vm.vm.provider "virtualbox" do |vb|
          vb.memory = memory_size
        end
        vm.vm.synced_folder "elk/", "/home/claudio/ubuntu/elk"
        vm.vm.network :forwarded_port, guest: port_vm, host: port_host, id: port_id
        vm.vm.network "public_network", bridge: tap1, mac: mac_tap1, ip: ip_address_tap1
        vm.vm.network "public_network", bridge: tap2, mac: mac_tap2, ip: ip_address_tap2
        
      
        routes1.each do |route|
          vm.vm.provision "shell",
        run: "always",
        inline: "ip route add #{route} via #{ip_address_route1} dev enp0s8"
        end
        
        routes2.each do |route|
          vm.vm.provision "shell",
        run: "always",
        inline: "ip route add #{route} via #{ip_address_route2} dev enp0s9"
        end
        
      
        vm.vm.provision "shell", path: "./configurations/elk.sh"
        vm.vm.provision "shell", path: "./elk/start.sh"
    end
    end
