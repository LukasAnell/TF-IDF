import re
from pathlib import Path


def normalize(filename: str) -> None:
    # Compiled regex to remove punctuation
    punctuation_pattern = re.compile(r"[^\w\s]")

    # Root folder
    PROJECT_ROOT: Path = Path(__file__).resolve().parent

    # Designate paths for input and output data
    trimmed_data_dir: Path = PROJECT_ROOT.parents[2] / "data" / "processed" / "trimmed"
    normalized_data_dir: Path = (
        PROJECT_ROOT.parents[2] / "data" / "processed" / "normalized"
    )

    # Create directory
    normalized_data_dir.mkdir(parents=True, exist_ok=True)

    # Open input file and output file
    with (
        open(trimmed_data_dir / filename, "r", encoding="utf-8") as infile,
        open(normalized_data_dir / filename, "w", encoding="utf-8") as outfile,
    ):
        for line in infile:
            cleaned_line = punctuation_pattern.sub("", line.casefold())

            _ = outfile.write(cleaned_line)


if __name__ == "__main__":
    # List of book ids
    ids: list[int] = [
        1228,
        2300,
        2940,
        46129,
        4341,
    ]
