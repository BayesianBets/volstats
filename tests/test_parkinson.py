from volstats import parkinson_vol

def test_parkinson_basic(simple_ohlc):
    vol = parkinson_vol(simple_ohlc)
    assert isinstance(vol, float)
    assert vol >= 0
