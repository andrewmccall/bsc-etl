

from ethereum_dasm.evmdasm import EvmCode, Contract
from ethereumetl.service.eth_contract_service import ContractWrapper, EthContractService, clean_bytecode


class BscContractService(EthContractService):

    def get_function_sighashes(self, bytecode):
        bytecode = clean_bytecode(bytecode)
        if bytecode is not None:
            evm_code = EvmCode(contract=Contract(bytecode=bytecode), static_analysis=False, dynamic_analysis=False)
            evm_code.disassemble(bytecode)
            basic_blocks = evm_code.basicblocks
            if basic_blocks and len(basic_blocks) > 0:

                push4_instructions = list()
                for init_block in evm_code.basicblocks:
                    instructions = init_block.instructions
                    push4_instructions.extend(([inst for inst in instructions if inst.name == 'PUSH4']))    
                return sorted(list(set('0x' + inst.operand for inst in push4_instructions)))
            else:
                return []
        else:
            return []

    def is_bep20_contract(self, function_sighashes):
        c = ContractWrapper(function_sighashes)
        return c.implements('totalSupply()') and \
            c.implements('symbol()') and \
            c.implements('balanceOf(address)') and \
            c.implements('transfer(address,uint256)') and \
            c.implements('transferFrom(address,address,uint256)') and \
            c.implements('approve(address,uint256)') and \
            c.implements('allowance(address,address)')
