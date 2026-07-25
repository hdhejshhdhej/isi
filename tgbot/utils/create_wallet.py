import asyncio

from tgbot.utils.usdt_trc20 import NodeTron
from dataclasses import dataclass
from web3 import Web3


@dataclass
class Contract:
    symbol: str
    address: str
    decimals: int

    def __init__(self, symbol: str, address: str, decimals: int = None):
        self.symbol = symbol  # unimportant, only show
        self.address = Web3.to_checksum_address(address)
        self.decimals = decimals


async def create_wallet(token):
    if token == 'BUSD' :
        from eth_account import Account
        acct = Account.create('KEYSMASH FJAFJKLDSKF7JKFDJ 1530')
        return acct.address, acct.key.hex()



    elif token == 'USDT_TRC20':
        node = NodeTron()
        new_adres = node.new_adress()
        adress, key = new_adres['base58check_address'], new_adres['private_key']
        return adress, key

DECIMALS = 10 ** 18
async def check_payments(token, address):
    if token == 'BNB':
        from web3 import Web3
        bsc = "https://bsc-dataseed.binance.org/"
        web3 = Web3(Web3.HTTPProvider(bsc))
        balance = web3.eth.get_balance(web3.to_checksum_address(address)) / DECIMALS
        return balance
    elif token == "BUSD" or token == "USDT_BEP20":
        # address = "0xe2d3A739EFFCd3A99387d015E260eEFAc72EBea1"
        from web3 import Web3
        BUSD='[{"inputs":[],"payable":false,"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"spender","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"previousOwner","type":"address"},{"indexed":true,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Transfer","type":"event"},{"constant":true,"inputs":[],"name":"_decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"_name","outputs":[{"internalType":"string","name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"_symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"spender","type":"address"}],"name":"allowance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"approve","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"burn","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"subtractedValue","type":"uint256"}],"name":"decreaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"getOwner","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"addedValue","type":"uint256"}],"name":"increaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"mint","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[],"name":"renounceOwnership","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transfer","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"sender","type":"address"},{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transferFrom","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"}]'
        bsc = "https://bsc-dataseed.binance.org/"
        web3 = Web3(Web3.HTTPProvider(bsc))

        if token == "BUSD":
            busd_address = Web3.to_checksum_address('0xe9e7cea3dedca5984780bafc599bd69add087d56')
            contract = web3.eth.contract(busd_address, abi=BUSD)
        else:
            usdt_address = Web3.to_checksum_address('0x55d398326f99059fF775485246999027B3197955')
            contract = web3.eth.contract(usdt_address, abi=BUSD)


        ballance = int(contract.functions.balanceOf(address).call())/DECIMALS
        return ballance


    elif token == 'USDT_TRC20':
        tron = NodeTron()
        balance = await tron.get_token_balance(address, 'USDT')
        await tron.close_session()
        return balance
    elif token == "TRX":
        tron = NodeTron()
        balance = await tron.get_balance(address)
        await tron.close_session()
        return balance


async def get_last_tx(adress):
    from web3 import Web3
    bsc = "https://bsc-dataseed.binance.org/"
    web3 = Web3(Web3.HTTPProvider(bsc))
    # print(1)
    # print(web3.toJSON(web3.eth.wait_for_transaction_receipt(adress).logs))
    # block = web3.eth.get_block('latest')
    # print(block)
    # txs = web3.eth.getTransactionCount(adress)
    # print(txs)
