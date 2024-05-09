import logging
import sys

logger = logging.getLogger("weibo")

try:
    import pymysql
except ImportError:
    logger.warning("系统中可能没有安装pymysql库，请先运行 pip install pymysql ，再运行程序")
    sys.exit()


class MySQL:
    def __init__(self, mysql_config):
        self.mysql_config = mysql_config

    def create(self, connection: pymysql.Connection, sql):
        """创建MySQL数据库或表"""
        try:
            with connection.cursor() as cursor:
                cursor.execute(sql)
        finally:
            connection.close()


    def create_database(self, mysql_config, sql):
        """创建MySQL数据库"""
        try:
            if self.mysql_config:
                mysql_config = self.mysql_config
            connection = pymysql.connect(**mysql_config)
            self.create(connection, sql)
        except pymysql.OperationalError:
            logger.warning("系统中可能没有安装或正确配置MySQL数据库，请先根据系统环境安装或配置MySQL，再运行程序")
            sys.exit()


    def create_table(self, mysql_config, sql):
        """创建MySQL表"""
        if self.mysql_config:
            mysql_config = self.mysql_config
        mysql_config["db"] = "weibo"
        connection = pymysql.connect(**mysql_config)
        self.create(connection, sql)

    def insert(self, mysql_config, table, data_list):
        """
        向MySQL表插入或更新数据

        Parameters
        ----------
        mysql_config: map
            MySQL配置表
        table: str
            要插入的表名
        data_list: list
            要插入的数据列表

        Returns
        -------
        bool: SQL执行结果
        """

        if len(data_list) > 0:
            keys = ", ".join(data_list[0].keys())
            values = ", ".join(["%s"] * len(data_list[0]))
            if self.mysql_config:
                mysql_config = self.mysql_config
            mysql_config["db"] = "weibo"
            connection = pymysql.connect(**mysql_config)
            cursor = connection.cursor()
            sql = """INSERT INTO {table}({keys}) VALUES ({values}) ON
                        DUPLICATE KEY UPDATE""".format(
                table=table, keys=keys, values=values
            )
            update = ",".join(
                [" {key} = values({key})".format(key=key) for key in data_list[0]]
            )
            sql += update
            try:
                cursor.executemany(sql, [tuple(data.values()) for data in data_list])
                connection.commit()
            except Exception as e:
                connection.rollback()
                logger.exception(e)
            finally:
                connection.close()
