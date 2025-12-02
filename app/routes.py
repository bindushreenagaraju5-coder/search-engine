from flask import Blueprint, request, jsonify
from .search import redis_search

main = Blueprint("main", __name__)

@main.route("/search")
def search():
    query = request.args.get("q", "")
    page = int(request.args.get("page", 1))
    size = int(request.args.get("size", 10))

    results = redis_search(query)

    total = len(results)
    start = (page - 1) * size
    end = start + size

    return jsonify({
        "query": query,
        "total": total,
        "page": page,
        "page_size": size,
        "results": results[start:end]
    })
