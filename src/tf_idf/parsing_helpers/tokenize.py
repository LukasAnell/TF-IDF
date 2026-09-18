from pathlib import Path


def tokenize(book_id: int) -> None:
    # Root folder
    PROJECT_ROOT: Path = Path(__file__).resolve().parent

    # Designate paths for input and output data
    normalized_data_dir: Path = (
        PROJECT_ROOT.parents[2] / "data" / "processed" / "normalized"
    )
    tokenized_data_dir: Path = PROJECT_ROOT.parents[2] / "data" / "processed" / "tokenized"

    # Create directory
    tokenized_data_dir.mkdir(parents=True, exist_ok=True)


if __name__ == "__main__":
    # List of book ids
    ids: list[int] = [
        1228,
        2300,
        2940,
        46129,
        4341,
    ]

    for book_id in ids:
        tokenize(book_id)
