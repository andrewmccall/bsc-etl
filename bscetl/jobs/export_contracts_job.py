# MIT License
#
# Copyright (c) 2018 Evgeny Medvedev, evge.medvedev@gmail.com
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


import json

from ethereumetl.executors.batch_work_executor import BatchWorkExecutor
from blockchainetl.jobs.base_job import BaseJob
from ethereumetl.json_rpc_requests import generate_get_code_json_rpc
from bscetl.mappers.contract_mapper import BscContractMapper

from bscetl.service.bsc_contract_service import BscContractService
from ethereumetl.utils import rpc_response_to_result

from ethereumetl.jobs.export_contracts_job import ExportContractsJob as EthExportContractsJob


# Exports contracts bytecode
class ExportContractsJob(EthExportContractsJob):
    def __init__(
            self,
            contract_addresses_iterable,
            batch_size,
            batch_web3_provider,
            max_workers,
            item_exporter):
        self.batch_web3_provider = batch_web3_provider
        self.contract_addresses_iterable = contract_addresses_iterable

        self.batch_work_executor = BatchWorkExecutor(batch_size, max_workers)
        self.item_exporter = item_exporter

        self.contract_service = BscContractService()
        self.contract_mapper = BscContractMapper()
        print("SEE ME!")


    def _get_contract(self, contract_address, rpc_result):
        print("Getting contract {}".format(contract_address))
        contract = self.contract_mapper.rpc_result_to_contract(contract_address, rpc_result)
        bytecode = contract.bytecode
        function_sighashes = self.contract_service.get_function_sighashes(bytecode)

        contract.function_sighashes = function_sighashes
        contract.is_erc20 = self.contract_service.is_erc20_contract(function_sighashes)
        contract.is_erc721 = self.contract_service.is_erc721_contract(function_sighashes)
        contract.is_bep20 = self.contract_service.is_bep20_contract(function_sighashes)

        return contract
