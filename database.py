import sqlite3

class DataAccessObject:
    __instance = None

    def __init__(self):
        self.__instance = self
        self.__connection = sqlite3.connect('db.sqlite3')
        self.__cursor = self.__connection.cursor()
        self.__create_tables()
    
    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance
    
    def __del__(self):
        self.__connection.close()
        self.__instance = None

    def __create_tables(self):
        self.__cursor.execute("DROP TABLE IF EXISTS users")
        self.__cursor.execute("DROP TABLE IF EXISTS operation_exchange")
        self.__cursor.execute("DROP TABLE IF EXISTS operation_withdraws")
        self.__cursor.execute("DROP TABLE IF EXISTS operation_fillup")
        self.__cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                telegram_id VARCHAR(255),
                btc_wallet_number VARCHAR(255),
                btc_private_key VARCHAR(255),
                btc_public_key VARCHAR(255),
                btc_wif VARCHAR(255),
                eth_wallet_number VARCHAR(255),
                eth_private_key VARCHAR(255),
                eth_public_key VARCHAR(255)
            )
        ''')
        self.__cursor.execute('''
            CREATE TABLE IF NOT EXISTS operations (
                id INTEGER PRIMARY KEY,
                user_id INTEGER,
                b_tx_hash VARCHAR(255),
                c_tx_hash VARCHAR(255),
                FOREIGN KEY(user_id) REFERENCES users(id) 
            )
        ''')
        self.__connection.commit()

    def save_user(self, 
                  telegram_id, 
                  btc_wallet_number, btc_private_key, btc_public_key, btc_wif, 
                  eth_wallet_number, eth_private_key, eth_public_key):
        self.__cursor.execute(f'''
            INSERT INTO users ('telegram_id', 'btc_wallet_number', 'btc_private_key', 'btc_wif', 'btc_public_key', 'eth_wallet_number', 'eth_private_key', 'eth_public_key')
            VALUES ('{telegram_id}', 
            '{btc_wallet_number}', 
            '{btc_private_key}', 
            '{btc_public_key}',
            '{btc_wif}',
            '{eth_wallet_number}', 
            '{eth_private_key}',
            '{eth_public_key}'
            )
        ''')
        self.__connection.commit()
    
    def get_user_data(self, telegram_id):
        self.__cursor.execute(f'''
            SELECT users.btc_wallet_number, users.btc_private_key, users.btc_public_key, users.btc_wif, users.eth_wallet_number, users.eth_private_key, users.eth_public_key 
            FROM users
            WHERE telegram_id = {telegram_id}
        ''')
        data_raw = self.__cursor.fetchone()
        data = {
            "btc_wallet_number": "",
            "btc_private_key": "",
            "btc_public_key": "",
            "btc_wif": "",
            "eth_wallet_number": "",
            "eth_private_key": "",
            "eth_public_key": ""
        }
        if data_raw:
            data["btc_wallet_number"] = data_raw[0]
            data["btc_private_key"] = data_raw[1]
            data["btc_public_key"] = data_raw[2]
            data["btc_wif"] = data_raw[3]
            data["eth_wallet_number"] = data_raw[4]
            data["eth_private_key"] = data_raw[5]
            data["eth_public_key"] = data_raw[6]
            return data
        else:
            return None
    
    def save_operation(self, user_id, b_tx_hash, c_tx_hash):
        self.__cursor.execute(f'''
            INSERT INTO opearions ('user_id', 'b_tx_hash', 'c_tx_hash')
            VALUES ('{user_id}',
            '{b_tx_hash}',
            '{c_tx_hash}'
            )
        ''')
        self.__connection.commit()

    def get_opeation(self, telegram_operation):
        pass