import jsonpickle

from p2pnetwork.node import Node
import blockchain
from typing import TypeVar, Generic

T = TypeVar('T')


class ComputationNode(Node):
    """
    Class that represents a Computing Node
    """
    my_blockchain: blockchain

    def add_new_data(self, data: Generic[T]):
        """
        Add new Data to the Blockchain of this Node
        :param data: Generic[T] data that is added to the blockchain
        :return: nothing
        """
        print('started adding data: ' + str(data))
        self.my_blockchain.add_data(data)
        print('sending new blockchain to others')
        json_str = jsonpickle.encode(self.my_blockchain)
        self.send_to_nodes(json_str)

    def validate_and_update_blockchain(self, bc: blockchain):
        """
        Checks if the blockchain of this node is equal or longer to a given blockchain,
        if not, it is replaced with the newly arrived blockchain
        :param bc: blockchain the blockchain this node's blockchain is compared to
        :return:
        """
        print(bc.validate_blockchain())
        if not self.my_blockchain.compare_to(bc):
            print('Updated Blockchain')
            self.my_blockchain = bc
        print('Node (' + str(self.id) + ') Blockchain was not updated')

    def __init__(self, host, port, data: Generic[T], id=None, callback=None, max_connections=0):
        super(ComputationNode, self).__init__(host, port, id, callback, max_connections)
        self.my_blockchain = blockchain.Blockchain(data)
        print("MyPeer2PeerNode: Started")

    # Implement functions for p2p
    def outbound_node_connected(self, node):
        print("outbound_node_connected (" + self.id + "): " + node.id)
        self.nodes_outbound.append(node)

    def inbound_node_connected(self, node):
        print("inbound_node_connected: (" + self.id + "): " + node.id)
        self.nodes_inbound.append(node)

    def inbound_node_disconnected(self, node):
        print("inbound_node_disconnected: (" + self.id + "): " + node.id)
        self.nodes_inbound.remove(node)

    def outbound_node_disconnected(self, node):
        print("outbound_node_disconnected: (" + self.id + "): " + node.id)
        self.nodes_outbound.remove(node)

    def node_message(self, node, data):
        # parse the json object into a python object again
        print("Node (" + self.id + ") received Blockchain from " + node.id)
        string_dat = str(data)
        string_dat = string_dat.replace("\'", "\"")
        obj = jsonpickle.decode(string_dat)
        self.validate_and_update_blockchain(obj)

    def node_disconnect_with_outbound_node(self, node):
        print("node wants to disconnect with oher outbound node: (" + self.id + "): " + node.id)

    def node_request_to_stop(self):
        print("node is requested to stop (" + self.id + "): ")
