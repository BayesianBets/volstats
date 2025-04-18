import numpy as np
import pandas as pd
from typing import Optional, Union
from .rolling_helper import rolling_volatility_wrapper

def yang_zhang_vol(
    df: pd.DataFrame,
    window: Optional[int] = None,
    rolling: bool = False,
    return_annualized: bool = True,
    trading_days: int = 252
) -> Union[float, pd.Series]:
    """
    Compute Yang-Zhang volatility estimator.
    """
    required = {'Open', 'High', 'Low', 'Close'}
    if not required.issubset(df.columns):
        raise ValueError(f"DataFrame must contain {required} columns.")

    def _calc(sub: pd.DataFrame) -> float:
        sub = sub.sort_index()
        log_oc_prev = np.log(sub['Open'] / sub['Close'].shift(1)).dropna()
        log_co      = np.log(sub['Close'] / sub['Open'])
        n = len(log_co)
        if n < 2:
            return np.nan

        rs = ((np.log(sub['High'] / sub['Open'])**2 +
               np.log(sub['Low']  / sub['Open'])**2) / 2).mean()
        close_var = log_co.var()
        open_var  = log_oc_prev.var()
        k = 0.34 / (1.34 + (n+1)/(n-1))
        return np.sqrt(close_var + k*open_var + (1-k)*rs)

    if rolling:
        return rolling_volatility_wrapper(df, window, _calc, return_annualized, trading_days)
    else:
        data = df.tail(window) if window is not None else df
        return _calc(data) * (np.sqrt(trading_days) if return_annualized else 1.0)
