import topology as t
# THREAT INTELLIGENCE SUBNET MANAGEMENT
# indexes
COWRIE_INDEX = 0
HERALDING_INDEX = 1
HERALDING1_INDEX = 1
HERALDING2_INDEX = 2
HERALDING3_INDEX = 3
HERALDING4_INDEX = 4

SSH_INDEX = 0
TELNET_INDEX= 1
FTP_INDEX = 2
SOCKS5_INDEX = 3

def product_vector_matrix(vector, matrix):
 
    if len(vector) != len(matrix):
        raise ValueError("Error")

    result = [0] * len(matrix[0])

    for i in range(len(matrix[0])):
        for j in range(len(vector)):
            result[i] += vector[j] * matrix[j][i]

    return result

#list of host HN
hosts = [t.ti_host1, t.ti_host2]
# list of honeypots HP
honeypots = [t.cowrie, t.heralding1, t.heralding2,t.heralding3, t.heralding4]

#an m-dimensional vector that corresponds to running honeypots on a specific host hl. rhm equals to ‘1’ when hpm is installed on host hl , otherwise ‘0’;

h_h1 = [1, 1, 1, 0, 0]
h_h2 = [0, 0, 0, 1, 1]

# list of services SVC
services = ["ssh", "telnet", "ftp", "socks5"]

# service map (honeypots x services): rows = honeypot, columns = services supported
s_hp1 = [1, 1, 0, 0]
s_hp2 = [1, 0, 1, 1]
s_hp3 = [1, 0, 1, 1]
s_hp4 = [1, 0, 1, 1]
s_hp5 = [1, 0, 1, 1]
#sm = [[1, 1, 0, 0], [1, 0, 1, 1],[1, 0, 1, 1]]
sm= [s_hp1,s_hp2,s_hp3,s_hp4,s_hp5]

# port number of each service for hp, 0 if the service is not supported
ports_hp1 = [22,23,0,0]
ports_hp2 = [2022, 0, 2021, 2080]
ports_hp3 = [3022, 0, 3021, 3080]
ports_hp4 = [2022, 0, 2021, 2080]
ports_hp5 = [3022, 0, 3021, 3080]

ports = [ports_hp1,ports_hp2,ports_hp3,ports_hp4,ports_hp5]
#ports = [
   # [22, 23, 0, 0],
    #[2022, 0, 2021, 2080],
    #[3022, 0, 3021, 3080],
    #[2022, 0, 2021, 2080],
    #[3022, 0, 3021, 3080]
#]



#service distribution on a host hk
#redundant services on Host 1
#sd_h1 = h_h1 * sm
sd_h1 = product_vector_matrix(h_h1,sm)
#redundant services on Host 2
#sd_h2 = h_h2 * sm
sd_h2 = product_vector_matrix(h_h2,sm)


#print(sd_h1)
#print(sd_h2)

#Entire service distribution (SDH) in honeynet
sdh = [elem1 + elem2 for elem1, elem2 in zip(sd_h1, sd_h2)]

#print(sdh)

# service busy: sbn = 1 if it is busy, else it is 0
# default = all services are free
sb = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
