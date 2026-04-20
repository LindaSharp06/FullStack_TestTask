from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
STORAGE_DIR = BASE_DIR / "storage" / "files"
STORAGE_DIR.mkdir(parents=True, exist_ok=True)


def write_file(stored_name: str, content: bytes) -> Path:
    path = STORAGE_DIR / stored_name
    path.write_bytes(content)
    return path


def delete_file(stored_name: str) -> None:
    path = STORAGE_DIR / stored_name
    if path.exists():
        path.unlink()


def get_path(stored_name: str) -> Path:
    return STORAGE_DIR / stored_name
