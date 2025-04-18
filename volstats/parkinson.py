import numpy as np
import pandas as pd
from typing import Optional, Union
from .rolling_helper import rolling_volatility_wrapper

def parkinson_vol(
    df: pd.DataFrame,
    window: Optional[int] = None,
    rolling: bool = False,
    return_annualized: bool = True,
    trading_days: int = 252
) -> Union[float, pd.Series]:
    """
    Compute Parkinson's volatility.
    """
    if not {'High', 'Low'}.issubset(df.columns):
        raise ValueError("DataFrame must contain 'High' and 'Low' columns.")

    def _calc(sub: pd.DataFrame) -> float:
        hl = np.log(sub['High'] / sub['Low'])
        var = (hl ** 2).mean() / (4 * np.log(2))
        return np.sqrt(var)

    if rolling:
        return rolling_volatility_wrapper(df, window, _calc, return_annualized, trading_days)
    else:
        data = df.tail(window) if window is not None else df
        return _calc(data) * (np.sqrt(trading_days) if return_annualized else 1.0)
