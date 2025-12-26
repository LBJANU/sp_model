# S&P 500 Sector Deviation Analysis

This project analyzes the deviation of individual S&P sectors vs the S&P 500 over time and calculates correlations between sectors and the overall index.

## Features

- **Deviation Returns Analysis**: Calculates and visualizes how each sector's returns deviate from the S&P 500
- **Correlation Analysis**: Computes correlation matrix between all sectors and S&P 500
- **Visualizations**: 
  - Time series plot of deviation returns
  - Cumulative deviation returns
  - Correlation heatmap

## Setup

### 1. Create and activate virtual environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

## Usage

Run the main script:

```bash
python main.py
```

The script will:
1. Fetch historical data for S&P 500 (SPY) and all sector ETFs
2. Calculate daily returns
3. Calculate deviation returns (sector returns - S&P 500 returns)
4. Generate visualizations
5. Calculate and display correlation matrix
6. Save results to CSV files

## Output Files

- `sector_deviations.png`: Time series plot of deviation returns
- `cumulative_deviations.png`: Cumulative deviation returns over time
- `correlation_heatmap.png`: Correlation matrix visualization
- `deviation_returns.csv`: Raw deviation returns data
- `correlation_matrix.csv`: Correlation matrix data

## Sectors Analyzed

- Technology (XLK)
- Healthcare (XLV)
- Financials (XLF)
- Consumer Discretionary (XLY)
- Communication Services (XLC)
- Industrials (XLI)
- Consumer Staples (XLP)
- Energy (XLE)
- Utilities (XLU)
- Real Estate (XLRE)
- Materials (XLB)

## Roadmap

1. ✅ Set up virtual environment and dependencies
2. ✅ Data fetching module for S&P 500 and sector ETFs
3. ✅ Returns and deviation returns calculation
4. ✅ Visualization module for deviation returns
5. ✅ Correlation analysis and heatmap
6. ✅ Main implementation

