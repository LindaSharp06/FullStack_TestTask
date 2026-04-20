import mimetypes
from pathlib import Path
from uuid import uuid4

from fastapi import HTTPException, UploadFile, status

from src.database import async_session_maker
from src.models import StoredFile
from src.repository import AlertRepository, FileRepository
from src.schemas import AlertItem, FileItem
import src.storage as storage


async def list_files() -> list[FileItem]:
    async with async_session_maker() as session:
        repo = FileRepository(session)
        files = await repo.get_all()
        return [FileItem.model_validate(f) for f in files]


async def list_alerts() -> list[AlertItem]:
    async with async_session_maker() as session:
        repo = AlertRepository(session)
        alerts = await repo.get_all()
        return [AlertItem.model_validate(a) for a in alerts]


async def get_file(file_id: str) -> FileItem:
    async with async_session_maker() as session:
        repo = FileRepository(session)
        file_item = await repo.get_by_id(file_id)
        if not file_item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File not found")
        return FileItem.model_validate(file_item)


async def create_file(title: str, upload_file: UploadFile) -> FileItem:
    content = await upload_file.read()
    if not content:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="File is empty")

    file_id = str(uuid4())
    suffix = Path(upload_file.filename or "").suffix
    stored_name = f"{file_id}{suffix}"

    storage.write_file(stored_name, content)

    file_item = StoredFile(
        id=file_id,
        title=title,
        original_name=upload_file.filename or stored_name,
        stored_name=stored_name,
        mime_type=upload_file.content_type or mimetypes.guess_type(stored_name)[0] or "application/octet-stream",
        size=len(content),
        processing_status="uploaded",
    )

    async with async_session_maker() as session:
        repo = FileRepository(session)
        saved = await repo.save(file_item)
        return FileItem.model_validate(saved)


async def update_file(file_id: str, title: str) -> FileItem:
    async with async_session_maker() as session:
        repo = FileRepository(session)
        file_item = await repo.get_by_id(file_id)
        if not file_item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File not found")
        file_item.title = title
        updated = await repo.save(file_item)
        return FileItem.model_validate(updated)


async def delete_file(file_id: str) -> None:
    async with async_session_maker() as session:
        repo = FileRepository(session)
        file_item = await repo.get_by_id(file_id)
        if not file_item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File not found")
        storage.delete_file(file_item.stored_name)
        await repo.delete(file_item)
