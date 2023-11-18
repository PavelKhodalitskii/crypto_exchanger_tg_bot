from bit import PrivateKey
import json
import base58
from database import DataAccessObject
import requests
from user import User

import hashlib
import base58


class Operation:
    def __init__(self, user_id):
        self.user_id = user_id
    
    def save(self):
        raise NotImplementedError("Необходимо переопределить метод")

    def execute():
        raise NotImplementedError("Необходимо переопределить метод")

class Exchange(Operation):
    __valid_types = (
        "BTC->ETH",
        "ETH->ETH"
    )

    def __init__(self, user_id, type, amount):
        self.__database = DataAccessObject()
        self.__user_id = user_id
        self.__type = type if self.__validate_type(type) else "-1"
        self.__amount = amount
        self.__user = User(user_id)
        self.__btc_private_key = self.__user.get_btc_private_key()
        self.__eth_private_key = self.__user.get_eth_private_key()

    def __validate_type(self, type):
        if type in self.__valid_types:
            return True
        return False

    @staticmethod
    def generate_private_key_wif_compressed(private_key):
        try:
            bytes.fromhex(private_key)
        except ValueError:
            raise ValueError("Invalid private key. It should be a valid hexadecimal string.")
        private_key_with_prefix = '80' + private_key
        private_key_with_suffix = private_key_with_prefix + '01'

        hash1 = hashlib.sha256(bytes.fromhex(private_key_with_suffix)).digest()
        hash2 = hashlib.sha256(hash1).digest()
        
        private_key_with_checksum = private_key_with_suffix + checksum.hex()
        
        checksum = hash2[:4]

        private_key_wif_compressed = base58.b58encode(bytes.fromhesx(private_key_with_checksum)).decode()

        return private_key_wif_compressed

    def __save(self):
        self.__database.save_operation(self.__user_id, self.to_b_tx_hash, self.to_c_tx_hash)
        

    def execute(self):
        b_btc_wallet = ""
        b_eth_wallet = ""
        b_btc_public_key = ""
        b_eth_public_key = ""
        b_btc_private_key = ""
        b_eth_private_key = ""
        with open("../wallets.json", 'r') as wallets_json:
            wallets = json.load(wallets_json)
            btc_wallet = wallets["BTC"]
            eth_wallet = wallets["ETH"]
            b_btc_public_key = wallets["BTC_public_key"]
            b_eth_public_key = wallets["ETH_public_key"]
            b_btc_private_key = wallets["BTC_private_key"]
            b_eth_private_key = wallets["ETH_private_key"]


        user_key = PrivateKey(wif=self.generate_private_key_wif_compressed(self.__btc_private_key))
        buiseness_key = PrivateKey(wif=self.generate_private_key_wif_compressed(b_eth_private_key))
        
        fee = 2000
        btc_eth_pare = requests.get("https://tradeogre.com/api/v1/markets")[0]["BTC-ETH"]['price']
        eth_btc_pare = requests.get("https://tradeogre.com/api/v1/markets")[0]["ETH-BTC"]['price']

        if self.__type == "BTC->ETH":
            eth_amount = eth_btc_pare * self.__amount
            self.to_b_tx_hash = user_key.create_transaction([(btc_wallet, self.__amount, 'BTC')], fee=fee, absolute_fee=True)
            self.to_c_tx_hash = buiseness_key.create_transaction([(eth_wallet, eth_amount, 'ETH')], fee=fee, absolute_fee=True)
        elif self.__type == "ETH->BTC":
            btc_amount = btc_eth_pare * self.__amount
            self.to_b_tx_hash = user_key.create_transaction([(eth_wallet, self.__amount, 'ETH')], fee=fee, absolute_fee=True)
            self.to_c_tx_hash = buiseness_key.create_transaction([(btc_wallet, btc_amount, 'BTC')], fee=fee, absolute_fee=True)
        else:
            self.to_b_tx_hash = "-1"
            self.to_c_tx_hash = "-1"

        self.__save()