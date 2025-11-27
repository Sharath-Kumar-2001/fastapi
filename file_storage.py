import hashlib
import os
import uuid
from supabase import create_client, Client
from config import settings
UPLOAD_DIR = "uploads"

def encrypt_filename(original_filename: str) -> str:
    """
    Encrypt filename using SHA256 hash with unique salt.
    Returns encrypted filename with original extension.
    """
    # Generate unique salt
    salt = uuid.uuid4().hex
    
    # Combine original filename with salt
    to_hash = f"{original_filename}_{salt}".encode('utf-8')
    
    # Create hash
    hashed = hashlib.sha256(to_hash).hexdigest()
    
    # Preserve original extension
    file_extension = original_filename.split(".")[-1] if "." in original_filename else ""
    encrypted_name = f"{hashed}.{file_extension}" if file_extension else hashed
    
    return encrypted_name

def upload_file(bucket_name, path,contents, content_type):
    # supabase: Client = create_client(str(settings.SUPABASE_URL), settings.SUPABASE_KEY)
    # if settings.PRODUCTION:
    #     response = supabase.storage.from_(bucket_name) \
    #                 .upload(path, contents, {"content-type": content_type, "upsert": "true"})
    #     return f"{str(settings.SUPABASE_URL)}/storage/v1/object/public/{response.full_path}"
    # else:
    os.makedirs(UPLOAD_DIR, exist_ok = True)
    file_path = os.path.join(UPLOAD_DIR, bucket_name, path)
    with open(file_path, 'wb') as f:
        f.write(contents)
    return f"/{UPLOAD_DIR}/{path}"