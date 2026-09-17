import logging
from logging import Logger
from pathlib import Path

import requests


# Download a book into the designated destination folder
def download_book(url: str, destination_folder: Path) -> None:
    # Filename will just be ID from Project Gutenberg
    filename: str = f"{url.split('/')[-1]}"

    # Get full path for will-be downloaded file
    file_path: Path = destination_folder / filename

    # Send request to URL
    with requests.get(url, stream=True) as response:
        # Check if request was successful
        response.raise_for_status()

        # Open fetched file
        with open(file_path, "wb") as file:
            # Write file in 8KiB chunks
            file.writelines(response.iter_content(chunk_size=8192))

    # Log completed download
    logger.info(f"Downloaded: {filename} to {destination_folder}")


if __name__ == "__main__":
    # Create logger
    logger: Logger = logging.getLogger(__name__)

    # List of books to download
    ids: list[int] = [
        1228,
        2300,
        2940,
        46129,
        4341,
    ]

    # Find project's root folder instead of using relative paths
    PROJECT_ROOT: Path = Path(__file__).resolve().parent

    # Define directory to download books into
    download_dir: Path = PROJECT_ROOT.parents[2] / "data" / "raw"

    # Create directories if it doesn't already exist
    download_dir.mkdir(parents=True, exist_ok=True)

    # Run downloader for each url in the list
    for book_id in ids:
        url: str = f"https://www.gutenberg.org/ebooks/{book_id}.txt.utf-8"
        download_book(url, download_dir)
