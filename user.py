from database import DataAccessObject
import requests
from bipwallet import wallet
import bipwallet.utils as bipwalletutils
import pyetherbalance 

class User:
    def __init__(self, telegram_id):
        self.database = DataAccessObject()
        self.__telegram_id = telegram_id
        self.__is_exists = bool(self.database.get_user_data(self.__telegram_id))
        if not self.__is_exists:
            btc_wallet = self.__create_btc_wallet()
            self.__btc_wallet_number = btc_wallet["address"]
            self.__btc_private = btc_wallet["private"]
            self.__btc_public = btc_wallet["public"]
            self.__wif = btc_wallet["wif"]

            eth_wallet = self.__create_eth_wallet()
            self.__eth_wallet_number = eth_wallet["address"]
            self.__eth_private = eth_wallet["private"]
            self.__eth_public = eth_wallet["public"]

            print("WIFWIF: ", self.__wif)
            self.database.save_user(self.__telegram_id, 
                                    self.__btc_wallet_number, 
                                    self.__btc_private, 
                                    self.__btc_public,
                                    self.__wif.decode("utf-8"),
                                    self.__eth_wallet_number,
                                    self.__eth_private,
                                    self.__eth_public)
            user_data = self.database.get_user_data(telegram_id)
            print(f'''Creating user with:
                Telegram id: {self.__telegram_id}
                BTC Wallet number: {user_data["btc_wallet_number"]}
                BTC Private key: {user_data["btc_private_key"]}
                BTC Public key: {user_data["btc_public_key"]}
                BTC Wif: {user_data["btc_wif"]}
                eth Wallet number: {user_data["eth_wallet_number"]}
                eth Private key: {user_data["eth_private_key"]}
                eth Public key: {user_data["eth_public_key"]}
            ''')
        else:
            user_data = self.database.get_user_data(telegram_id)
            self.__btc_wallet_number = user_data["btc_wallet_number"]
            self.__btc_private = user_data["btc_private_key"]
            self.__btc_public = user_data["btc_public_key"]
            self.__wif = user_data["btc_wif"]

            self.__eth_wallet_number = user_data["eth_wallet_number"]
            self.__eth_private = user_data["eth_private_key"]
            self.__eth_public = user_data["eth_public_key"]

            print(f'''Getting user with:
                Telegram id: {self.__telegram_id}
                BTC Wallet number: {user_data["btc_wallet_number"]}
                BTC Private key: {user_data["btc_private_key"]}
                BTC Public key: {user_data["btc_public_key"]}
                BTC Wif: {user_data["btc_wif"]}
                eth Wallet number: {user_data["eth_wallet_number"]}
                eth Private key: {user_data["eth_private_key"]}
                eth Public key: {user_data["eth_public_key"]}
            ''')

    def __create_btc_wallet(self):
        seed = wallet.generate_mnemonic()

        wallet_data_raw = wallet.create_wallet(network="BTC", seed=seed, children=1)
        private_key = wallet_data_raw["private_key"]
        public_key = wallet_data_raw["public_key"]
        address = wallet_data_raw["address"]
        wif = wallet_data_raw["wif"]

        wallet_data = {"private": private_key,
				  "public": public_key,
				  "address": address,
                  "wif": wif}
        
        return wallet_data
    
    def __create_eth_wallet(self):
        seed = wallet.generate_mnemonic()

        wallet_data_raw = wallet.create_wallet(network="ETH", seed=seed, children=1)
        private_key = wallet_data_raw["private_key"]
        public_key = wallet_data_raw["public_key"]
        address = wallet_data_raw["address"]

        wallet_data = {"private": private_key,
                  "public": public_key,
                  "address": address}
        
        return wallet_data
    
    def get_balance_data(self):
        btc_balance = requests.get("https://blockchain.info/balance?active=%s" % self.__btc_wallet_number).json()

        ethirium_url = "https://mainnet.infura.io/v3/8217d43a61134929ba3607ad88943e6a"
        ethbalance = pyetherbalance.PyEtherBalance(ethirium_url)
        eth_balance = ethbalance.get_eth_balance(self.__eth_wallet_number)
        print(eth_balance)
        data = {
            "BTC": btc_balance[self.__btc_wallet_number]['final_balance'],
            "ETH": eth_balance['balance']
        }
        return data
    
    def get_telegram_id(self):
        return self.__telegram_id
    
    def get_btc_wallet_number(self):
        return self.__btc_wallet_number
    
    def get_eth_wallet_number(self):
        return self.__eth_wallet_number

    def get_btc_public_key(self):
        return self.__btc_public
    
    def get_btc_private_key(self):
        return self.__btc_private
    
    def get_eth_public_key(self):
        return self.__eth_public
    
    def get_eth_private_key(self):
        return self.__eth_private


    def __str__(self):
        return f"Telegram id: {self.__telegram_id}, {self.__btc_wallet_number}"