import requests
from app.indexing import index_messages

URL = "https://november7-730026606190.europe-west1.run.app/messages"

def load_and_index():
    print("Fetching messages...")
    messages = requests.get(URL).json()
    print(f"Fetched {len(messages)} messages.")

    print("Indexing...")
    index_messages(messages)

    print("Done! Messages indexed into Redis.")

if __name__ == "__main__":
    load_and_index()
