import numpy as np
import pandas as pd
from typing import Optional, Union
from .rolling_helper import rolling_volatility_wrapper

def garman_klass_vol(
    df: pd.DataFrame,
    window: Optional[int] = None,
    rolling: bool = False,
    return_annualized: bool = True,
    trading_days: int = 252
) -> Union[float, pd.Series]:
    """
    Compute Garman-Klass volatility.
    """
    required = {'Open', 'High', 'Low', 'Close'}
    if not required.issubset(df.columns):
        raise ValueError(f"DataFrame must contain {required} columns.")

    def _calc(sub: pd.DataFrame) -> float:
        hl = np.log(sub['High'] / sub['Low'])
        oc = np.log(sub['Close'] / sub['Open'])
        var = 0.5 * (hl ** 2) - (2 * np.log(2) - 1) * (oc ** 2)
        return np.sqrt(var.mean())

    if rolling:
        return rolling_volatility_wrapper(df, window, _calc, return_annualized, trading_days)
    else:
        data = df.tail(window) if window is not None else df
        return _calc(data) * (np.sqrt(trading_days) if return_annualized else 1.0)
