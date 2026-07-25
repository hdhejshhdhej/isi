import tgbot.config as cfg
import tgbot.utils.usdt_trc20 as usdt
import asyncio


async def send_tokens(from_address, from_private_key, to_address, amount, token, deposit=False):
    amount = f'{float(amount):.8f}'

    tron = usdt.NodeTron()
    if token == "USDT_TRC20":
        main_adress, main_key = cfg.ADDRESS_USDT_TRC20, cfg.PK_USDT_TRC20
        if deposit:
            # считаем комиссию для отправки USDT основной адрес
            fee = 30
            # Отправляем trx c основного адреса   private_key, address, to_address, amount=None

            try:
                await tron.create_sign_transaction(private_key=main_key, address=main_adress, to_address=from_address,
                                                   amount=fee)
            except:
                return 'error', 'Недостаточно TRX на оплату комиссии USDT"'
            # Отправляем USDT на основной адрес private_key, address, to_address,  token, amount=None
            try:
                balance_user_token = await tron.get_token_balance(from_address, 'USDT')
                if balance_user_token == 0:
                    return 'error', "Хитрожопый юзер"
                tx = await tron.create_sign_trc20_transactions(private_key=from_private_key,
                                                               address=from_address,
                                                               to_address=main_adress,
                                                               token='USDT')
                #     смоторим баланс тронов на кошелье пользователя
                balance_user_trx = await tron.get_balance(from_address)
                balance_user_token = await tron.get_token_balance(from_address, 'USDT')
                if balance_user_token > 0.1:
                    return 'error', str(tx)

                if balance_user_trx > 0:
                    for i in range(3):
                        try:
                            await tron.create_sign_transaction(private_key=from_private_key,
                                                               address=from_address,
                                                               to_address=main_adress, )

                        except:
                            pass
            except Exception as e:
                return 'error', str(e)
        else:
            try:
                thn = await tron.create_sign_trc20_transactions(private_key=main_key,
                                                                address=main_adress,
                                                                to_address=to_address,
                                                                token='USDT',
                                                                amount=amount)
                return "https://tronscan.org/#/transaction/" + thn
            except Exception as e:
                return 'error', str(e)
    elif token == 'BUSD' or token == "USDT_BEP20":
        from web3 import Web3

        bsc_url = "https://bsc-dataseed.binance.org/"
        web3 = Web3(Web3.HTTPProvider(bsc_url))
        main_adress, main_key = cfg.ADDRESS_BNB, cfg.PK_BNB
        gas_price = web3.to_wei('5', 'gwei')
        BUSD = '[{"inputs":[],"payable":false,"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"spender","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"previousOwner","type":"address"},{"indexed":true,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Transfer","type":"event"},{"constant":true,"inputs":[],"name":"_decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"_name","outputs":[{"internalType":"string","name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"_symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"spender","type":"address"}],"name":"allowance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"approve","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"burn","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"subtractedValue","type":"uint256"}],"name":"decreaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"getOwner","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"addedValue","type":"uint256"}],"name":"increaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"mint","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[],"name":"renounceOwnership","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transfer","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"sender","type":"address"},{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transferFrom","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"}]'
        # busdcontract = web3.eth.contract(busd_address, abi=BUSD)
        if token == "BUSD":
            busd_address = Web3.to_checksum_address('0xe9e7cea3dedca5984780bafc599bd69add087d56')
            busdcontract = web3.eth.contract(busd_address, abi=BUSD)
        else:
            usdt_address = Web3.to_checksum_address('0x55d398326f99059fF775485246999027B3197955')
            busdcontract = web3.eth.contract(usdt_address, abi=BUSD)
        if deposit:
            ballance = int(busdcontract.functions.balanceOf(from_address).call())
            try:
                nonce = web3.eth.get_transaction_count(main_adress)
                token_tx = {
                    'nonce': nonce,
                    'to': web3.to_checksum_address(from_address),
                    'value': 210000 * gas_price,
                    'gas': 21000,
                    'gasPrice': gas_price,
                }

                signed_tx = web3.eth.account.sign_transaction(token_tx, main_key)
                tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
                trans = web3.to_hex(tx_hash)
                transaction = web3.eth.get_transaction(trans)

                await asyncio.sleep(5)

                ballance = int(busdcontract.functions.balanceOf(from_address).call())
                if ballance == 0:
                    return 'error', str("Хитрожопый юзер")
                nonce = web3.eth.get_transaction_count(from_address)
                token_tx = {
                    'nonce': nonce,
                    'from': web3.to_checksum_address(from_address),
                    'value': 0,
                    'gas': 210000,
                    'gasPrice': gas_price
                }
                transaction = busdcontract.functions.transfer(main_adress,
                                                              web3.to_wei(amount, "ether")).build_transaction(token_tx)
                signed_txn = web3.eth.account.sign_transaction(transaction, from_private_key)
                txn_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
                web3.eth.wait_for_transaction_receipt(txn_hash, timeout=120, poll_latency=0.1)

                ballance = int(busdcontract.functions.balanceOf(from_address).call())

                if ballance > 0:
                    return 'error', str(txn_hash.hex())

                return txn_hash.hex()
            except Exception as e:
                return 'error', str(e)
        else:

            try:
                nonce = web3.eth.get_transaction_count(main_adress)
                token_tx = {
                    'nonce': nonce,
                    'from': web3.to_checksum_address(main_adress),
                    'value': 0,
                    'gas': 70000,
                    'gasPrice': gas_price
                }
                transaction = busdcontract.functions.transfer(web3.to_checksum_address(to_address),
                                                              web3.to_wei(amount, "ether")).build_transaction(
                    token_tx)

                signed_txn = web3.eth.account.sign_transaction(transaction, main_key)
                txn_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
                return "https://bscscan.com/tx/" + txn_hash.hex()

            except Exception as e:
                print(e)
                return 'error', str(e)
    elif token == 'BNB':
        from web3 import Web3
        bsc_url = "https://bsc-dataseed.binance.org/"
        web3 = Web3(Web3.HTTPProvider(bsc_url))
        main_adress, main_key = cfg.ADDRESS_BNB, cfg.PK_BNB
        to_address = main_adress
        try:
            nonce = web3.eth.get_transaction_count(from_address)
            balance = web3.to_wei(web3.eth.get_balance(web3.to_checksum_address(from_address)) / 10 ** 18, 'ether'),
            gas_price = web3.to_wei('5', 'gwei')
            total_balance = balance[0] - (21000 * gas_price)
            token_tx = {
                'nonce': nonce,
                'to': web3.to_checksum_address(to_address),
                'value': total_balance,
                'gas': 21000,
                'gasPrice': gas_price
            }
            signed_tx = web3.eth.account.sign_transaction(token_tx, from_private_key)
            tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
            trans = web3.to_hex(tx_hash)
            transaction = web3.eth.get_transaction(trans)
            return transaction
        except Exception as e:
            return 'error', str(e)
    elif token == 'TRX':
        main_adress, main_key = cfg.ADDRESS_USDT_TRC20, cfg.PK_USDT_TRC20
        tron = usdt.NodeTron()
        ballance = await tron.get_balance(from_address)
        if ballance < 1:
            return 'error', str("Хитрожопый юзер")
        try:
            tx = await tron.create_sign_transaction(private_key=from_private_key,
                                                    address=from_address,
                                                    to_address=main_adress, )
            for i in range(3):
                try:
                    await tron.create_sign_transaction(private_key=from_private_key,
                                                       address=from_address,
                                                       to_address=main_adress, )
                except:
                    pass
            return str(tx)
        except Exception as e:
            for i in range(3):
                try:
                    await tron.create_sign_transaction(private_key=from_private_key,
                                                       address=from_address,
                                                       to_address=main_adress, )
                except:
                    pass
            return 'error', str(e)
