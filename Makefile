# Builds all the docker images of the project

.PHONY: all images clean bridge

all: images 

images:
	docker build . -f Dockerfile -t test
	docker build . -f router -t pimd_router
	docker build . -f Networks -t add_networks

clean:
	docker rmi -f test pimd_router add_networks
	docker network rm dds_network_1
	docker network rm dds_network_2
	
	

# Creates two bridges that will be used as networks by docker containers and libvirt VMs. 
bridge:
	docker network create --driver=bridge --gateway=172.12.0.1 --subnet=172.12.0.0/16 --ip-range=172.12.0.0/17 -o "com.docker.network.bridge.name"="dds_network_2"  dds_network_2
	docker network create --driver=bridge --gateway=172.11.0.1 --subnet=172.11.0.0/16 --ip-range=172.11.0.0/17 -o "com.docker.network.bridge.name"="dds_network_1"  dds_network_1
	
