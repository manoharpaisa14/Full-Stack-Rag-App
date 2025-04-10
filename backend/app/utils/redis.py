import redis
import json
from fastapi import HTTPException

# Connect to Redis inside Docker Compose using service name
try:
    r = redis.Redis(host="redis", port=6379, decode_responses=True)
    r.ping()  # check connection on init
except redis.exceptions.ConnectionError:
    raise HTTPException(status_code=500, detail="Redis connection failed.")

def save_metadata(file_id: str, metadata: dict):
    try:
        r.set(file_id, json.dumps(metadata))
    except redis.exceptions.ConnectionError:
        raise HTTPException(status_code=500, detail="Failed to save metadata to Redis.")

def get_metadata(file_id: str) -> dict:
    try:
        data = r.get(file_id)
        if data:
            return json.loads(data)
        else:
            raise HTTPException(status_code=404, detail="Metadata not found.")
    except redis.exceptions.ConnectionError:
        raise HTTPException(status_code=500, detail="Failed to get metadata from Redis.")

def delete_metadata(file_id: str):
    try:
        result = r.delete(file_id)
        if result == 0:
            raise HTTPException(status_code=404, detail="Metadata not found.")
    except redis.exceptions.ConnectionError:
        raise HTTPException(status_code=500, detail="Failed to delete metadata from Redis.")
