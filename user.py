

class User:
    def __init__(self, telegram_id):
        self.__telegram_id = telegram_id
        self.__wallet_number = "47593749645986730485763946538"

    def get_telegram_id(self):
        return self.__telegram_id
    
    def get_wallet_number(self):
        return self.__wallet_number
