import numpy as np
import pandas as pd
from typing import Callable, Optional

def rolling_volatility_wrapper(
    df: pd.DataFrame,
    window: int,
    calc_func: Callable[[pd.DataFrame], float],
    return_annualized: bool = True,
    trading_days: int = 252
) -> pd.Series:
    """
    Compute rolling volatility using a custom OHLC-based estimator.

    Parameters
    ----------
    df : pd.DataFrame
        OHLC DataFrame sorted by date.
    window : int
        Rolling window size.
    calc_func : Callable
        Function that takes a DataFrame window and returns volatility.
    return_annualized : bool
        Whether to annualize the result.
    trading_days : int
        Number of trading days in a year for annualization.

    Returns
    -------
    pd.Series
        Series of rolling volatility values.
    """
    if window is None:
        raise ValueError("For rolling volatility, 'window' must be specified.")

    df = df.sort_index()
    out = pd.Series(index=df.index, dtype=float)

    for i in range(window - 1, len(df)):
        sub = df.iloc[i - window + 1 : i + 1]
        val = calc_func(sub)
        if return_annualized:
            val *= np.sqrt(trading_days)
        out.iloc[i] = val

    return out
