# Simple Search Engine API

This project implements a fast, lightweight search engine on top of the given data source:

**Messages API:**  
https://november7-730026606190.europe-west1.run.app/docs#/default/get_messages_messages__get

The service fetches the messages, indexes them into Redis (supports both Upstash Redis and local Redis), and exposes a public `/search` endpoint that returns matching results in under **100ms**.

The goal is to provide a simple full-text search over `message` and `user_name`.

---

## Features

- Full-text token-based search  
- Redis-backed inverted index  
- Pagination support  
- <100ms response time  
- Compatible with:
  - Upstash Redis (serverless)
  - Local Redis (redis-py)
- Deployed on Render  


---

## API Endpoints

### **GET `/search`**
Search for messages matching the query.

**Query Parameters:**

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `q` | string | yes | Search query |
| `page` | int | no | Page number (default: 1) |
| `limit` | int | no | Results per page (default: 10) |

**Example Request:**

/search?q=sophia&page=1&limit=5


**Example Response:**
```json
{
  "results": [
    {
      "message": "Sophia replied to your message",
      "user_name": "Sophia"
    }
  ]
}

**Tech Stack:**

Python 3.11

Flask

Redis / Upstash Redis

Gunicorn (production server)

Render (deployment)



##Bonus 1 — Design Notes (Alternative Approaches):##

When designing the search engine, I evaluated multiple approaches based on latency, scalability, memory usage, and implementation complexity. Below are the main alternatives considered.

1. Redis Set-Based Indexing (Chosen Approach)

Idea:
Store tokenized fields (first name, last name, message text) in Redis Sets.
Each token becomes a key, e.g.:

token:john → {id1, id4, id7}
token:doe  → {id1, id2}


At query time:

GET /search?q=john doe
→ SINTER(token:john, token:doe)


Pros

Very fast (<1 ms operations inside Redis)

Constant-time lookups

Easy to deploy and scale

Low operational overhead

Good for exact-match or prefix-match search

Cons

Not suitable for fuzzy search or ranking

Memory increases with number of tokens

Why I chose it:
Best balance between speed, simple implementation, and deployment constraints (Renderer RAM limits). Gives predictable <100ms performance.



2. Full-Text Search with PostgreSQL (TSVector)

Idea:
Store the dataset in PostgreSQL and run full-text queries:

SELECT * FROM messages WHERE to_tsvector(message) @@ plainto_tsquery('john');


Pros

Native ranking & stemming

Fuzzy search with extensions

Zero extra infrastructure if the app already uses SQL

Good for moderate dataset sizes (<5M)

Cons

Latency often 10–50ms per query depending on index size

Harder to tune for real-time search

Renderer’s free tier DB is slow

Conclusion:
A solid choice if the dataset grows large or needs ranking, but slower and heavier than Redis for this task.

3. ElasticSearch / OpenSearch

Idea:
Use a real search engine cluster with inverted indexes.

Pros

Best for large-scale text search

Powerful: fuzzy, synonyms, boosts, ranking

High-speed: queries often <10ms

Cons

Heavy operational cost

Not suitable for free-tier deployment

Requires cluster provisioning & monitoring

Conclusion:
Overkill for this assignment and impossible within renderer free-tier.

4. In-Memory Python Index (Trie + Token Map)

Idea:
Build everything in Python:

A token → IDs map (dict of sets)

A Trie for prefix search

Pros

Fast in-memory (<1ms lookup)

No external system required

Easy to implement

Cons

Data resets on deploy

Memory footprint grows

Doesn’t scale horizontally

No persistence

Conclusion:
Good for prototypes, but not stable for deployed/public endpoints.

5. Client-Side Filtering (Not Suitable)

Idea:
Load all messages into memory and filter in Python.

Pros

Simple

Zero infra

Cons

Very slow (O(n))

Breaks at scale

Latency >300ms for each query

Violates <100ms requirement
