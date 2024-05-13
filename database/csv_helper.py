import codecs
import csv
import os
import sys


def csv_helper(headers, result_data, file_path):
    """将指定信息写入csv文件"""
    if not os.path.isfile(file_path):
        is_first_write = 1
    else:
        is_first_write = 0
    if sys.version < "3":  # python2.x
        with open(file_path, "ab") as f:
            f.write(codecs.BOM_UTF8)
            writer = csv.writer(f)
            if is_first_write:
                writer.writerows([headers])
            writer.writerows(result_data)
    else:  # python3.x
        with open(file_path, "a", encoding="utf-8-sig", newline="") as f:
            writer = csv.writer(f)
            if is_first_write:
                writer.writerows([headers])
            writer.writerows(result_data)
