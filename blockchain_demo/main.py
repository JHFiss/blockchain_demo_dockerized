import socket
import time
import os
import computationnode
import logging

CONST_PORT = 8001
SUBNET_MASK = "10.5.0."


def connect(hn, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket.setdefaulttimeout(1)
    result = sock.connect_ex((hn, port))
    sock.close()
    return result == 0


logging.basicConfig(filename='blockchain.log', level=logging.INFO)
logger = logging.getLogger(__name__)

node_num = os.environ['NODENUM']

hostname = socket.gethostname()
ip = socket.gethostbyname(hostname)

logger.debug('IP: ' + str(ip))
logger.debug('NODE: ' + str(node_num))

n0 = computationnode.ComputationNode(ip, CONST_PORT, 'Testdata', node_num)

# Schedule three calls *concurrently*:

n0.start()

for i in range(0, 16):
    res = connect(SUBNET_MASK + str(i), CONST_PORT)
    if res:
        n0.connect_with_node(SUBNET_MASK + str(i), CONST_PORT)
i = 0
while 1:
    time.sleep(1)
    n0.add_new_data('Node' + str(node_num) + ' Testdata' + str(i))
    logger.info(str(n0.my_blockchain))
    i = i + 1

n0.join()






