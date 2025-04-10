from fastapi import APIRouter, File, UploadFile, HTTPException, Depends
from app.utils.minio import upload_to_minio
from app.utils.parser import parse_document
from app.models.document import Document
from app.utils.redis import save_metadata, get_metadata, delete_metadata
from app.utils.elasticsearch import index_document
from app.utils.auth import get_current_user

router = APIRouter()

@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    user=Depends(get_current_user)  # 🔐 Protect this route
):
    try:
        file_content = await file.read()
        file_id = upload_to_minio(file.filename, file_content)
        text, metadata = parse_document(file_content, file.filename)
        index_document(file_id, text)

        doc = Document(
            file_id=file_id,
            filename=file.filename,
            text=text,
            num_elements=metadata["num_elements"]
        )
        doc.save()
        return {
            None
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
