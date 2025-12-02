import re
import json
from . import r

def index_messages(messages):
    pipe = r.pipeline(transaction=False)

    for msg in messages:
        msg_id = msg["id"]

        # Store the full message
        pipe.set(f"message:{msg_id}", json.dumps(msg))

        # Create keywords
        words = re.findall(r"\w+", msg["message"].lower())
        unique_words = set(words)

        # Build inverted index
        for w in unique_words:
            pipe.sadd(f"index:{w}", msg_id)

    pipe.execute()
