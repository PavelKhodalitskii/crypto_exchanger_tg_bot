import bitcoin
from database import DataAccessObject
import requests

class User:
    def __init__(self, telegram_id):
        self.database = DataAccessObject()
        self.__telegram_id = telegram_id
        self.__is_exists = bool(self.database.get_user_data(self.__telegram_id))
        if not self.__is_exists:
            self.__wallet_number = self.__create_wallet()["address"]
            self.__private = self.__create_wallet()["private"]
            self.__public = self.__create_wallet()["public"]
            self.database.save_user(self.__telegram_id, self.__wallet_number, self.__private, self.__public)
            user_data = self.database.get_user_data(telegram_id)
            print(f'''Creating user with:
                Telegram id: {self.__telegram_id}
                Wallet number: {user_data["wallet_number"]}
                Private key: {user_data["private_key"]}
                Public key: {user_data["public_key"]}
            ''')
        else:
            user_data = self.database.get_user_data(telegram_id)
            self.__wallet_number = user_data["wallet_number"]
            self.__private = user_data["private_key"]
            self.__public = user_data["public_key"]
            print(f'''Getting user with:
                Telegram id: {self.__telegram_id}
                Wallet number: {user_data["wallet_number"]}
                Private key: {user_data["private_key"]}
                Public key: {user_data["public_key"]}
            ''')

    def __create_wallet(self):
        key = bitcoin.random_key()
        private = bitcoin.sha256(key) 
        public = bitcoin.privtopub(private)
        address = bitcoin.pubtoaddr(public)

        wallet = {"private": private,
				  "public": public,
				  "address": address}
        
        return wallet
    
    def get_balance(self):
        res = requests.get("https://blockchain.info/balance?active=%s" % self.__wallet_number).json()
        print(res)

    def get_telegram_id(self):
        return self.__telegram_id
    
    def get_wallet_number(self):
        return self.__wallet_number
    
    def get_public_key(self):
        return self.__public
    
    def get_private_key(self):
        return self.__private

    def __str__(self):
        return f"Telegram id: {self.__telegram_id}, {self.__wallet_number}"