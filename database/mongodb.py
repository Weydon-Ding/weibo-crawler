import copy
import logging
import sys

logger = logging.getLogger("weibo")

try:
    import pymongo
except ImportError:
    logger.warning("系统中可能没有安装pymongo库，请先运行 pip install pymongo ，再运行程序")
    sys.exit()


class MongoDB:
    def __init__(self, mongodb_URI, write_mode):
        self.mongodb_URI = mongodb_URI
        self.write_mode = write_mode

    def insert(self, collection, info_list):
        """将爬取的信息写入MongoDB数据库"""
        try:
            from pymongo import MongoClient

            client = MongoClient(self.mongodb_URI)
            db = client["weibo"]
            collection = db[collection]
            if len(self.write_mode) > 1:
                new_info_list = copy.deepcopy(info_list)
            else:
                new_info_list = info_list
            for info in new_info_list:
                if not collection.find_one({"id": info["id"]}):
                    collection.insert_one(info)
                else:
                    collection.update_one({"id": info["id"]}, {"$set": info})
        except pymongo.errors.ServerSelectionTimeoutError:
            logger.warning("系统中可能没有安装或启动MongoDB数据库，请先根据系统环境安装或启动MongoDB，再运行程序")
            sys.exit()
