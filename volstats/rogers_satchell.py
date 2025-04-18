import numpy as np
import pandas as pd
from typing import Optional, Union
from .rolling_helper import rolling_volatility_wrapper

def rogers_satchell_vol(
    df: pd.DataFrame,
    window: Optional[int] = None,
    rolling: bool = False,
    return_annualized: bool = True,
    trading_days: int = 252
) -> Union[float, pd.Series]:
    """
    Compute Rogers-Satchell volatility.
    """
    required = {'Open', 'High', 'Low', 'Close'}
    if not required.issubset(df.columns):
        raise ValueError(f"DataFrame must contain {required} columns.")

    def _calc(sub: pd.DataFrame) -> float:
        o, h, l, c = sub['Open'], sub['High'], sub['Low'], sub['Close']
        term = (np.log(h / o) * np.log(h / c) +
                np.log(l / o) * np.log(l / c))
        return np.sqrt(term.mean())

    if rolling:
        return rolling_volatility_wrapper(df, window, _calc, return_annualized, trading_days)
    else:
        data = df.tail(window) if window is not None else df
        return _calc(data) * (np.sqrt(trading_days) if return_annualized else 1.0)
