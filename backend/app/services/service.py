# backend/app/services/document_service.py

from unstructured.partition.auto import partition
from fastapi import UploadFile
import tempfile

def process_uploaded_file(file: UploadFile):
    # Save file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=file.filename) as tmp:
        tmp.write(file.file.read())
        tmp_path = tmp.name

    # Use unstructured.io on that file
    elements = partition(filename=tmp_path)

    # Extract raw text from elements
    full_text = "\n".join([str(el) for el in elements])
    return full_text
