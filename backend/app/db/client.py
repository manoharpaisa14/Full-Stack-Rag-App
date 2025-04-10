from redis_om import get_redis_connection

# Use Redis URL from your .env or docker-compose
redis = get_redis_connection(
    host="localhost",
    port=6379,
    decode_responses=True
)
