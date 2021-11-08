import pymysql

MYSQL = {
        'host': '47.102.139.195',
        'port': 3306,
        'user': 'root',
        'passwd': 'root',
        'db': 'jobseeker_post',
        'charset': 'utf8',
    }

class SQLManager(object):


    # 初始化实例方法
    def __init__(self):
        """

        :rtype: object
        """
        self.conn = None
        self.cursor = None
        self.connect()

    # 连接数据库
    def connect(self):
        self.conn = pymysql.connect(
            host=MYSQL['host'],
            port=MYSQL['port'],
            user=MYSQL['user'],
            passwd=MYSQL['passwd'],
            db=MYSQL['db'],
            charset=MYSQL['charset']
        )
        self.cursor = self.conn.cursor(cursor=pymysql.cursors.DictCursor)

    # 查询一条数据
    def get_one(self, sql, args):
        self.cursor.execute(sql, args)
        return self.cursor.fetchone()

    # 查询所有数据
    def get_list(self, sql, args):
        self.cursor.execute(sql, args)
        return self.cursor.fetchall()

    # 修改数据
    def modify(self, sql, args):
        self.cursor.execute(sql, args)
        self.conn.commit()

    # 批量修改数据
    def multi_modify(self, sql, args):
        self.cursor.executemany(sql, args)
        self.conn.commit()

    # 关闭所有连接
    def close(self):
        self.cursor.close()
        self.conn.close()