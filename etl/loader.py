from backoff import expo, on_exception

from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

from contextlib import contextmanager

from settings import ELASTIC_PORT, ELASTIC_HOST, elastic_exceptions


@contextmanager
def es_connect(url: str):
    es = Elasticsearch(url)
    try:
        yield es
    finally:
        es.close()


@on_exception(wait_gen=expo, exception=elastic_exceptions, max_value=10)
def load_data(data, index):
    """Функция для загрузки данных в Elasticsearch"""
    with es_connect(f"http://{ELASTIC_HOST}:{ELASTIC_PORT}/") as es_conn:
        data = [{"_index": index, "_id": item.get("id"), "_source": item} for item in data]
        bulk(client=es_conn, actions=data)
