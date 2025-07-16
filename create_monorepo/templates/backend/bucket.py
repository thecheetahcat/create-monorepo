BUCKET = """import json
import pickle
from typing import Any, Dict

from app.core.config import sb_client, settings


def upload_json(data: Dict[str, Any], bucket_path: str, upsert: bool = True) -> Any:
    storage = sb_client.storage.from_(settings.SUPABASE_BUCKET)
    json_data = json.dumps(data, indent=2).encode()

    return storage.upload(
        bucket_path,
        json_data,
        file_options={
            "contentType": "application/json",
            "upsert": str(upsert).lower(),
        },
    )


def upload_pkl(obj: Any, bucket_path: str, upsert: bool = True) -> Any:
    storage = sb_client.storage.from_(settings.SUPABASE_BUCKET)
    pkl_data = pickle.dumps(obj)

    return storage.upload(
        bucket_path,
        pkl_data,
        file_options={
            "contentType": "application/octet-stream",
            "upsert": str(upsert).lower(),
        },
    )


def delete(bucket_path: str) -> Any:
    storage = sb_client.storage.from_(settings.SUPABASE_BUCKET)
    storage.remove([bucket_path])


def get_signed_url(bucket_path: str, expires_in: int = 300) -> str:
    storage = sb_client.storage.from_(settings.SUPABASE_BUCKET)
    return storage.create_signed_url(bucket_path, expires_in)


def download_json(bucket_path: str) -> Dict[str, Any]:
    storage = sb_client.storage.from_(settings.SUPABASE_BUCKET)
    response = storage.download(bucket_path)
    return json.loads(response)


def download_pkl(bucket_path: str) -> Any:
    storage = sb_client.storage.from_(settings.SUPABASE_BUCKET)
    response = storage.download(bucket_path)
    return pickle.loads(response)
"""
