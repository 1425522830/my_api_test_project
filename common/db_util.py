# 数据库客户端，封装数据库连接、SQL执行、查询及关闭操作，提供数据验证与清理能力。

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
                charset=DATABASE.get('charset', 'utf8mb4'),
                autocommit=True   # 默认自动提交，便于非事务操作
            )
        else:
            raise ValueError("Unsupported database type, only 'mysql' is configured now.")
        self.cursor = self.conn.cursor()

    def execute(self, sql, params=None):
        """执行写操作（INSERT/UPDATE/DELETE），事务外自动提交，事务内由 commit/rollback 控制"""
        if params:
            self.cursor.execute(sql, params)
        else:
            self.cursor.execute(sql)
        # 如果当前处于自动提交模式（未开启事务），则立即提交
        if self.conn.autocommit:
            self.conn.commit()
        return self.cursor

    def execute_query(self, sql, params=None):
        """执行查询（SELECT），不提交事务"""
        if params:
            self.cursor.execute(sql, params)
        else:
            self.cursor.execute(sql)
        return self.cursor

    def fetch_one(self, sql, params=None):
        self.execute_query(sql, params)
        return self.cursor.fetchone()

    def fetch_all(self, sql, params=None):
        self.execute_query(sql, params)
        return self.cursor.fetchall()

    def begin(self):
        """开始事务，关闭自动提交"""
        self.conn.autocommit = False
        self.conn.begin()

    def commit(self):
        """提交事务，恢复自动提交"""
        self.conn.commit()
        self.conn.autocommit = True

    def rollback(self):
        """回滚事务，恢复自动提交"""
        self.conn.rollback()
        self.conn.autocommit = True

    def close(self):
        self.cursor.close()
        self.conn.close()