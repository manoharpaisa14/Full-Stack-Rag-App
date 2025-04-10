from unstructured.partition.auto import partition
from io import BytesIO

def parse_document(content: bytes, filename: str):
    elements = partition(file=BytesIO(content))  # ✅ fixed: removed filename param
    text = "\n".join([el.text for el in elements if hasattr(el, "text")])
    metadata = {
        "filename": filename,
        "num_elements": len(elements),
    }
    return text, metadata
