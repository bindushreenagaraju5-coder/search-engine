
from flask import Flask, request
from search import search

app = Flask(__name__)

@app.route("/search")
def search_endpoint():
    query = request.args.get("q", "").strip().lower()
    page = int(request.args.get("page", 1))
    limit = int(request.args.get("limit", 5))
    return search(query,page,limit)
   

if __name__ == "__main__":
    app.run(debug=True, port=5001)
