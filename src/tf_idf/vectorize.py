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


def tfidf(d: DataFrame, D: DataFrame, output_path: Path) -> DataFrame:
    # tf(t, d) * idf(t, D)

    # read in parquet if it exists
    if output_path.exists():
        return read_parquet(output_path)

    # merge tf and idf DataFrames together
    merged: DataFrame = d.merge(D, on="token")

    # calculate tfidf for each document
    merged["tfidf"] = merged["tf"] * merged["idf"]

    # save as parquet
    merged.to_parquet(output_path)

    return merged


if __name__ == "__main__":
    # Root folder
    PROJECT_ROOT: Path = Path(__file__).resolve().parent

    # Designate paths for input and output data
    tokenized_data_dir: Path = (
        PROJECT_ROOT.parents[1] / "data" / "processed" / "tokenized"
    )
    tf_data_dir: Path = (
        PROJECT_ROOT.parents[1] / "data" / "processed" / "tf"
    )
    idf_data_dir: Path = (
        PROJECT_ROOT.parents[1] / "data" / "processed" / "idf"
    )
    tfidf_data_dir: Path = (
        PROJECT_ROOT.parents[1] / "data" / "processed" / "tfidf"
    )

    # Create directory
    tf_data_dir.mkdir(parents=True, exist_ok=True)
    idf_data_dir.mkdir(parents=True, exist_ok=True)
    tfidf_data_dir.mkdir(parents=True, exist_ok=True)

    # List of book ids
    ids: list[str] = [
        "1228",
        "2300",
        "2940",
        "46129",
        "4341",
    ]

    tf_dfs: list[DataFrame] = []

    # for each document, run tf on it and append it to a list
    for id in ids:
        df: DataFrame = read_parquet(tokenized_data_dir / f"{id}.parquet")
        tf_dfs.append(tf(df, id, tf_data_dir))

    # run idf on list of tf DataFrames
    idf_df: DataFrame = idf(tf_dfs, idf_data_dir / "idf.parquet")

    # run tfidf on every tf DataFrame
    for index, df in enumerate(tf_dfs):
        _ = tfidf(df, idf_df, tfidf_data_dir / f"{ids[index]}.parquet")
