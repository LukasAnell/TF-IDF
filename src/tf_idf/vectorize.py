from pandas import DataFrame


def tf(t: str, d: DataFrame) -> None:
    # tf(t, d) = \frac{f(t, d)}{\sum_{t' \in d}{f(t', d)}}
    pass


def idf(t: str, D: list[DataFrame]) -> None:
    # idf(t, D) = \log{\frac{N_D}{1 + n_t}}
    pass

def tfidf(t, d, D) -> None:
    # tf(t, d) * idf(t, D)
    #
    pass
