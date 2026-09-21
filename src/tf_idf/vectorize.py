from pathlib import Path

from pandas import DataFrame, Series


def tf(d: DataFrame, book_id: str, output_dir: Path) -> DataFrame:
    # tf(t, d) = \frac{f(t, d)}{\sum_{t' \in d}{f(t', d)}}

    # vector storing each token with how many occurences there are
    counts: Series[int] = d["token"].value_counts()

    # apply division step of tf to each element
    tf_values: Series[float] = counts / counts.sum()

    # turn Series back into DataFrame
    tf_df: DataFrame = tf_values.reset_index(name="tf")

    # save as parquet
    tf_df.to_parquet(output_dir / f"{book_id}.parquet")

    return tf_df


def idf(D: list[DataFrame]) -> None:
    # idf(t, D) = \log{\frac{N_D}{1 + n_t}}
    pass


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
