import argparse
from pathlib import Path

from .downloader import append_to_manifest, download_file
from .paths import (
    RAW_CITEPA_DIR,
    RAW_DRIAS_DIR,
    RAW_IMPACTS_DIR,
    RAW_METEO_DIR,
    ensure_data_dirs,
)

SOURCE_DIRECTORIES = {
    "meteo": RAW_METEO_DIR,
    "drias": RAW_DRIAS_DIR,
    "citepa": RAW_CITEPA_DIR,
    "impacts": RAW_IMPACTS_DIR,
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Download one raw file and register it in the manifest."
    )
    parser.add_argument(
        "--source",
        required=True,
        choices=SOURCE_DIRECTORIES.keys(),
        help="Source key: meteo, drias, citepa, impacts",
    )
    parser.add_argument(
        "--url",
        required=True,
        help="Direct download URL",
    )
    parser.add_argument(
        "--filename",
        required=True,
        help="Target filename to save under the source raw directory",
    )
    parser.add_argument(
        "--description",
        default="",
        help="Optional human-readable description",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    ensure_data_dirs()

    target_dir = SOURCE_DIRECTORIES[args.source]
    target_path = Path(target_dir) / args.filename

    download_file(args.url, target_path)
    append_to_manifest(
        source_key=args.source,
        url=args.url,
        saved_path=target_path,
        description=args.description,
    )

    print(f"Downloaded: {target_path}")


if __name__ == "__main__":
    main()
