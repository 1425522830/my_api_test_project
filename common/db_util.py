#  数据库客户端，封装数据库连接、SQL执行、查询及关闭操作，提供数据验证与清理能力。
import pymysql
from config.settings import DATABASE

class DBClient:
    def __init__(self):
        if DATABASE['type'] == 'mysql':
            self.conn = pymysql.connect(
                host=DATABASE['host'],
                port=DATABASE['port'],
                user=DATABASE['user'],
                password=DATABASE['password'],
                database=DATABASE['database'],
                charset=DATABASE.get('charset', 'utf8mb4')
            )
        else:
            raise ValueError("Unsupported database type, only 'mysql' is configured now.")
        self.cursor = self.conn.cursor()

    def execute(self, sql, params=None):
        if params:
            self.cursor.execute(sql, params)
        else:
            self.cursor.execute(sql)
        self.conn.commit()
        return self.cursor

    def fetch_one(self, sql, params=None):
        self.execute(sql, params)
        return self.cursor.fetchone()

    def fetch_all(self, sql, params=None):
        self.execute(sql, params)
        return self.cursor.fetchall()

    def close(self):
        self.cursor.close()
        self.conn.close()