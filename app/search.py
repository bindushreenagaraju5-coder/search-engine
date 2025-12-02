import re
import json
from . import r

def redis_search(query):
    words = re.findall(r"\w+", query.lower())
    if not words:
        return []

    keys = [f"index:{w}" for w in words if r.exists(f"index:{w}")]

    if not keys:
        return []

    matched_ids = r.sinter(keys)

    pipe = r.pipeline(transaction=False)
    for mid in matched_ids:
        pipe.get(f"message:{mid}")

    raw_msgs = pipe.execute()
    results = [json.loads(msg) for msg in raw_msgs if msg]

    return results
