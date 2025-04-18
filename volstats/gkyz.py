import numpy as np
import pandas as pd
from typing import Optional, Union
from .rolling_helper import rolling_volatility_wrapper

def gkyz_vol(
    df: pd.DataFrame,
    window: Optional[int] = None,
    rolling: bool = False,
    return_annualized: bool = True,
    trading_days: int = 252
) -> Union[float, pd.Series]:
    """
    Compute GKYZ (hybrid) volatility estimator.
    """
    required = {'Open', 'High', 'Low', 'Close'}
    if not required.issubset(df.columns):
        raise ValueError(f"DataFrame must contain {required} columns.")

    def _calc(sub: pd.DataFrame) -> float:
        o = sub['Open'].values
        h = sub['High'].values
        l = sub['Low'].values
        c = sub['Close'].values
        c_prev = np.roll(c, 1)
        o, h, l, c, c_prev = o[1:], h[1:], l[1:], c[1:], c_prev[1:]

        term1 = 0.5 * (np.log(o / c_prev))**2
        term2 = 0.5 * (np.log(h / l))**2
        term3 = (2*np.log(2) - 1) * (np.log(c / o))**2
        return np.sqrt(np.mean(term1 + term2 - term3))

    if rolling:
        return rolling_volatility_wrapper(df, window, _calc, return_annualized, trading_days)
    else:
        data = df.tail(window) if window is not None else df
        return _calc(data) * (np.sqrt(trading_days) if return_annualized else 1.0)
