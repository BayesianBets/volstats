from volstats import close_to_close_vol

def test_close_to_close_single(simple_ohlc):
    vol = close_to_close_vol(simple_ohlc)
    assert isinstance(vol, float)
    assert vol >= 0

def test_close_to_close_rolling(simple_ohlc):
    series = close_to_close_vol(simple_ohlc, window=3, rolling=True)
    assert len(series) == len(simple_ohlc)
    assert series.dropna().min() >= 0
