import json
import aiohttp


async def get_tokens_in_dollars(dtk):
    vall = {'BTC': 0.0, 'USDT_TRC20': 0.0, 'BNB': 0.0, 'LTC': 0.0, 'Solana': 0.0}
    coin = {'BTC': 'bitcoin', 'USDT_TRC20': "tether", 'BNB': 'binancecoin', 'LTC': 'litecoin', "Solana": 'solana'}
    'https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd'
    for k in dtk:
        if k.startswith("balance_"):
            if float(dtk[k]) > 0:
                token = k[8:]
                async with aiohttp.ClientSession() as session:
                    async with session.get(
                            f"https://api.coingecko.com/api/v3/simple/price?ids={coin[token]}&vs_currencies=usd") as resp:
                        course = (await resp.json())[coin[token]]['usd']
                        vall[token] = round(course * dtk[k], 2)
    return vall

async def tokenn_in_dollars(token, balance):
    coin = {'BTC': 'bitcoin',
            'USDT_TRC20': "tether",
            'USDC_TRC20': "tether",
            'TRX': "tron",
            'BNB': 'binancecoin',
            'LTC': 'litecoin',
            "Solana": 'solana'}
    async with aiohttp.ClientSession() as session:
        async with session.get(
                f"https://api.coingecko.com/api/v3/simple/price?ids={coin[token]}&vs_currencies=usd") as resp:
            course = (await resp.json())[coin[token]]['usd']
    return round(float(course) * float(balance), 2)

async def get_rub_in_dollars(balance):
    async with aiohttp.ClientSession() as session:
        async with session.get(
                f"https://api.coingecko.com/api/v3/simple/price?ids=tether&vs_currencies=rub") as resp:

            course = (await resp.json())['tether']['rub']

    return float(round(float(balance) / course, 2))

async def get_rub_course():
    async with aiohttp.ClientSession() as session:
        async with session.get(
                f"https://api.coingecko.com/api/v3/simple/price?ids=tether&vs_currencies=rub") as resp:

            course = (await resp.json())['tether']['rub']
            print(await resp.json())
    return int(round(float(course), 2))

async def get_dollars_in_rub(balance):
    async with aiohttp.ClientSession() as session:
        async with session.get(
                f"https://api.coingecko.com/api/v3/simple/price?ids=tether&vs_currencies=rub") as resp:

            course = (await resp.json())['tether']['rub']

    return float(round(float(balance) * course, 2))