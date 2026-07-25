import json

from tgbot.config import API_KEY_TRON, MAIN_NET_TRON
import aiohttp

from tronpy.tron import Tron, HTTPProvider, PrivateKey
from tronpy.async_tron import AsyncTron, AsyncHTTPProvider, PrivateKey

import decimal
from decimal import localcontext, Decimal
import tronpy.exceptions


decimals = decimal.Context()

SUN = decimal.Decimal("1000000")
MIN_SUN = 0
MAX_SUN = 2 ** 256 - 1


async def get_course_usdt():
    async with aiohttp.ClientSession() as session:
        async with session.get("https://coincodex.com/api/coincodex/get_coin/USDT") as resp:
            response = await resp.text()
            list_currency = json.loads(response)
            return list_currency['last_price_usd']


async def get_usdt_in_dollars(amount_usdt):
    course = await get_course_usdt()
    return round(course * amount_usdt, 2)


def from_sun(num):
    """
    Helper function that will convert a value in TRX to SUN
    :param num: Value in TRX to convert to SUN
    """
    if num == 0:
        return 0
    if num < 0 or num > 2 ** 256 - 1:
        raise ValueError("Value must be between 1 and 2**256 - 1")

    unit_value = SUN

    with localcontext() as ctx:
        ctx.prec = 999
        d_num = Decimal(value=num, context=ctx)
        result = d_num / unit_value
    return result


def to_sun(num) -> int:
    """
    Helper function that will convert a value in TRX to SUN
    :param num: Value in TRX to convert to SUN
    """
    if isinstance(num, int) or isinstance(num, str):
        d_num = Decimal(value=num)
    elif isinstance(num, float):
        d_num = Decimal(value=str(num))
    elif isinstance(num, Decimal):
        d_num = num
    else:
        raise TypeError("Unsupported type. Must be one of integer, float, or string")

    s_num = str(num)
    unit_value = SUN

    if d_num == 0:
        return 0

    if d_num < 1 and "." in s_num:
        with localcontext() as ctx:
            multiplier = len(s_num) - s_num.index(".") - 1
            ctx.prec = multiplier
            d_num = Decimal(value=num, context=ctx) * 10 ** multiplier
        unit_value /= 10 ** multiplier

    with localcontext() as ctx:
        ctx.prec = 999
        result = Decimal(value=d_num, context=ctx) * unit_value
    if result < MIN_SUN or result > MAX_SUN:
        raise ValueError("Resulting wei value must be between 1 and 2**256 - 1")

    return int(result)


class TokenDB:

    @staticmethod
    def get_token(cur):
        USDT = {
            "name": "Tether USD",
            "symbol": "USDT",
            "address": "TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t",
            "decimals": 6,
            "bandwidth": 345,
            "feeLimit": 2000,
            "isBalanceNotNullEnergy": 14631,
            "isBalanceNullEnergy": 29631
        }
        USDC = {
            "name": "USD Coin",
            "symbol": "USDC",
            "address": "TEkxiTehnzSmSe2XqrBj4w32RUN966rdz8",
            "decimals": 6,
            "bandwidth": 345,
            "feeLimit": 2000,
            "isBalanceNotNullEnergy": 14380,
            "isBalanceNullEnergy": 28827
        }
        if cur == "USDT":
            return USDT
        else:
            return USDC


class NodeTron:
    db = TokenDB()

    def __init__(self):
        """Connect to Tron Node"""

        self.provider = AsyncHTTPProvider(endpoint_uri=MAIN_NET_TRON, api_key=API_KEY_TRON)
        self.node = AsyncTron(provider=self.provider)
        self.provider_http = HTTPProvider(endpoint_uri=MAIN_NET_TRON, api_key=API_KEY_TRON)
        self.node_http = Tron(provider=self.provider_http)

    async def get_balance(self, address):
        """Get TRX balance"""
        try:
            balance = await self.node.get_account_balance(address)
            return decimals.create_decimal("%.8f" % balance) if balance > 0 else 0
        except tronpy.exceptions.AddressNotFound:
            return 0

    def new_adress(self):
        address = self.node.generate_address()
        if self.node.is_address(str(address['base58check_address'])):
            return self.node.generate_address()

    def is_valid(self, address):
        is_address = self.node.is_address(str(address))
        return is_address

    async def get_token_balance(self, address, token):
        """
        Get TRC20 tokens balance
        :param address: Wallet address
        :param token: Token symbol or contract address
        """
        balance = 0
        token_dict = self.db.get_token(token)
        # Connecting to a smart contract
        contract = await self.node.get_contract(addr=token_dict["address"])
        result = await contract.functions.balanceOf(address)
        if int(result) > 0:
            balance = decimals.create_decimal(result) / decimals.create_decimal(10 ** token_dict["decimals"])
        return decimals.create_decimal("%.8f" % balance) if float(balance) > 0 else balance

    async def unspents_token(self, address, token):
        async with aiohttp.ClientSession() as session:
            async with session.get(
                    'https://apilist.tronscan.org/api/transaction?sort=timestamp&address=' + address) as resp:
                txs = await resp.json()
        token_dict = self.db.get_token(token)
        for tx in txs['data']:
            if (token_dict["address"] in tx['toAddressList']) and tx['contractRet'] == 'SUCCESS':
                return True
        return False

    async def get_account_energy(self, address):
        """
        Returns energy data from account.
        :param address: Address of account
        """
        try:
            account_resources = await self.node.get_account_resource(address)

        except:
            account_resources = {}
        energy = account_resources["EnergyLimit"] if "EnergyLimit" in account_resources else 0
        energy_used = account_resources["EnergyUsed"] if "EnergyUsed" in account_resources else 0
        total_energy = energy - energy_used if energy > 0 and energy_used > 0 else 0
        return {
            "energy": energy,
            "energyUsed": energy_used,
            "totalEnergy": total_energy
        }

    async def get_energy(self, address: str, energy: int) -> int:
        """If the user has enough energy."""

        total_energy = (await self.get_account_energy(address=address))["totalEnergy"]

        if int(total_energy) <= 0:
            return energy
        elif energy - int(total_energy) <= 0:
            return 0
        else:
            return energy - int(total_energy)

    async def get_chain_parameters_by_name(self, name: str) -> int:
        parameters = await self.node.get_chain_parameters()
        for parameter in parameters:
            if parameter["key"] == name:
                return parameter["value"]
        else:
            return 0

    async def calculate_burn_energy(self, amount) -> Decimal:
        """
        Returns the amount of energy generated by burning TRX
        :param amount: Amount of TRX in sun
        :return:
        """
        energy_fee = await self.get_chain_parameters_by_name(name="getEnergyFee")
        if float(energy_fee) == 0:
            return decimals.create_decimal(0)
        fee = (amount / energy_fee) * 1_000_000
        return decimals.create_decimal(fee)

    async def get_account_bandwidth(self, address):
        """
        Returns bandwidth data from account.
        :param address: Address of account
        """
        try:
            account_resources = await self.node.get_account_resource(address)
        except:
            account_resources = {}
        free_bandwidth = account_resources["freeNetLimit"] if "freeNetLimit" in account_resources else 0
        free_bandwidth_used = account_resources["freeNetUsed"] if "freeNetUsed" in account_resources else 0
        total_bandwidth = free_bandwidth - free_bandwidth_used
        return {
            "freeBandwidth": free_bandwidth,
            "freeBandwidthUsed": free_bandwidth_used,
            "totalBandwidth": total_bandwidth
        }

    async def get_optimal_fee(self, from_address, to_address, token=None) -> json:
        """Get optimal fee"""
        fee = 0
        energy = 0
        try:
            _ = await self.node.get_account(to_address)
        except tronpy.exceptions.AddressNotFound:
            fee += 1.0
        if token is None:
            bd = 267
        else:
            token_dict = self.db.get_token(token)
            # Connecting to a smart contract

            contract = await self.node.get_contract(addr=token_dict["address"])
            bal_token = float(await contract.functions.balanceOf(to_address))

            if bal_token > 0:
                energy = token_dict["isBalanceNotNullEnergy"]
            else:
                energy = token_dict["isBalanceNullEnergy"]

            fee = await self.get_energy(address=from_address, energy=energy) / await self.calculate_burn_energy(1)
            bd = token_dict["bandwidth"]
        if int((await self.get_account_bandwidth(address=from_address))["totalBandwidth"]) <= bd:
            fee += decimals.create_decimal(267) / 1_000
        return {
            "fee": "%.6f" % fee if fee > 0 else fee,
            "energy": energy,
            "bandwidth": bd
        }

    async def create_sign_transaction(self, private_key, address, to_address, amount=None):

        """Create a transaction TRX"""
        # Checks the correctness of the data entered by users
        private_key = PrivateKey(private_key_bytes=bytes.fromhex(private_key))
        balance = await self.get_balance(address)
        if balance > 1:
            cms = 0.1
        else:
            cms = 0
        resources = await self.get_optimal_fee(from_address=address, to_address=to_address)

        if amount == None:
            amount = to_sun(float(balance) - (float(resources['fee']) + cms))
        else:
            amount = to_sun(float(amount))
        # Creates and build a transaction
        txb = self.node.trx.transfer(from_=address, to=to_address, amount=amount)
        txn = await txb.build()
        sign_transaction = await txn.sign(private_key).broadcast()

        await sign_transaction.wait()
        return sign_transaction.txid

    async def create_sign_trc20_transactions(self, private_key, address, to_address, token, amount=None):
        """Create a transaction TRC20"""
        # Token information
        token_dict = self.db.get_token(token)
        # Connecting to a smart contract
        contract = self.node_http.get_contract(addr=token_dict["address"])
        # Let's get the amount for the offspring in decimal
        if amount == None:
            bal = await self.get_token_balance(address, token)
            amount = int(float(bal) * 10 ** int(token_dict["decimals"]))
        else:
            amount = int(float(amount) * 10 ** int(token_dict["decimals"]))
        # Checks whether the user has a tokens balance to transfer
        if contract.functions.balanceOf(address) * 10 ** int(token_dict["decimals"]) < amount:
            raise Exception("You do not have enough funds on your balance to make a transaction!!!")
        txn = contract.functions.transfer(to_address, amount).with_owner(address).build()
        sign_transaction = txn.sign(priv_key=PrivateKey(private_key_bytes=bytes.fromhex(private_key)))
        sign_transaction.broadcast().wait()
        return sign_transaction.txid


    async def close_session(self):
        if self.node is not None:
            await self.node.close()



import asyncio

async def main():
    node = NodeTron()

    print(wall)
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main()) # передайте точку входа
    finally:
        # действия на выходе, если требуются
        pass


# {'base58check_address': 'TR4SurvpPCy1vUybV9KZoGKiKRxNWJ4xpN',
# 'hex_address': '41a58794105e0015820fae04ef3dcb7533e9462735',
# 'private_key': 'e62f6ff91a1179bc6f5f0d1fe0594830ff2098590f3bb3852129357d3b1bd8a5',
# 'public_key': '7bb229240246a5c674e4139da099bc7fa6edaeec7fba7468693dad6875de02618e7e339e66d6eb7f45ad21129188a1e26953bb0c0f2e597d18803a1e35b244de'}