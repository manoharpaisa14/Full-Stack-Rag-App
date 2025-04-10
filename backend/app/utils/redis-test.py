from fastapi import APIRouter
from app.utils import redis_utils

router = APIRouter()

@router.get("/redis-test")
def test_redis():
    try:
        redis_utils.save_metadata("test-key", {"message": "Hello from FastAPI"})
        data = redis_utils.get_metadata("test-key")
        return {"status": "success", "data": data}
    except Exception as e:
        return {"status": "error", "message": str(e)}
