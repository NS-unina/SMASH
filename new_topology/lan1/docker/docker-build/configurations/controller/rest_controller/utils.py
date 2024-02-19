from network import Subnet
import random

class Utils():

    @staticmethod
    def host_to_port(subnet : Subnet, host_ip):
        out_port = None
        nodes = subnet.nodes
        for k, v in nodes.items():
            ip = v.get_ip_addr()
            if ip == host_ip:
               out_port = k
        return out_port
    
    @staticmethod
    def host_to_mac(subnet : Subnet, host_ip):
        mac = None
        nodes = subnet.nodes
        for k, v in nodes.items():
            ip = v.get_ip_addr()
            if ip == host_ip:
                mac = v.get_MAC_addr()
        return mac
    
    @staticmethod
    def make_new_IP(ips, sub):
        while(True):
            if len(ips) == 251:
                ips.clear()
            new_ip = sub + str(random.randint(2, 253))
            if new_ip not in ips:
                ips.append(new_ip)
                break
        return new_ip
    
    def product_vector_matrix(vector, matrix):
        if len(vector) != len(matrix):
            raise ValueError("Error")

        result = [0] * len(matrix[0])

        for i in range(len(matrix[0])):
            for j in range(len(vector)):
                result[i] += vector[j] * matrix[j][i]

        return result
    
    def find_free_honeypot_by_service(service_busy, service_map, service):
        for honeypot_index in range(len(service_busy)):
            if service_busy[honeypot_index][service] == 0 and service_map[honeypot_index][service] == 1:
                return honeypot_index
            

        return None
    
    
            
    