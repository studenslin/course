# -*- codeing = utf-8 -*-
# @Time : 2022/4/12 13:43
# @Author : linyaxuan
# @File : es.py
# @Software : PyCharm
"""
es 引擎相关
"""

from elasticsearch import Elasticsearch

es = Elasticsearch("http://47.94.58.100:9200/")


class ES(object):
    """
    es 对象
    """

    def __init__(self, index_name: str):
        self.es = es
        self.index_name = index_name

    def get_doc(self, uid):
        return self.es.get(index=self.index_name, id=uid)

    def insert_one(self, doc: dict):
        self.es.index(index=self.index_name, body=doc)

    def insert_array(self, docs: list):
        for doc in docs:
            self.es.index(index=self.index_name, body=doc)

    def search(self, query, count: int = 30):
        dsl = {
            "query": {
                "multi_match": {
                    "query": query,
                    "fields": ["title", "desc"]
                }
            },
            "highlight": {
                "fields": {
                    "title": {}
                }
            }
        }
        match_data = self.es.search(index=self.index_name, body=dsl, size=count)
        return match_data

    def __search(self, query: dict, count: int = 20):  # count: 返回的数据大小
        results = []
        params = {
            'size': count
        }
        match_data = self.es.search(index=self.index_name, body=query, params=params)
        for hit in match_data['hits']['hits']:
            results.append(hit['_source'])

    def create_index(self):
        if self.es.indices.exists(index=self.index_name) is True:
            self.es.indices.delete(index=self.index_name)
        self.es.indices.create(index=self.index_name, ignore=400)

    def delete_index(self):
        try:
            self.es.indices.delete(index=self.index_name)
        except:
            pass