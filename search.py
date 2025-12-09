import json
from flask import jsonify
import redis
import requests
from redis_index import index_to_redis, tokenize


DATA_URL = "https://november7-730026606190.europe-west1.run.app/messages"
data_source = []
#r = redis.Redis(host="localhost", port=6379, db=0)

from upstash_redis import Redis

UPSTASH_REDIS_REST_URL = "https://communal-elf-7735.upstash.io"
UPSTASH_REDIS_REST_TOKEN = "AR43AAImcDI3N2Q3Njk0ZDdkMmY0Yjg3OTk3MzYwODA3NzFmY2JlNHAyNzczNQ"

r = Redis(url=UPSTASH_REDIS_REST_URL, token=UPSTASH_REDIS_REST_TOKEN)


def load_data():
    resp = requests.get(DATA_URL)
    try:
        data_source = resp.json()
    except Exception:
        return {"error": "Invalid JSON from source API"}, 500
    if data_source and 'items' in data_source:
        index_to_redis(data_source['items'])
        
def search(query,page,limit):
    if not query:
        return jsonify({"error": "q is required"}), 400

    tokens = tokenize(query)

    redis_keys = [f"token:{t}" for t in tokens]
    
    if r.dbsize() == 0:
        print("Loading and indexing data into Redis…")
        load_data()
        
    matching_ids = r.sinter(redis_keys)

    matching_ids = sorted(list(matching_ids))
    start = (page - 1) * limit
    end = start + limit
    page_ids = matching_ids[start:end]

    results = []
    for doc_id in page_ids:
        raw = r.get(f"message:{doc_id.decode('utf-8')}")
        if raw:
            doc = json.loads(raw.decode('utf-8'))
            tmp = {
                'message': doc['message'],
                'user_name': doc['user_name']
            }
            results.append(tmp)

    if not results:
        return {"error": f"{query} item not found"}
    return jsonify(results)
