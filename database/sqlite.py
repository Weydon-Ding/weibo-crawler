import os
import sqlite3


class Sqlite:
    def __init__(self):
        pass

    def get_path(self):
        return "./weibo/weibodata.db"

    def get_connection(self):
        path = self.get_path()
        create = False
        if not os.path.exists(path):
            create = True

        con = sqlite3.connect(path)

        if create == True:
            self.create_table(connection=con)

        return con

    def create_table(self, connection: sqlite3.Connection):
        sql = self.create()
        cur = connection.cursor()
        cur.executescript(sql)
        connection.commit()

    def create(self):
        create_sql = """
                CREATE TABLE IF NOT EXISTS user (
                    id varchar(64) NOT NULL
                    ,nick_name varchar(64) NOT NULL
                    ,gender varchar(6)
                    ,follower_count integer
                    ,follow_count integer
                    ,birthday varchar(10)
                    ,location varchar(32)
                    ,edu varchar(32)
                    ,company varchar(32)
                    ,reg_date DATETIME
                    ,main_page_url text
                    ,avatar_url text
                    ,bio text
                    ,PRIMARY KEY (id)
                );

                CREATE TABLE IF NOT EXISTS weibo (
                    id varchar(20) NOT NULL
                    ,bid varchar(12) NOT NULL
                    ,user_id varchar(20)
                    ,screen_name varchar(30)
                    ,text varchar(2000)
                    ,article_url varchar(100)
                    ,topics varchar(200)
                    ,at_users varchar(1000)
                    ,pics varchar(3000)
                    ,video_url varchar(1000)
                    ,location varchar(100)
                    ,created_at DATETIME
                    ,source varchar(30)
                    ,attitudes_count INT
                    ,comments_count INT
                    ,reposts_count INT
                    ,retweet_id varchar(20)
                    ,PRIMARY KEY (id)
                );

                CREATE TABLE IF NOT EXISTS bins (
                    id integer PRIMARY KEY AUTOINCREMENT
                    ,ext varchar(10) NOT NULL /*file extension*/
                    ,data blob NOT NULL
                    ,weibo_id varchar(20)
                    ,comment_id varchar(20)
                    ,path text
                    ,url text
                );

                CREATE TABLE IF NOT EXISTS comments (
                    id varchar(20) NOT NULL
                    ,bid varchar(20) NOT NULL
                    ,weibo_id varchar(32) NOT NULL
                    ,root_id varchar(20)
                    ,user_id varchar(20) NOT NULL
                    ,created_at varchar(20)
                    ,user_screen_name varchar(64) NOT NULL
                    ,user_avatar_url text
                    ,text varchar(1000)
                    ,pic_url text
                    ,like_count integer
                    ,PRIMARY KEY (id)
                );

                CREATE TABLE IF NOT EXISTS reposts (
                    id varchar(20) NOT NULL
                    ,bid varchar(20) NOT NULL
                    ,weibo_id varchar(32) NOT NULL
                    ,user_id varchar(20) NOT NULL
                    ,created_at varchar(20)
                    ,user_screen_name varchar(64) NOT NULL
                    ,user_avatar_url text
                    ,text varchar(1000)
                    ,like_count integer
                    ,PRIMARY KEY (id)
                );
                """
        return create_sql

    def exist_file(self, url):
        if not os.path.exists(self.get_path()):
            return True
        con = self.get_connection()
        cur = con.cursor()

        query_sql = """SELECT url FROM bins WHERE path=? """
        count = cur.execute(query_sql, (url,)).fetchone()
        con.close()
        if count is None:
            return False

        return True

    def insert(self, con: sqlite3.Connection, data: dict, table: str):
        if not data:
            return
        cur = con.cursor()
        keys = ",".join(data.keys())
        values = ",".join(["?"] * len(data))
        sql = """INSERT OR REPLACE INTO {table}({keys}) VALUES({values})
                """.format(
            table=table, keys=keys, values=values
        )
        cur.execute(sql, list(data.values()))
        con.commit()