import pymysql


class Database:
    def __init__(self, db_name: str, db_user: str, db_password: str, db_port: int, db_host: str) -> None:
        self.db_name = db_name
        self.db_user = db_user
        self.db_password = db_password
        self.db_host = db_host
        self.db_port = db_port

    @property
    def connect(self):
        return pymysql.connect(
            database=self.db_name,
            user=self.db_user,
            password=self.db_password,
            host=self.db_host,
            port=self.db_port,
            cursorclass=pymysql.cursors.DictCursor
        )

    def execute(self, sql: str, params: tuple = None, fetchall: bool = False, fetchone: bool = False, commit: bool = False) -> dict | tuple | None:
        connection = self.connect

        if not params:
            params = ()

        cursor = connection.cursor()

        cursor.execute(sql, params)

        data = None
        if fetchall:
            data = cursor.fetchall()

        elif fetchone:
            data = cursor.fetchone()

        else:
            data = None

        if commit:
            connection.commit()

        connection.close()
        return data
    
    def create_table(self):
        sql= """
            CREATE TABLE IF NOT EXISTS users (
            id INT PRIMARY KEY AUTO_INCREMENT,
            full_name VARCHAR(255),
            user_id VARCHAR(255),
            username VARCHAR(255))
        """

        self.execute(sql=sql)
    
    def register_user(self, full_name, user_id, username):
        sql= """
            INSERT INTO users (full_name, user_id, username) VALUES
            (%s, %s, %s)
        """

        params = (full_name, user_id, username)

        self.execute(sql=sql, params=params, commit=True)

    def all_users(self):
        sql = """
            SELECT * FROM users
        """

        return self.execute(sql=sql, fetchall=True)
    

db = Database(db_name="railway",
              db_user="root",
              db_password="pvpyZCvAnLcPmiidblCbnVnQLpDmwSXb",
              db_host="junction.proxy.rlwy.net",
              db_port=41961)