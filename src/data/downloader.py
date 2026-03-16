import csv
import hashlib
from datetime import datetime, timezone
from pathlib import Path

import requests

from .paths import RAW_MANIFEST_PATH, ensure_data_dirs


def sha256_file(file_path: Path) -> str:
    """Compute SHA-256 hash for a file."""
    hash_sha256 = hashlib.sha256()
    with file_path.open("rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            hash_sha256.update(chunk)
    return hash_sha256.hexdigest()


def download_file(url: str, target_path: Path, timeout: int = 120) -> Path:
    """Download a file from a URL to target_path."""
    ensure_data_dirs()
    target_path.parent.mkdir(parents=True, exist_ok=True)

    with requests.get(url, stream=True, timeout=timeout) as response:
        response.raise_for_status()
        with target_path.open("wb") as output_file:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    output_file.write(chunk)

    return target_path


def append_to_manifest(
    source_key: str,
    url: str,
    saved_path: Path,
    description: str = "",
) -> None:
    """Append one download event to the raw download manifest."""
    ensure_data_dirs()

    manifest_exists = RAW_MANIFEST_PATH.exists()
    saved_path = saved_path.resolve()

    row = {
        "downloaded_at_utc": datetime.now(timezone.utc).isoformat(),
        "source_key": source_key,
        "url": url,
        "saved_path": str(saved_path),
        "file_name": saved_path.name,
        "sha256": sha256_file(saved_path),
        "description": description,
    }

    with RAW_MANIFEST_PATH.open("a", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(
            csvfile,
            fieldnames=[
                "downloaded_at_utc",
                "source_key",
                "url",
                "saved_path",
                "file_name",
                "sha256",
                "description",
            ],
        )

        if not manifest_exists:
            writer.writeheader()

        writer.writerow(row)
