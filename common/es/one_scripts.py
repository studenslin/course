# -*- codeing = utf-8 -*-
# @Time : 2022/4/12 13:43
# @Author : linyaxuan
# @File : one_scripts.py
# @Software : PyCharm

"""
将数据库数据导入es
"""
import pymysql
import traceback
from elasticsearch import Elasticsearch


def get_db_data():
    # 打开数据库连接（ip/数据库用户名/登录密码/数据库名）
    db = pymysql.connect(host="127.0.0.1:3306", user="root", password="linyaxuan666",
                         database="course", charset='utf8')
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()
    sql = "SELECT * FROM tb_course"
    # 使用 execute()  方法执行 SQL 查询
    cursor.execute(sql)
    # 获取所有记录列表
    results = cursor.fetchall()
    # 关闭数据库连接
    db.close()
    return results


def insert_data_to_es():
    es = Elasticsearch("http://47.94.58.100:9200/")
    es.indices.delete(index='course')
    try:
        i = -1
        for row in get_db_data():
            print(row)
            print(row[1], row[2])
            i += 1
            es.index(index='course', body={
                'id': i,
                'title': row[1],
                'desc': row[2],
            })
    except:
        error = traceback.format_exc()
        print("Error: unable to fecth data", error)


if __name__ == "__main__":
    insert_data_to_es()