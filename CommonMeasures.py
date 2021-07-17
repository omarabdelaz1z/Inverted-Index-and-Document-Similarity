from numpy import log10, linalg, dot


def log_tf(tf):
    if tf > 0:
        return 1 + log10(tf)
    return 0


def idf(N, df):
    return log10((N / df))


def normalize(series):
    return series / linalg.norm(series)


def dot_product(S1, S2):
    return dot(S1, S2)
