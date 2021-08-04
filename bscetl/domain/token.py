

from ethereumetl.domain.token import EthToken


class BscToken(EthToken):
    def __init__(self):
        self.address = None
        self.symbol = None
        self.name = None
        self.decimals = None
        self.total_supply = None
        self.block_number = None
        self.owner = None