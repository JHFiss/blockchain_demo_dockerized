import string
import hashlib
from typing import TypeVar, Generic

T = TypeVar('T')


class Block(Generic[T]):
    """
    Implementation of a block for a blockchain that can contain arbitrary data
    """
    this_hash: string
    prev_hash: string
    data: T
    time_stamp: int
    nonce = 0
    MINE_COND: string = '300597'

    def calc_hash(self):
        """
        Generates a hash for a block instance
        """
        hash_data = self.prev_hash + str(self.data) + str(self.time_stamp) + str(self.nonce) + self.MINE_COND
        return hashlib.sha3_256(hash_data.encode('utf-8')).hexdigest()

    def mine_this_block(self):
        """
        Proof of work function for a block
        Generates new hashes and increases nonce until the created hash contains the value defined in ``mine_cond``
        """

        mine_hash: string = self.calc_hash()
        while self.MINE_COND not in mine_hash:
            self.nonce += 1
            mine_hash = self.calc_hash()
            # Print the current value of nonce for debug and demonstration purposes
            # print(self.nonce)
        self.this_hash = mine_hash
        return mine_hash

    def __init__(self, prev_hash: string, data: T, timestamp: int):
        self.prev_hash = prev_hash
        self.data = data
        self.time_stamp = timestamp
        self.this_hash = self.calc_hash()

        # print the values of a block after initialisation for debug and demonstration purposes
        print(self.this_hash)
        print(self.prev_hash)
        print(self.data)
        print(self.time_stamp)

    def __str__(self):
        return "{\n previous Hash: %s \n " \
               "Hash: %s \n " \
               "Data: %s \n " \
               "Nonce: %s \n " \
               "Timestamp: %s \n " \
               "Mine Cond: %s \n" \
               "}" % (self.prev_hash, self.this_hash, self.data, self.nonce, self.time_stamp, self.MINE_COND)



