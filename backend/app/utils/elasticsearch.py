from elasticsearch import Elasticsearch
from elasticsearch.exceptions import NotFoundError

es = Elasticsearch("http://elasticsearch:9200")
index_name = "documents"

def index_document(file_id, content):
    es.index(index=index_name, id=file_id, document={"text": content})


def search_documents(query):
    try:
        print(f"🔍 Searching ES with query: {query}")
        response = es.search(index=index_name, query={
            "match_phrase": {"text": query}
        })
        print("📦 Raw ES response:", response)
        hits = response["hits"]["hits"]
        return [hit["_source"]["text"] for hit in hits]
    except NotFoundError:
        print("❌ Index not found:", index_name)
        return []
    except Exception as e:
        print("❌ Elasticsearch search error:", e)
        return []

