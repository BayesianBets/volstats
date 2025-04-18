import numpy as np
import pandas as pd
from typing import Optional, Union

def ewma_vol(
    df: pd.DataFrame,
    span: int = 20,
    window: Optional[int] = None,
    rolling: bool = False,
    return_annualized: bool = True,
    trading_days: int = 252
) -> Union[float, pd.Series]:
    """
    Compute EWMA volatility.
    """
    if 'Close' not in df.columns:
        raise ValueError("DataFrame must contain 'Close' column.")

    log_ret = np.log(df['Close'] / df['Close'].shift(1)).dropna()

    if rolling:
        if window is None:
            raise ValueError("For rolling volatility, 'window' must be specified.")
        out = pd.Series(index=log_ret.index, dtype=float)
        for i in range(window - 1, len(log_ret)):
            sl = log_ret.iloc[i - window + 1 : i + 1]
            var = sl.ewm(span=span, adjust=False).var().iloc[-1]
            out.iloc[i] = np.sqrt(var) * (np.sqrt(trading_days) if return_annualized else 1.0)
        return out
    else:
        data = log_ret.tail(window) if window is not None else log_ret
        var = data.ewm(span=span, adjust=False).var().iloc[-1]
        return np.sqrt(var) * (np.sqrt(trading_days) if return_annualized else 1.0)
