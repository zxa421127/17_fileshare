from app.config import settings
from app.database.models import FileObject
from app.main import app
from app.storage.minio import get_storage


class FakeStorage:
    def __init__(self):
        self.objects = {}

    def upload_bytes(self, object_name: str, content: bytes, content_type: str):
        self.objects[object_name] = {
            "content": content,
            "content_type": content_type,
        }

    def presigned_download_url(self, object_name: str, expires_seconds: int) -> str:
        if object_name not in self.objects:
            raise RuntimeError("missing object")
        return f"https://storage.test/{object_name}?expires={expires_seconds}"


def login_headers(client):
    response = client.post(
        "/api/auth/login",
        json={"username": "admin", "password": "admin123"},
    )
    assert response.status_code == 200
    return {"Authorization": f"Bearer {response.json()['access_token']}"}


def test_files_require_authentication(client):
    response = client.get("/api/files")
    assert response.status_code == 401


def test_upload_list_detail_and_download(client, active_user):
    storage = FakeStorage()
    app.dependency_overrides[get_storage] = lambda: storage
    headers = login_headers(client)

    upload = client.post(
        "/api/files/upload",
        headers=headers,
        files={"file": ("report.pdf", b"hello", "application/pdf")},
    )
    assert upload.status_code == 201
    uploaded = upload.json()
    assert uploaded["original_name"] == "report.pdf"
    assert uploaded["size"] == 5
    assert uploaded["owner_id"] == active_user.id

    listing = client.get("/api/files", headers=headers)
    assert listing.status_code == 200
    assert len(listing.json()) == 1
    assert listing.json()[0]["id"] == uploaded["id"]

    detail = client.get(f"/api/files/{uploaded['id']}", headers=headers)
    assert detail.status_code == 200
    assert detail.json()["original_name"] == "report.pdf"

    download = client.get(f"/api/files/{uploaded['id']}/download", headers=headers)
    assert download.status_code == 200
    assert download.json()["file_id"] == uploaded["id"]
    assert download.json()["expires_in"] == settings.download_url_expire_seconds
    assert download.json()["url"].startswith("https://storage.test/")


def test_user_cannot_access_another_users_file(client, active_user, db):
    storage = FakeStorage()
    app.dependency_overrides[get_storage] = lambda: storage
    headers = login_headers(client)

    record = FileObject(
        original_name="private.pdf",
        object_name="999/private-object",
        content_type="application/pdf",
        size=10,
        owner_id=999,
        status="active",
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    storage.objects[record.object_name] = {"content": b"x", "content_type": "application/pdf"}

    detail = client.get(f"/api/files/{record.id}", headers=headers)
    download = client.get(f"/api/files/{record.id}/download", headers=headers)

    assert detail.status_code == 404
    assert download.status_code == 404


def test_empty_file_is_rejected(client, active_user):
    storage = FakeStorage()
    app.dependency_overrides[get_storage] = lambda: storage
    headers = login_headers(client)

    response = client.post(
        "/api/files/upload",
        headers=headers,
        files={"file": ("empty.txt", b"", "text/plain")},
    )

    assert response.status_code == 400
    assert storage.objects == {}


def test_oversized_file_is_rejected(client, active_user, monkeypatch):
    storage = FakeStorage()
    app.dependency_overrides[get_storage] = lambda: storage
    headers = login_headers(client)
    monkeypatch.setattr(settings, "max_upload_bytes", 3)

    response = client.post(
        "/api/files/upload",
        headers=headers,
        files={"file": ("big.txt", b"1234", "text/plain")},
    )

    assert response.status_code == 413
    assert storage.objects == {}
