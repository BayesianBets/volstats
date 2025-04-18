import numpy as np
import pandas as pd
from typing import Optional, Union

def close_to_close_vol(
    df: pd.DataFrame,
    window: Optional[int] = None,
    rolling: bool = False,
    return_annualized: bool = True,
    trading_days: int = 252
) -> Union[float, pd.Series]:
    """
    Compute close-to-close volatility.

    Parameters
    ----------
    df : pd.DataFrame
        Must contain a 'Close' column.
    window : int, optional
        Window size for rolling calculation.
    rolling : bool
        If True, returns a pd.Series of the same length as df, with NaNs
        for the first window-1 entries.
    return_annualized : bool
        Whether to annualize the volatility (sqrt(trading_days)).
    trading_days : int
        Number of trading days in a year (for annualization).

    Returns
    -------
    float or pd.Series
    """
    if 'Close' not in df.columns:
        raise ValueError("Input DataFrame must contain 'Close' column.")

    # log returns, dropping the very first NaN
    log_ret = np.log(df['Close'] / df['Close'].shift(1)).dropna()

    if rolling:
        if window is None:
            raise ValueError("For rolling volatility, 'window' must be specified.")

        # 1) compute rolling std on the log-returns series
        raw = log_ret.rolling(window=window).std()

        # 2) annualize if requested
        if return_annualized:
            raw = raw * np.sqrt(trading_days)

        # 3) reindex onto the original df index so length matches
        out = pd.Series(index=df.index, dtype=float)
        out.loc[raw.index] = raw

        return out

    else:
        # non‑rolling: optionally take only the last `window` returns
        if window is not None:
            log_ret = log_ret.tail(window)

        vol = log_ret.std()
        return vol * np.sqrt(trading_days) if return_annualized else vol
