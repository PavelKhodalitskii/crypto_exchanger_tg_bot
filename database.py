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
                wallet_number VARCHAR(256)
            )
        ''')
        self.__cursor.execute('''
            CREATE TABLE IF NOT EXISTS operation_exchange (
                id INTEGER PRIMARY KEY,
                date_time DATETIME2,
                user_id INTEGER,
                FOREIGN KEY(user_id) REFERENCES users(id) 
            )
        ''')
        self.__cursor.execute('''
            CREATE TABLE IF NOT EXISTS operation_fillup (
                id INTEGER PRIMARY KEY,
                date_time DATETIME2,
                user_ids INTEGER,
                FOREIGN KEY(user_ids) REFERENCES users(id) 
            )
        ''')
        self.__cursor.execute('''
            CREATE TABLE IF NOT EXISTS operation_withdraws (
                id INTEGER PRIMARY KEY,
                date_time DATETIME2,
                user_ids INTEGER,
                FOREIGN KEY(user_ids) REFERENCES users(id) 
            )
        ''')
        self.__connection.commit()

    def save_user(self, telegram_id, wallet_number):
        self.__cursor.execute(f'''
            INSERT INTO users (telegram_id, wallet_number)
            VALUES ('{telegram_id}', '{wallet_number}')
        ''')
        self.__connection.commit()
    
    def get_user(self, telegram_id):
        self.__cursor.execute(f'''
            SELECT users.wallet_number
            FROM users
            WHERE telegram_id = {telegram_id}
        ''')
        return self.__cursor.fetchone()

    def save_operation(self, opeartion):
        pass
    
    def get_opeation(self, telegram_operation):
        pass