import jsonpickle
import logging
from p2pnetwork.node import Node
import blockchain
from typing import TypeVar, Generic

T = TypeVar('T')


class ComputationNode(Node):
    """
    Class that represents a Computing Node
    Based on the Node class from p2pnetwork: https://github.com/macsnoeren/python-p2p-network
    """
    my_blockchain: blockchain
    logger: logging.getLogger(__name__)

    def add_new_data(self, data: Generic[T]):
        """
        Add new Data to the Blockchain of this Node
        :param data: Generic[T] data that is added to the blockchain
        :return: nothing
        """
        self.logger.info('Node ' + str(self.id) + ' started adding data: ' + str(data))
        self.my_blockchain.add_data(data)
        # While the blockchain is not valid tear it down, until it is valid again
        while not self.my_blockchain.validate_blockchain():
            self.logger.debug('Node ' + str(self.id) + ' removing last block trying to reach valid state!')
            self.my_blockchain.chain.pop()
        self.logger.info('Node ' + str(self.id) + ' added Block: ' + str(self.my_blockchain.chain[len(self.my_blockchain.chain) - 1]))
        self.logger.debug('Node ' + str(self.id) + ' sending new blockchain to others')
        json_str = jsonpickle.encode(self.my_blockchain)
        self.send_to_nodes(json_str)

    def validate_and_update_blockchain(self, bc: blockchain):
        """
        Checks if the blockchain of this node is equal or longer to a given blockchain,
        if not, it is replaced with the newly arrived blockchain
        :param bc: blockchain the blockchain this node's blockchain is compared to
        :return:
        """
        if not self.my_blockchain.compare_to(bc):
            self.logger.info('Node ' + str(self.id) + ' Updated Blockchain')
            self.my_blockchain = bc
        self.logger.debug('Node ' + str(self.id) + ' Blockchain was not updated')

    def __init__(self, host, port, data: Generic[T], id=None, callback=None, max_connections=0):
        super(ComputationNode, self).__init__(host, port, id, callback, max_connections)
        self.logger = logging.getLogger(__name__)
        self.my_blockchain = blockchain.Blockchain(data)
        self.logger.debug('Node ' + str(self.id) + ' Started')

    # Implement functions for p2p
    # based on the work of
    def outbound_node_connected(self, node):
        logging.debug('Node ' + str(self.id) + ' outbound_node_connected: ' + node.id)
        self.nodes_outbound.append(node)

    def inbound_node_connected(self, node):
        logging.debug('Node ' + str(self.id) + ' inbound_node_connected: ' + node.id)
        self.nodes_inbound.append(node)

    def inbound_node_disconnected(self, node):
        logging.debug('Node ' + str(self.id) + ' inbound_node_disconnected: ' + node.id)
        self.nodes_inbound.remove(node)

    def outbound_node_disconnected(self, node):
        logging.debug(' outbound_node_disconnected: ' + node.id)
        self.nodes_outbound.remove(node)

    def node_message(self, node, data):
        # parse the json object into a python object again
        self.logger.info('Node ' + self.id + ' received Blockchain from ' + node.id)
        string_dat = str(data)
        string_dat = string_dat.replace("\'", "\"")
        obj = jsonpickle.decode(string_dat)
        self.validate_and_update_blockchain(obj)

    def node_disconnect_with_outbound_node(self, node):
        logging.debug('Node ' + str(self.id) + ' node wants to disconnect with oher outbound node: ' + node.id)

    def node_request_to_stop(self):
        logging.debug('Node ' + str(self.id) + ' node is requested to stop')
