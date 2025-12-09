import re
import redis
import json

r = redis.Redis(host="localhost", port=6379, db=0)

from upstash_redis import Redis

UPSTASH_REDIS_REST_URL = "https://communal-elf-7735.upstash.io"
UPSTASH_REDIS_REST_TOKEN = "AR43AAImcDI3N2Q3Njk0ZDdkMmY0Yjg3OTk3MzYwODA3NzFmY2JlNHAyNzczNQ"

r = Redis(url=UPSTASH_REDIS_REST_URL, token=UPSTASH_REDIS_REST_TOKEN)


def tokenize(text):
    text = text.lower()
    tokens = re.findall(r'\b\w+\b', text)
    return tokens

def index_to_redis(documents):
    pipe = r.pipeline()

    for doc in documents:
        doc_id = doc["id"]
        text = doc["message"] + " " + doc["user_name"]
        tokens = tokenize(text)

        # 1) Store original document
        pipe.set(f"message:{doc_id}", json.dumps(doc))

        # 2) Store index entries
        for token in tokens:
            pipe.sadd(f"token:{token}", doc_id)

    pipe.execute()
