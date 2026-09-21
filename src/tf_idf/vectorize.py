from pathlib import Path

from numpy import log
from pandas import DataFrame, Series, concat, read_parquet


def tf(d: DataFrame, book_id: str, output_dir: Path) -> DataFrame:
    # tf(t, d) = \frac{f(t, d)}{\sum_{t' \in d}{f(t', d)}}

    # read in parquet if it exists
    output_path: Path = output_dir / f"{book_id}.parquet"
    if output_path.exists():
        return read_parquet(output_path)

    # vector storing each token with how many occurences there are
    counts: Series[int] = d["token"].value_counts()

    # apply division step of tf to each element
    tf_values: Series[float] = counts / counts.sum()

    # turn Series back into DataFrame
    tf_df: DataFrame = tf_values.reset_index(name="tf")

    # save as parquet
    tf_df.to_parquet(output_path)

    return tf_df


def idf(D: list[DataFrame], output_path: Path) -> DataFrame:
    # idf(t, D) = \log{\frac{N_D}{1 + n_t}}

    # read in parquet if it exists
    if output_path.exists():
        return read_parquet(output_path)

    # get total number of documents
    N_D: int = len(D)

    # combine all documents into one
    combined: DataFrame = concat(D)

    # get each token's occurences across all documents
    n_t: Series[int] = combined["token"].value_counts()

    # calculate idf for each term
    idf_values: Series[float] = log(N_D / (1 + n_t))  # type: ignore[assignment]

    # convert back to DataFrame
    idf_df: DataFrame = idf_values.reset_index(name="idf")

    # save as parquet
    idf_df.to_parquet(output_path)

    return idf_df


def tfidf(t, d, D) -> None:
    # tf(t, d) * idf(t, D)
    #
    pass


if __name__ == "__main__":
    # List of book ids
    ids: list[str] = [
        "1228",
        "2300",
        "2940",
        "46129",
        "4341",
    ]

    pass
