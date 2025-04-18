import pandas as pd
import numpy as np
import pytest

@pytest.fixture
def simple_ohlc():
    data = {
        "Open":  [100, 102, 101, 103, 102],
        "High":  [101, 103, 102, 104, 103],
        "Low":   [ 99, 101, 100, 102, 101],
        "Close": [100.5, 102.5, 101.5, 103.5, 102.5]
    }
    idx = pd.date_range("2025-01-01", periods=5)
    return pd.DataFrame(data, index=idx)
