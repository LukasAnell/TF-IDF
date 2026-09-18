from pathlib import Path

from pandas import DataFrame
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS


def tokenize(book_id: str) -> None:
    # Root folder
    PROJECT_ROOT: Path = Path(__file__).resolve().parent

    # Designate paths for input and output data
    normalized_data_dir: Path = (
        PROJECT_ROOT.parents[2] / "data" / "processed" / "normalized"
    )
    tokenized_data_dir: Path = (
        PROJECT_ROOT.parents[2] / "data" / "processed" / "tokenized"
    )

    # Create directory
    tokenized_data_dir.mkdir(parents=True, exist_ok=True)

    with open(
        normalized_data_dir / f"{book_id}.txt.utf-8", "r", encoding="utf-8"
    ) as infile:
        # Read in whole file as text
        text: str = infile.read()

        # Split over whitespace so it's a list where each entry is one word
        tokens: list[str] = text.split()

        # Stopword removal using scikit-learn's ENGLISH_STOP_WORD set
        tokens = [token for token in tokens if token not in ENGLISH_STOP_WORDS]

        # Turn list of tokens into a list of dicts that label each token as coming from the given book_id
        rows: list[dict[str, str]] = [
            {"book_id": book_id, "token": token} for token in tokens
        ]

        # Create a pandas DataFrame using tokens
        df: DataFrame = DataFrame(rows)

        # Create parquet file to store tokens on disk
        df.to_parquet(tokenized_data_dir / f"{book_id}.parquet")  # type: ignore


if __name__ == "__main__":
    # List of book ids
    ids: list[str] = [
        "1228",
        "2300",
        "2940",
        "46129",
        "4341",
    ]

    for book_id in ids:
        tokenize(book_id)
