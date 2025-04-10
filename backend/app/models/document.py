from redis_om import JsonModel
from app.db.client import redis
from typing import Optional

class Document(JsonModel):
    file_id: str
    filename: str
    text: Optional[str]
    num_elements: int

    class Meta:
        database = redis
