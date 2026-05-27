import hashlib
import datetime

class Block:

    def __init__(self, index, data, previous_hash):

        self.index = index
        self.timestamp = str(datetime.datetime.now())
        self.data = data
        self.previous_hash = previous_hash

        self.hash = self.calculate_hash()

    def calculate_hash(self):

        text = (
            str(self.index)
            + self.timestamp
            + self.data
            + self.previous_hash
        )

        return hashlib.sha256(text.encode()).hexdigest()


class Blockchain:

    def __init__(self):

        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):

        return Block(0, "Genesis", "0")

    def add_block(self, data):

        previous = self.chain[-1]

        new_block = Block(
            len(self.chain),
            data,
            previous.hash
        )

        self.chain.append(new_block)