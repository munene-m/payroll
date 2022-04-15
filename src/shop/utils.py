import uuid

def generate_uuid_code():
    code=str(uuid.uuid4())[:8].replace("-", "").lower()
    return code