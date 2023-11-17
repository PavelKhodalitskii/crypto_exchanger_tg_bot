from bit import PrivateKey
import json

class Operation:
    def __init__(self, user_id):
        self.user_id = user_id
    
    def execute():
        raise NotImplementedError("Необходимо переопределить метод")
    
class Withdraw(Operation):
    __valid_types = (
        "BTC",
        "RVN"
    )

    def __init__(self, user_id, private_key, type, amount):
        self.__user_id = user_id
        self.__private_key = private_key
        self.__type = type if self.__validate_type(type) else "-1"
        self.__amount = amount

    def __validate_type(self, type):
        if type in self.__valid_types:
            return True
        return False

    def get_currency_type(self):
        return self.__type

    def get_amount(self):
        return self.__amount

    def execute(self):
        # my_key = PrivateKey(wif=str(self.__private_key))
        # wallet = ""
        with open("../wallets.json", 'r') as wallets_json:
            wallets = json.load(wallets_json)
            wallet = wallets[self.__type]

        print(wallet)
        # print(my_key)
        # fee=2000
        # tx_hash = my_key.create_transaction([(wallet, self.__amount, 'BTC')],fee=fee,absolute_fee=True)