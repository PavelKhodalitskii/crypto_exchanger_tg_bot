import sqlite3
from user import User

class DataAccessObject:
    __instance = None

    def __init__(self):
        self.__instance = sqlite3.connect('db.sqlite3')
        self.__cursor = self.__instance.cursor()
        self.__create_tables()
    
    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance
    
    def __del__(self):
        self.__instance.close()
        self.__instance = None

    def __create_tables(self):
        self.__cursor.execute("DROP TABLE IF EXISTS users")
        self.__cursor.execute("DROP TABLE IF EXISTS operations")
        self.__cursor.execute('''
            CREATE TABLE users (
                id INTEGER PRIMARY KEY,
                telegram_id VARCHAR(255),
                wallet_number VARCHAR(256)
            )
        ''')
        self.__cursor.execute('''
            CREATE TABLE operations (
                id INTEGER PRIMARY KEY,
                date_time DATETIME2,
                user_ids INTEGER,
                FOREIGN KEY(user_ids) REFERENCES users(id) 
            )
        ''')
        self.__instance.commit()

    def save_user(self,user):
        self.__cursor.execute(f'''INSERT INTO users (telegram_id) VALUES ({user.get_telegram_id()})''')
        self.__cursor.execute(f'''INSERT INTO users (wallet_number) VALUES ({user.get_wallet_number()})''')
    
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


user = User("253453")
db = DataAccessObject()
db.save_user(user)
print(db.get_user(user.get_telegram_id()))
