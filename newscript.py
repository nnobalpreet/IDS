import yaml
import sys
import os
assert(len(sys.argv)>1),"No network specified";
network_name=sys.argv[1];

with open("docker-compose.yml", 'r') as input:
	try:
	   data = (yaml.load(input))
           if network_name not in data["networks"]:
		data["networks"].update({'dds_network_1': {'external': True}});
	   if network_name not in data["services"]["participant"]["networks"]: 
               data["services"]["participant"]["networks"].append(network_name);
               data["services"]["participant"]["networks"].remove(data["services"]["participant"]["networks"][0]);
	   with open('docker-compose.yml',"w") as k:
		yaml.dump(data, k, default_flow_style=False)
	except yaml.YAMLError as error1:
	   print(error1)
g = "docker-compose run participant ";
for i in range(2,len(sys.argv)):
	string1 = sys.argv[i];
	g = g+ string1 + " ";
os.system(g)
