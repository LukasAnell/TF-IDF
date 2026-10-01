from pathlib import Path

import matplotlib.pyplot as plt
from numpy import dot, outer
from numpy.linalg import norm
from pandas import DataFrame, concat, read_parquet


def load_stage(data_dir: Path, ids: list[str]) -> DataFrame:
    # Read each book's parquet and add it into the list of DataFrames
    dfs: list[DataFrame] = []
    for book_id in ids:
        df: DataFrame = read_parquet(data_dir / f"{book_id}.parquet")

        # re-add a book_id column
        df["book_id"] = book_id
        dfs.append(df)

    # Concatenate every DataFrame in the list, with 1 row per (book_id, token)
    return concat(dfs, ignore_index=True)


def top_terms(df: DataFrame, value_col: str, n: int) -> DataFrame:
    # Sort by value_col, keeping the top n terms
    return (
        df.sort_values(["book_id", value_col], ascending=[True, False])
        .groupby("book_id")
        .head(n)
        .reset_index(drop=True)
    )


def idf_extremes(idf_df: DataFrame, n: int) -> tuple[DataFrame, DataFrame]:
    # Most common terms
    lowest: DataFrame = idf_df.nsmallest(n, "idf")

    # Rarest terms
    highest: DataFrame = idf_df.nlargest(n, "idf")

    return lowest, highest


def to_wide(tfidf_long: DataFrame) -> DataFrame:
    # Pivot DataFrame so each row is one book, and each column is one token
    # If a book doesn't have a given token, store as 0
    return tfidf_long.pivot(index="book_id", columns="token", values="tfidf").fillna(0)


def cosine_similarity(wide: DataFrame) -> DataFrame:
    # Compute cosine similarity for every pair of rows at once
    vectors = wide.to_numpy()
    dots = dot(vectors, vectors.T)
    norms = norm(vectors, axis=1)
    sim = dots / outer(norms, norms)

    # Return DataFrame holding cosine similarity values
    return DataFrame(sim, index=wide.index, columns=wide.index)


def plot_top_terms(
    top: DataFrame, value_col: str, output_dir: Path, filename: str
) -> None:
    # Make each book have one horizontal bar chart
    # Each chart is stacked vertically
    book_ids: list[str] = list(top["book_id"].unique())
    fig, axes = plt.subplots(len(book_ids), 1, figsize=(8, 3 * len(book_ids)))

    for ax, book_id in zip(axes, book_ids):
        book: DataFrame = top[top["book_id"] == book_id]

        # Make the highest value be at the top
        ax.barh(book["token"][::-1], book[value_col][::-1])
        ax.set_title(book_id)
        ax.set_xlabel(value_col)

    fig.tight_layout()
    fig.savefig(output_dir / filename, dpi=150)
    plt.close(fig)


def plot_similarity(sim: DataFrame, output_dir: Path, filename: str) -> None:
    # Heatmap of the similarity matrix with each cell's value printed on it
    fig, ax = plt.subplots(figsize=(6, 5))
    image = ax.imshow(sim.to_numpy(), cmap="viridis")

    ax.set_xticks(range(len(sim.columns)), labels=sim.columns)
    ax.set_yticks(range(len(sim.index)), labels=sim.index)

    for i in range(len(sim.index)):
        for j in range(len(sim.columns)):
            ax.text(
                j, i, f"{sim.iat[i, j]:.2f}", ha="center", va="center", color="white"
            )

    fig.colorbar(image, ax=ax, label="cosine similarity")
    ax.set_title("TF-IDF cosine similarity between books")
    fig.tight_layout()
    fig.savefig(output_dir / filename, dpi=150)
    plt.close(fig)


if __name__ == "__main__":
    # Root folder
    PROJECT_ROOT: Path = Path(__file__).resolve().parent

    # Designate paths for input data and output figures
    tf_data_dir: Path = PROJECT_ROOT.parents[1] / "data" / "processed" / "tf"
    idf_data_dir: Path = PROJECT_ROOT.parents[1] / "data" / "processed" / "idf"
    tfidf_data_dir: Path = PROJECT_ROOT.parents[1] / "data" / "processed" / "tfidf"
    figures_dir: Path = PROJECT_ROOT.parents[1] / "figures"

    # Create directory
    figures_dir.mkdir(parents=True, exist_ok=True)

    # List of book ids
    ids: list[str] = [
        "1228",
        "2300",
        "2940",
        "46129",
        "4341",
    ]

    # Load data into separate DatFrames for each stage
    tf_long: DataFrame = load_stage(tf_data_dir, ids)
    tfidf_long: DataFrame = load_stage(tfidf_data_dir, ids)
    idf_df: DataFrame = read_parquet(idf_data_dir / "idf.parquet")

    # Sorted tf and idf
    print(top_terms(tf_long, "tf", 10))
    lowest, highest = idf_extremes(idf_df, 10)
    print(lowest)
    print(highest)

    # Highest tfidf terms per book
    top_tfidf: DataFrame = top_terms(tfidf_long, "tfidf", 10)
    print(top_tfidf)

    # Compare books as vectors using cosine similarity
    wide: DataFrame = to_wide(tfidf_long)
    similarity: DataFrame = cosine_similarity(wide)
    print(similarity.round(3))

    # Plotting
    plot_top_terms(top_tfidf, "tfidf", figures_dir, "top_tfidf_terms.png")
    plot_similarity(similarity, figures_dir, "tfidf_similarity.png")
