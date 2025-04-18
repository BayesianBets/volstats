from volstats import yang_zhang_vol

def test_yang_zhang_basic(simple_ohlc):
    vol = yang_zhang_vol(simple_ohlc)
    assert isinstance(vol, float)
    assert vol >= 0
