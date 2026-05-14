# config.py - Centralized Configuration settings for API tests
import os

BASE_URL = os.getenv("BASE_URL", "https://jsonplaceholder.typicode.com")

HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json"
}

API_TIMEOUT = 10000  # milliseconds
