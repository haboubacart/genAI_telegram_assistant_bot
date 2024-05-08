from elasticsearch import Elasticsearch
from dotenv import load_dotenv
import os

load_dotenv()
ELASTIC_HOST = os.getenv("ELASTIC_HOST")
es = Elasticsearch([ELASTIC_HOST])

def create_index(elastic_instance, index_name, mapping):
    try : 
        status = elastic_instance.indices.create(index=index_name, body={"mappings": mapping}) 
        return status
    except:
        return

def insert_new_doc(elastic_instance, index_name, doc_object):
    elastic_instance.index(index=index_name, body=doc_object)

def retrieve_matched_docs(elastic_instance, index_name, query):
    results = es.search(index=index_name, body={"query": {"match_all": {}}})
    return results

if __name__=='__main__':
    index_name = "mon_index3"
    mapping = {
        "properties": {
            "nom": {"type": "text"},
            "age": {"type": "integer"},
            "ville": {"type": "text"}
        }
    }

    doc1 = {
        "nom": "Jean",
        "age": 30,
        "ville": "Paris"
    }


    doc2 = {
        "nom": "Marie",
        "age": 25,
        "ville": "Lyon"
    }

    create_index(es, index_name, mapping)
    insert_new_doc(es, index_name, doc1)
    insert_new_doc(es, index_name, doc2)

    results = es.search(index=index_name, body={"query": {"match_all": {}}})
    for hit in results['hits']['hits']:
        print(hit['_source'])
