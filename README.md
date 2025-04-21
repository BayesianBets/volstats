**volstats**  
OHLC-based volatility estimators for financial time series.  

---

## Table of Contents
1. [Introduction](#introduction)  
2. [Features](#features)  
3. [Installation](#installation)  
4. [Quick Start](#quick-start)  
5. [API Reference](#api-reference)  
6. [Examples](#examples)  
7. [Contributing](#contributing)  
8. [License](#license)

---

## Introduction
`volstats` is a lightweight Python library providing a suite of popular volatility estimators based on Open–High–Low–Close (OHLC) data. Rather than relying solely on close-to-close returns, these estimators exploit intra-period high and low prices to deliver more efficient and accurate volatility measures.

This package is ideal for quantitative analysts, researchers, and traders who need robust volatility inputs for risk management, option pricing, algorithmic strategies, or academic research.

---

## Features
- **Parkinson volatility**: Uses high–low range to estimate volatility more efficiently than close-to-close.  
- **Garman–Klass volatility**: Incorporates open, close, high, and low prices for improved bias correction.  
- **Rogers–Satchell volatility**: Accounts for drift by combining log‑returns of open vs. high/low/close.  
- **Yang–Zhang volatility**: An advanced estimator correcting for overnight jumps and drift.  
- **Garman‑Klass‑Yang‑Zhang hybrid**: Blends Garman–Klass and Yang–Zhang for an all‑in‑one measure.  
- **Close‑to‑close (historical) volatility**: Standard deviation of log returns with optional annualization.  
- **Annualization helper**: Convert period volatility to annualized figures given trading days per year.  

---

## Installation
Install via PyPI:

```bash
pip install volstats
```

Or install the latest development version directly from GitHub:

```bash
git clone https://github.com/BayesianBets/volstats.git
cd volstats
pip install .
```

---

## Quick Start

```python
import pandas as pd
from volstats import (
    historical_vol,
    parkinson_vol,
    garman_klass_vol,
    rogers_satchell_vol,
    yang_zhang_vol,
    gk_yz_vol,
    annualize
)

# Load OHLC data (DataFrame with columns: 'Open', 'High', 'Low', 'Close')
df = pd.read_csv('AAPL_3yr.csv', parse_dates=['Date'], index_col='Date')

# Compute Parkinson volatility
park_vol = parkinson_vol(
    high=df['High'], low=df['Low'],
    log=True  # set to False for non-logged return form
)

# Annualize that volatility (assuming 252 trading days per year)
park_ann = annualize(park_vol, periods_per_year=252)
print(f"Parkinson annualized volatility: {park_ann:.2%}")
```

---

## API Reference

### `historical_vol(close, window=None, log=True)`
- **Description**: Close-to-close historical volatility (std dev of log returns).  
- **Parameters**:
  - `close` (`Series`): Series of closing prices.  
  - `window` (`int`, optional): Rolling window size (e.g., 21 for monthly). If `None`, computes over entire series.  
  - `log` (`bool`): Whether to compute on log returns (`True`) or simple returns (`False`).  
- **Returns**: `float` or `Series` of volatility estimates.

### `parkinson_vol(high, low, log=True)`
- **Description**: Parkinson (1980) estimator using the range `log(high/low)`.  
- **Parameters**:
  - `high`, `low` (`Series`): High and low price series.  
  - `log` (`bool`): Whether to apply log transformation.  
- **Returns**: `float` volatility estimate.

### `garman_klass_vol(open, high, low, close, log=True)`
- **Description**: Garman–Klass (1980) estimator leveraging open-close and high-low ranges.  
- **Parameters**: same as Parkinson plus `open` & `close`.  
- **Returns**: `float` volatility estimate.

### `rogers_satchell_vol(open, high, low, close)`
- **Description**: Rogers–Satchell (1991) captures drift components.  
- **Parameters**: `open`, `high`, `low`, `close`.  
- **Returns**: `float` volatility estimate.

### `yang_zhang_vol(open, high, low, close, window=None)`
- **Description**: Yang–Zhang (2000) combines overnight and intraday measures.  
- **Parameters**:
  - `window` (`int`, optional): When provided, computes rolling volatility.  
- **Returns**: `float` or `Series`.

### `gk_yz_vol(open, high, low, close, window=None)`
- **Description**: Hybrid Garman–Klass and Yang–Zhang estimator.  
- **Parameters**: same as Yang–Zhang.  
- **Returns**: `float` or `Series`.

### `annualize(vol, periods_per_year=252)`
- **Description**: Annualize a volatility figure.  
- **Parameters**:
  - `vol` (`float` or `Series`): Period volatility.  
  - `periods_per_year` (`int`): Number of periods per year (default 252 trading days).  
- **Returns**: Annualized volatility.

---

## Examples

See the `examples/` folder for Jupyter notebooks demonstrating:
- Backtesting volatility forecasts.  
- Comparing estimators on historical stock data.  
- Integrating `volstats` into option pricing workflows.  

---

## Contributing

Contributions are welcome! Please:
1. Fork the repo.  
2. Create a new branch (`git checkout -b feature/your-feature`).  
3. Add tests, ensuring new code is covered.  
4. Submit a pull request.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

