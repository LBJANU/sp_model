"""
Data Fetching Module for S&P 500 Sector Analysis

This module handles fetching historical stock data for:
- S&P 500 (SPY ETF)
- Individual S&P sector ETFs
"""

import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta
from typing import Dict, Optional, Tuple


# S&P 500 ETF ticker
SPY_TICKER = 'SPY'

# S&P Sector ETF Tickers
SECTOR_TICKERS = {
    'Technology': 'XLK',
    'Healthcare': 'XLV',
    'Financials': 'XLF',
    'Consumer Discretionary': 'XLY',
    'Communication Services': 'XLC',
    'Industrials': 'XLI',
    'Consumer Staples': 'XLP',
    'Energy': 'XLE',
    'Utilities': 'XLU',
    'Real Estate': 'XLRE',
    'Materials': 'XLB'
}


def fetch_spy_data(start_date: datetime, end_date: datetime) -> pd.Series:
    """
    Fetch S&P 500 historical data.
    
    Args:
        start_date: Start date for data retrieval
        end_date: End date for data retrieval
    
    Returns:
        Series with closing prices indexed by date
    """
    print(f"Fetching S&P 500 (SPY) data from {start_date.date()} to {end_date.date()}...")
    
    try:
        spy = yf.Ticker(SPY_TICKER)
        data = spy.history(start=start_date, end=end_date)
        
        if data.empty:
            raise ValueError(f"No data retrieved for {SPY_TICKER}")
        
        closing_prices = data['Close']
        print(f"✓ Successfully fetched {len(closing_prices)} days of S&P 500 data")
        return closing_prices
    
    except Exception as e:
        raise Exception(f"Error fetching S&P 500 data: {str(e)}")


def fetch_sector_data(start_date: datetime, end_date: datetime) -> pd.DataFrame:
    """
    Fetch historical data for all S&P sector ETFs.
    
    Args:
        start_date: Start date for data retrieval
        end_date: End date for data retrieval
    
    Returns:
        DataFrame with closing prices for each sector, columns are sector names
    """
    print(f"\nFetching sector ETF data from {start_date.date()} to {end_date.date()}...")
    
    sector_data = {}
    failed_tickers = []
    
    for sector_name, ticker in SECTOR_TICKERS.items():
        try:
            print(f"  Fetching {sector_name} ({ticker})...", end=' ')
            stock = yf.Ticker(ticker)
            data = stock.history(start=start_date, end=end_date)
            
            if data.empty:
                print(f"✗ No data")
                failed_tickers.append((sector_name, ticker))
                continue
            
            sector_data[sector_name] = data['Close']
            print(f"✓ {len(data)} days")
        
        except Exception as e:
            print(f"✗ Error: {str(e)}")
            failed_tickers.append((sector_name, ticker))
    
    if not sector_data:
        raise Exception("Failed to fetch data for all sectors")
    
    if failed_tickers:
        print(f"\n⚠ Warning: Failed to fetch {len(failed_tickers)} sector(s):")
        for sector, ticker in failed_tickers:
            print(f"  - {sector} ({ticker})")
    
    # Convert to DataFrame
    df = pd.DataFrame(sector_data)
    print(f"\n✓ Successfully fetched data for {len(df.columns)} sectors")
    
    return df


def fetch_all_data(
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    years_back: int = 5
) -> Tuple[pd.Series, pd.DataFrame]:
    """
    Fetch both S&P 500 and all sector data.
    
    Args:
        start_date: Start date (if None, calculates from years_back)
        end_date: End date (if None, uses today)
        years_back: Number of years to look back (used if start_date is None)
    
    Returns:
        Tuple of (S&P 500 prices, Sector prices DataFrame)
    """
    # Set default dates if not provided
    if end_date is None:
        end_date = datetime.now()
    
    if start_date is None:
        start_date = end_date - timedelta(days=years_back * 365)
    
    # Fetch S&P 500 data
    spy_prices = fetch_spy_data(start_date, end_date)
    
    # Fetch sector data
    sector_prices = fetch_sector_data(start_date, end_date)
    
    # Align to S&P 500 dates (S&P is the reference, sectors may have different start dates)
    # This ensures we have S&P data for all dates, but sectors can have NaN for early dates
    all_dates = spy_prices.index.union(sector_prices.index).sort_values()
    spy_prices = spy_prices.reindex(all_dates)
    sector_prices = sector_prices.reindex(all_dates)
    
    # Show date range info for each sector
    print(f"\n✓ Data prepared:")
    print(f"  S&P 500 date range: {spy_prices.index.min().date()} to {spy_prices.index.max().date()}")
    print(f"  Sector date ranges:")
    for sector in sector_prices.columns:
        sector_dates = sector_prices[sector].dropna()
        if not sector_dates.empty:
            print(f"    {sector:30s}: {sector_dates.index.min().date()} to {sector_dates.index.max().date()}")
    
    return spy_prices, sector_prices


def get_data_info(spy_prices: pd.Series, sector_prices: pd.DataFrame) -> None:
    """
    Print summary information about the fetched data.
    
    Args:
        spy_prices: S&P 500 price series
        sector_prices: Sector prices DataFrame
    """
    print("\n" + "="*60)
    print("DATA SUMMARY")
    print("="*60)
    print(f"S&P 500 (SPY):")
    print(f"  Date range: {spy_prices.index.min().date()} to {spy_prices.index.max().date()}")
    print(f"  Total days: {len(spy_prices)}")
    print(f"  Missing values: {spy_prices.isna().sum()}")
    
    print(f"\nSectors ({len(sector_prices.columns)} total):")
    for sector in sector_prices.columns:
        missing = sector_prices[sector].isna().sum()
        print(f"  {sector:30s}: {len(sector_prices)} days, {missing} missing")
    
    print("="*60 + "\n")


def inspect_sector_data(spy_prices: pd.Series, sector_prices: pd.DataFrame) -> None:
    """
    Quick test function to inspect the type and structure of sector data.
    
    Args:
        spy_prices: S&P 500 price series
        sector_prices: Sector prices DataFrame
    """
    print("\n" + "="*60)
    print("DATA TYPE INSPECTION")
    print("="*60)
    
    # S&P 500 data info
    print("\n📊 S&P 500 (SPY) Data:")
    print(f"  Type: {type(spy_prices)}")
    print(f"  Data type: {spy_prices.dtype}")
    print(f"  Index type: {type(spy_prices.index)}")
    print(f"  Shape: {spy_prices.shape}")
    print(f"  Sample values:")
    print(spy_prices.head(3))
    print(f"  Min value: ${spy_prices.min():.2f}")
    print(f"  Max value: ${spy_prices.max():.2f}")
    
    # Sector data info
    print("\n📊 Sector Data:")
    print(f"  Type: {type(sector_prices)}")
    print(f"  Shape: {sector_prices.shape} (rows, columns)")
    print(f"  Columns: {list(sector_prices.columns)}")
    print(f"  Index type: {type(sector_prices.index)}")
    print(f"  Data types per column:")
    for col in sector_prices.columns:
        print(f"    {col:30s}: {sector_prices[col].dtype}")
    
    print(f"\n  Sample values (first 3 rows):")
    print(sector_prices.head(3))
    
    print(f"\n  Price ranges per sector:")
    for col in sector_prices.columns:
        print(f"    {col:30s}: ${sector_prices[col].min():7.2f} - ${sector_prices[col].max():7.2f}")
    
    print("="*60 + "\n")


if __name__ == "__main__":
    # Test the data fetching module
    print("Testing Data Fetching Module")
    print("="*60)
    
    spy_data, sector_data = fetch_all_data(years_back=1)  # Test with 1 year
    
    get_data_info(spy_data, sector_data)
    
    print("Sample S&P 500 data (first 5 rows):")
    print(spy_data.head())
    
    print("\nSample Sector data (first 5 rows):")
    print(sector_data.head())

