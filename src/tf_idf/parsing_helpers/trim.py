import logging
from logging import Logger
from pathlib import Path

# Trim before `When on board H.M.S. ‘Beagle,’ as naturalist, I was much struck with`
# Trim after `and are being, evolved.`


# Trim before `The nature of the following work will be best understood by a brief`
# Trim after `probability to the action of sexual selection.`


# Trim before `IT may be safely assumed that, two thousand years ago, before Caesar` (11-12 lines before this?)
# Trim after `"Childe Roland to the dark Tower came."`


# Trim before `Two aspects of animal life impressed me most during the journeys which I` (3-4 lines before this?)
# Trim after `evolution of our race.`


# Trim before `THE DATA OF ETHICS.`
# Trim after `Transcriber's note:`


def trim_text(
    input_path: Path, output_path: Path, start_phrase: str, end_phrase: str
) -> None:
    # Track whether lines are being written to the output (start_phrase was found)
    recording: bool = False

    # Track whether the end_phrase was found
    # Otherwise, all lines after start_phrase are written to the outuput
    found_end: bool = False

    # Open both input file and output file
    with (
        open(input_path, "r", encoding="utf-8") as infile,
        open(output_path, "w", encoding="utf-8") as outfile,
    ):
        for line in infile:
            # If start_phrase is found, start writing to output
            if not recording and start_phrase in line:
                recording = True

                _ = outfile.write(line)
                continue

            # If the end_phrase is found, stop writing to output
            # Also add check for if end_phrase came before start_phrase
            if recording:
                if end_phrase in line:
                    found_end = True
                    break

                _ = outfile.write(line)

    # Add warnings if start_phrase or end_phrase weren't found
    if not recording:
        logger.warning("Start phrase was not found in the file.")
    elif not found_end:
        logger.warning(
            "End phrase was not found, trimmed everything after start phrase."
        )


if __name__ == "__main__":
    # Create logger
    logger: Logger = logging.getLogger(__name__)

    # List of book ids
    ids: list[int] = [
        1228,
        2300,
        2940,
        46129,
        4341,
    ]

    # Root folder
    PROJECT_ROOT: Path = Path(__file__).resolve().parent

    # Define directory storing raw data
    raw_data_dir: Path = PROJECT_ROOT.parents[2] / "data" / "raw"
