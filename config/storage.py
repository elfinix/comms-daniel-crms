import os
import mimetypes
import urllib.request
import urllib.error
import json
from django.core.files.storage import Storage
from django.core.files.base import ContentFile
from django.utils.deconstruct import deconstructible


from django.conf import settings
from dotenv import load_dotenv

@deconstructible
class SupabaseMediaStorage(Storage):
    """
    Custom Django Storage backend that persists media files directly
    to Supabase Storage (public 'media' bucket).
    """

    def __init__(self, **kwargs):
        load_dotenv()
        self.supabase_id = getattr(settings, "SUPABASE_ID", os.environ.get("SUPABASE_ID", ""))
        self.supabase_key = getattr(settings, "SUPABASE_KEY", os.environ.get("SUPABASE_KEY", ""))
        self.bucket = "media"
        self.base_url = f"https://{self.supabase_id}.supabase.co/storage/v1"
        self.public_url = f"{self.base_url}/object/public/{self.bucket}"

    def _headers(self, content_type=None, upsert=True):
        headers = {
            "apikey": self.supabase_key,
            "Authorization": f"Bearer {self.supabase_key}",
        }
        if content_type:
            headers["Content-Type"] = content_type
        if upsert:
            headers["x-upsert"] = "true"
        return headers

    def _save(self, name, content):
        clean_name = str(name).lstrip("/")
        
        content.seek(0)
        file_bytes = content.read()
        
        content_type, _ = mimetypes.guess_type(clean_name)
        if not content_type:
            content_type = "application/octet-stream"

        upload_url = f"{self.base_url}/object/{self.bucket}/{clean_name}"
        req = urllib.request.Request(
            upload_url,
            data=file_bytes,
            headers=self._headers(content_type=content_type, upsert=True),
            method="POST",
        )

        try:
            with urllib.request.urlopen(req):
                pass
        except urllib.error.HTTPError as e:
            if e.code in (400, 409):
                put_req = urllib.request.Request(
                    upload_url,
                    data=file_bytes,
                    headers=self._headers(content_type=content_type, upsert=True),
                    method="PUT",
                )
                with urllib.request.urlopen(put_req):
                    pass
            else:
                raise e

        return clean_name

    def _open(self, name, mode="rb"):
        clean_name = str(name).lstrip("/")
        file_url = f"{self.public_url}/{clean_name}"
        req = urllib.request.Request(file_url, headers=self._headers())
        with urllib.request.urlopen(req) as resp:
            data = resp.read()
        return ContentFile(data, name=clean_name)

    def exists(self, name):
        clean_name = str(name).lstrip("/")
        check_url = f"{self.public_url}/{clean_name}"
        req = urllib.request.Request(check_url, method="HEAD")
        try:
            with urllib.request.urlopen(req) as resp:
                return resp.status == 200
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return False
            return False
        except Exception:
            return False

    def url(self, name):
        if not name:
            return ""
        name_str = str(name)
        if name_str.startswith("http://") or name_str.startswith("https://"):
            return name_str
        clean_name = name_str.lstrip("/")
        return f"{self.public_url}/{clean_name}"

    def delete(self, name):
        clean_name = str(name).lstrip("/")
        delete_url = f"{self.base_url}/object/{self.bucket}"
        headers = self._headers(content_type="application/json")
        payload = json.dumps({"prefixes": [clean_name]}).encode("utf-8")
        req = urllib.request.Request(delete_url, data=payload, headers=headers, method="DELETE")
        try:
            with urllib.request.urlopen(req):
                pass
        except Exception:
            pass

    def size(self, name):
        clean_name = str(name).lstrip("/")
        check_url = f"{self.public_url}/{clean_name}"
        req = urllib.request.Request(check_url, method="HEAD")
        try:
            with urllib.request.urlopen(req) as resp:
                length = resp.headers.get("Content-Length")
                return int(length) if length else 0
        except Exception:
            return 0
