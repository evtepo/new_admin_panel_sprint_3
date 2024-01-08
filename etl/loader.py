from contextlib import contextmanager

from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from etl_backoff import backoff
from settings import Settings, elastic_dsn


@contextmanager
def es_connect(url: str):
    es = Elasticsearch(url)
    try:
        yield es
    finally:
        es.close()


@backoff(exceptions=Settings.elastic_exceptions)
def load_data(data, index):
    """Функция для загрузки данных в Elasticsearch"""
    with es_connect(elastic_dsn) as es_conn:
        data = [{"_index": index, "_id": item.get("id"), "_source": item} for item in data]
        bulk(client=es_conn, actions=data)
