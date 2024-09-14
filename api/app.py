from flask import Flask, jsonify, request
import requests
from threading import Thread
import time
import logging
from functools import wraps
from cachetools import TTLCache
from time import time as current_time
from pymongo import MongoClient
from bs4 import BeautifulSoup
import re

app = Flask(__name__)

# Setup API logging
logging.basicConfig(filename='api.log', level=logging.INFO, format='%(asctime)s %(message)s')

# Cache setup with TTL
cache = TTLCache(maxsize=100, ttl=300)

# Initialize MongoDB client
client = MongoClient('mongodb://localhost:27017/')
db = client['api_database']
users_collection = db['users']

# Scraping function for web pages (news articles, blogs, etc.)
def scrape_articles():
    url = "https://indianexpress.com/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # This example assumes articles are inside <article> tags.
    articles = soup.find_all('article')
    scraped_data = []
    
    for article in articles:
        title = article.find('h2').get_text()
        content = article.find('p').get_text()
        scraped_data.append({
            'title': title,
            'content': content
        })
    
    cache['scraped_articles'] = scraped_data
    logging.info(f"Scraped {len(scraped_data)} articles.")

# Background scraping task
def background_scraping():
    while True:
        scrape_articles()
        logging.info("Scraping news articles...")
        time.sleep(3600)  # Simulate scraping every hour

@app.before_first_request
def start_background_task():
    # Start background thread to scrape news articles
    thread = Thread(target=background_scraping, daemon=True)
    thread.start()

# Caching decorator for search results
def cache_search(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        cache_key = str(kwargs)
        if cache_key in cache:
            return cache[cache_key]
        result = f(*args, **kwargs)
        cache[cache_key] = result
        return result
    return wrapper

# Rate limiting decorator
def rate_limiter(max_requests):
    def decorator(f):
        def wrapper(*args, **kwargs):
            user_id = kwargs.get('user_id')
            user = users_collection.find_one({'user_id': user_id})
            if user and user['request_count'] >= max_requests:
                return jsonify({"error": "Too many requests"}), 429
            return f(*args, **kwargs)
        return wrapper
    return decorator

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "API is active"}), 200

@app.route('/search', methods=['POST'])
@cache_search
@rate_limiter(5)  # Limit to 5 requests per user
def search():
    start_time = current_time()  # Start inference time measurement
    
    data = request.get_json()
    
    # Extract required fields from JSON
    text = data.get('text')
    top_k = data.get('top_k', 10)
    threshold = data.get('threshold', 0.5)
    user_id = data.get('user_id')

    if not text or not user_id:
        return jsonify({"error": "text and user_id are required"}), 400

    # Generate fake search results
    results = [f"Result {i+1} for '{text}'" for i in range(top_k)]

    # Track user API call frequency
    user = users_collection.find_one({'user_id': user_id})
    if user:
        users_collection.update_one({'user_id': user_id}, {'$inc': {'request_count': 1}})
    else:
        users_collection.insert_one({'user_id': user_id, 'request_count': 1})

    # Calculate inference time
    inference_time = current_time() - start_time

    # Log the request details
    logging.info(f"User {user_id} made a request: {data}")
    logging.info(f"Inference time: {inference_time} seconds")

    response = {
        "user_id": user_id,
        "search_results": results,
        "inference_time": inference_time
    }

    return jsonify(response), 200




if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
