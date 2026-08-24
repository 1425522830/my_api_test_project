"""
MySQL数据库操作封装类
    1. 统一管理MySQL连接、游标创建与关闭
    2. 封装增删改执行、单条/多条查询方法
    3. 支持事务操作：开启事务、提交、回滚，用于自动清理测试脏数据
    4. 适配settings全局数据库配置，统一读取账号地址
"""

import pymysql
from config.settings import DATABASE

class DBClient:
    def __init__(self):                         # 初始化数据库连接，仅支持mysql类型
        if DATABASE['type'] == 'mysql':
            self.conn = pymysql.connect(
                host=DATABASE['host'],
                port=DATABASE['port'],
                user=DATABASE['user'],
                password=DATABASE['password'],
                database=DATABASE['database'],
                charset=DATABASE.get('charset', 'utf8mb4'),
                autocommit=True                 # 默认自动提交，非事务场景直接生效
            )
        else:
            raise ValueError("当前仅支持mysql数据库配置")
        self.cursor = self.conn.cursor()        # 创建游标对象，用于执行SQL语句

    def execute(self, sql, params=None):        # 执行增删改SQL
        try:
            if params:
                self.cursor.execute(sql, params)
            else:
                self.cursor.execute(sql)
            if self.conn.autocommit:            # 自动提交模式下执行完立即提交数据
                self.conn.commit()
            return self.cursor
        except Exception as e:
            if not self.conn.autocommit:        # 异常强制回滚并恢复自动提交，防止事务残留
                self.rollback()
            raise e


    def execute_query(self, sql, params=None):  # 执行查询SQL，不执行提交操作
        if params:
            self.cursor.execute(sql, params)
        else:
            self.cursor.execute(sql)
        return self.cursor

    def fetch_one(self, sql, params=None):      # 查询单条数据，返回元组
        self.execute_query(sql, params)
        return self.cursor.fetchone()

    def fetch_all(self, sql, params=None):      # 查询全部多条数据，返回元组列表
        self.execute_query(sql, params)
        return self.cursor.fetchall()

    def begin(self):                            # 开启事务：关闭自动提交，所有操作暂存，等待commit/rollback
        self.conn.autocommit = False
        self.conn.begin()

    def commit(self):                           # 提交事务，数据永久存入数据库，执行完成恢复自动提交
        self.conn.commit()
        self.conn.autocommit = True

    def rollback(self):                         # 回滚事务，撤销本次事务所有操作，执行完成恢复自动提交
        self.conn.rollback()
        self.conn.autocommit = True

    def close(self):                                # 关闭游标、数据库连接，释放资源
        self.cursor.close()
        self.conn.close()