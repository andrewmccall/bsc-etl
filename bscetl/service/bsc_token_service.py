from ethereumetl.service.eth_token_service import EthTokenService
from bscetl.domain.token import BscToken
from bscetl.bep20_abi import BEP20_ABI

class BscTokenService(EthTokenService):
    def __init__(self, web3, function_call_result_transformer=None):
        self._web3 = web3
        self._function_call_result_transformer = function_call_result_transformer

    def get_token(self, token_address):
        checksum_address = self._web3.toChecksumAddress(token_address)
        contract = self._web3.eth.contract(address=checksum_address, abi=BEP20_ABI)

        symbol = self._get_first_result(contract.functions.symbol(), contract.functions.SYMBOL())
        name = self._get_first_result(contract.functions.name(), contract.functions.NAME())
        decimals = self._get_first_result(contract.functions.decimals(), contract.functions.DECIMALS())
        total_supply = self._get_first_result(contract.functions.totalSupply())
        owner = self._get_first_result(contract.functions.owner())

        token = BscToken()
        token.address = token_address
        token.symbol = symbol
        token.name = name
        token.decimals = decimals
        token.total_supply = total_supply
        token.owner = owner

        return token