'''
@Author: ChenXiaolei
@Date: 2020-03-14 16:12:44
@LastEditTime: 2020-03-19 15:37:32
@LastEditors: ChenXiaolei
@Description: mysql helper
@FilePath: /seven_manage_api/libs./seven_framework/mysql.py
'''
# -*- coding: utf-8 -*-
import pymysql
from DBUtils.PooledDB import PooledDB
import traceback

class MySQLHelper:
    # 对MySQLdb常用函数进行封装的类

    error_code = ''  # MySQL错误号码
    _instance = None  # 本类的实例
    conn = None  # 数据库conn
    _cur = None

    def __init__(self, dbconfig):
        """
        @description: mysql 操作类初始化
        @param dbconfig: 连接字符串
        @last_editors: ChenXiaolei
        """
        self.POOL = PooledDB(
            creator=pymysql,  # 使用链接数据库的模块
            maxconnections=0,  # 连接池允许的最大连接数，0和None表示不限制连接数
            mincached=0,  # 初始化时，链接池中至少创建的空闲的链接，0表示不创建
            maxcached=0,  # 链接池中最多闲置的链接，0和None不限制
            maxshared=0,  # 链接池中最多共享的链接数量，0和None表示全部共享。PS: 无用，因为pymysql和MySQLdb等模块的 threadsafety都为1，所有值无论设置为多少，_maxcached永远为0，所以永远是所有链接都共享。
            blocking=True,  # 连接池中如果没有可用连接后，是否阻塞等待。True，等待；False，不等待然后报错
            maxusage=None,  # 一个链接最多被重复使用的次数，None表示无限制
            setsession=[],  # 开始会话前执行的命令列表。如：["set datestyle to ...", "set time zone ..."]
            ping=0,
            # ping MySQL服务端，检查是否服务可用。# 如：0 = None = never, 1 = default = whenever it is requested, 2 = when a cursor is created, 4 = when a query is executed, 7 = always
            host=dbconfig['host'],
            port=dbconfig['port'],
            user=dbconfig['user'],
            passwd=dbconfig['passwd'],
            db=dbconfig['db'],
            charset=dbconfig['charset'])

    def query(self, sql, params=None):
        """
        @description: 执行 SELECT 语句
        @param sql: 查询语句
        @param params: 参数值
        @return: 查询结果
        @last_editors: ChenXiaolei
        """
        # 执行 SELECT 语句
        self._execute(sql, params)
        record_list = self._cur.fetchall()
        self.close()
        return record_list

    def update(self, sql, params=None):
        """
        @description: 执行 UPDATE 操作
        @param sql: 查询语句
        @param params: 参数值
        @return: 执行结果
        @last_editors: ChenXiaolei
        """
        self._execute(sql, params)
        self._conn.commit()
        row_count = self._cur.rowcount
        self.close()
        return row_count

    def delete(self, sql, params=None):
        """
        @description: 执行 Delete 操作
        @param sql: 查询语句
        @param params: 参数值
        @return: 执行结果
        @last_editors: ChenXiaolei
        """
        self._execute(sql, params)
        self._conn.commit()
        row_count = self._cur.rowcount
        self.close()
        return row_count

    def insert(self, sql, params=None):
        """
        @description: 执行 INSERT 语句
        @param sql: 数据insert语句
        @return: 如主键为自增长int，则返回新生成的ID
        @last_editors: ChenXiaolei
        """
        # 执行 INSERT 语句。如主键为自增长int，则返回新生成的ID
        self._execute(sql, params)
        self._conn.commit()
        primary_id = self._cur._result.insert_id
        self.close()
        return primary_id

    def _execute(self, sql, params=None):
        self.connection()

        try:
            self._cur = self._conn.cursor(pymysql.cursors.DictCursor)
            if not params:
                self._cur.execute(sql)
            else:
                self._cur.execute(sql, params)
            return self._cur
        except Exception as e:
            print(traceback.print_exc())
            raise Exception("ERROR:" + str(e) + " SQL：" +
                            str(sql) + " 参数：" + str(params))

    def transaction_execute(self, sql_list):
        """
        @description: 事务提交
        @param sql_list: sql字符串数组
        @return: 执行成功返回 True   失败 False
        @last_editors: ChenXiaolei
        """
        try:
            for sql in sql_list:
                self._execute(sql)
        except Exception as e:
            self.rollback()  # 事务回滚
            # raise Exception("执行事务ERROR:" + str(e) + " SQL：" + str(sql))
            return False
        else:
            self.commit()  # 事务提交
        self.close()
        return True

    def fetch_all_rows(self, sql, params=None):
        """
        @description: 返回结果列表
        @param sql: 查询语句
        @param params: 参数值
        @return: 结果列表
        @last_editors: ChenXiaolei
        """
        self._execute(sql, params)
        record_list = self._cur.fetchall()
        self.close()
        return record_list

    def fetch_limit_rows(self, sql, params=None, current_page=1, list_rows=20):
        """
        @description: 分页查询结果
        @param sql: 查询语句
        @param params: 参数值
        @return: 分页查询结果
        @last_editors: ChenXiaolei
        """
        count = self.get_row_count(sql, params)
        pages = count / list_rows
        pages = pages + 1 if not count % list_rows == 0 else pages
        if (pages == 0):
            pages = 1
        if (current_page < 1):
            current_page = 1
        if (current_page > pages):
            current_page = pages
        start = (current_page - 1) * list_rows
        end = list_rows
        previous_page = current_page - 1 if current_page > 1 else 1
        next_page = current_page + \
            1 if current_page < int(pages) else int(pages)
        limit_sql = sql + " limit " + str(int(start)) + "," + str(int(end))
        result = {}
        result["list"] = self.fetch_all_rows(limit_sql, params)
        result["page"] = {
            "prev": previous_page,
            "next": next_page,
            "current": current_page,
            "pages": int(pages),
            "total": count,
        }

        return result

    def fetch_one_row(self, sql, params=None):
        """
        @description: 返回一行结果，然后游标指向下一行。到达最后一行以后，返回None
        @param sql: 查询语句
        @param params: 参数值
        @return: 返回一行结果
        @last_editors: ChenXiaolei
        """
        self._execute(sql, params)
        record = self._cur.fetchone()
        self.close()
        return record

    def get_row_count(self, sql, params=None):
        """
        @description: 获取结果行数
        @param sql: 查询语句
        @param params: 参数值
        @return: 返回查询行数
        @last_editors: ChenXiaolei
        """
        self._execute(sql, params)
        row_count = self._cur.rowcount
        self.close()
        return row_count

    def fetch_and_commit(self, sql, params=None):
        """
        @description: 执行并commit提交
        @param sql: 查询语句
        @param params: 参数值
        @return: 返回第一行结果
        @last_editors: ChenXiaolei
        """
        self._execute(sql, params)
        record = self._cur.fetchone()
        self._conn.commit()
        self.close()
        return record

    def commit(self):
        """
        @description: 数据库commit操作
        @last_editors: ChenXiaolei
        """
        # 数据库commit操作
        self._conn.commit()

    def rollback(self):
        """
        @description: 执行数据库回滚操作
        @last_editors: ChenXiaolei
        """
        # 数据库回滚操作'
        self._conn.rollback()

    def connection(self):
        self._conn = self.POOL.connection()

    def __del__(self):
        """
        @description: 执行释放资源（系统GC自动调用）
        @last_editors: ChenXiaolei
        """
        # 释放资源（系统GC自动调用）
        try:
            self._cur.close()
            self._conn.close()
        except:
            pass

    def close(self):
        """
        @description: 执行关闭数据库连接
        @last_editors: ChenXiaolei
        """
        # 关闭数据库连接
        self.__del__()
