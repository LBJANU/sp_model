"""
Returns Calculation Module for S&P 500 Sector Analysis

This module handles:
- Calculating daily returns from prices
- Calculating deviation returns (sector returns - S&P 500 returns)
"""

import pandas as pd
import numpy as np
from typing import Tuple


def calculate_returns(prices: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate daily returns from price data.
    
    Formula: Return = (Price_today - Price_yesterday) / Price_yesterday
    Or equivalently: Return = Price_today / Price_yesterday - 1
    
    Args:
        prices: DataFrame or Series with price data (indexed by date)
    
    Returns:
        DataFrame or Series with daily returns (as decimals, e.g., 0.02 = 2%)
        First row will be NaN (no previous day to compare)
    """
    returns = prices.pct_change()
    return returns


def calculate_deviation_returns(
    sector_returns: pd.DataFrame, 
    spy_returns: pd.Series
) -> pd.DataFrame:
    """
    Calculate deviation returns: sector returns - S&P 500 returns.
    
    Positive deviation = sector outperformed S&P 500 that day
    Negative deviation = sector underperformed S&P 500 that day
    Zero deviation = sector matched S&P 500 that day
    
    Args:
        sector_returns: DataFrame with daily returns for each sector
        spy_returns: Series with daily returns for S&P 500
    
    Returns:
        DataFrame with deviation returns for each sector
    """
    # Align dates to ensure we're subtracting matching days
    common_dates = sector_returns.index.intersection(spy_returns.index)
    sector_returns_aligned = sector_returns.loc[common_dates]
    spy_returns_aligned = spy_returns.loc[common_dates]
    
    # Calculate deviation: sector return - S&P return
    deviation_returns = sector_returns_aligned.subtract(spy_returns_aligned, axis=0)
    
    return deviation_returns


def clean_returns_data(returns: pd.DataFrame) -> pd.DataFrame:
    """
    Remove rows with NaN values (typically the first row after pct_change).
    
    Args:
        returns: DataFrame with returns (may contain NaN values)
    
    Returns:
        DataFrame with NaN rows removed
    """
    cleaned = returns.dropna()
    return cleaned


def get_returns_summary(
    spy_returns: pd.Series,
    sector_returns: pd.DataFrame,
    deviation_returns: pd.DataFrame
) -> None:
    """
    Print summary statistics about the returns data.
    
    Args:
        spy_returns: S&P 500 returns
        sector_returns: Sector returns
        deviation_returns: Deviation returns
    """
    print("\n" + "="*60)
    print("RETURNS SUMMARY")
    print("="*60)
    
    # S&P 500 returns stats
    print(f"\nS&P 500 Returns:")
    print(f"  Total days: {len(spy_returns)}")
    print(f"  Mean daily return: {spy_returns.mean():.4%}")
    print(f"  Std deviation: {spy_returns.std():.4%}")
    print(f"  Min return: {spy_returns.min():.4%}")
    print(f"  Max return: {spy_returns.max():.4%}")
    
    # Sector returns stats
    print(f"\nSector Returns (mean daily return per sector):")
    for sector in sector_returns.columns:
        mean_ret = sector_returns[sector].mean()
        std_ret = sector_returns[sector].std()
        print(f"  {sector:30s}: {mean_ret:7.4%} (std: {std_ret:.4%})")
    
    # Deviation returns stats
    print(f"\nDeviation Returns (mean deviation per sector):")
    for sector in deviation_returns.columns:
        mean_dev = deviation_returns[sector].mean()
        std_dev = deviation_returns[sector].std()
        print(f"  {sector:30s}: {mean_dev:7.4%} (std: {std_dev:.4%})")
        if mean_dev > 0:
            print(f"    → On average, {sector} outperformed S&P 500")
        elif mean_dev < 0:
            print(f"    → On average, {sector} underperformed S&P 500")
        else:
            print(f"    → On average, {sector} matched S&P 500")
    
    print("="*60 + "\n")


if __name__ == "__main__":
    # Test the returns calculation module
    print("Testing Returns Calculation Module")
    print("="*60)
    
    # Create sample data for testing
    dates = pd.date_range('2023-01-01', periods=10, freq='D')
    sample_prices = pd.DataFrame({
        'Sector1': [100, 102, 101, 105, 103, 107, 106, 108, 110, 109],
        'Sector2': [50, 51, 50.5, 52, 51.5, 53, 52.5, 54, 55, 54.5],
        'SPY': [400, 402, 401, 405, 403, 407, 406, 408, 410, 409]
    }, index=dates)
    
    print("\nSample prices:")
    print(sample_prices)
    
    # Calculate returns
    print("\nCalculating returns...")
    returns = calculate_returns(sample_prices)
    print(returns)
    
    # Calculate deviation returns
    print("\nCalculating deviation returns...")
    spy_ret = returns['SPY']
    sector_ret = returns[['Sector1', 'Sector2']]
    deviation_ret = calculate_deviation_returns(sector_ret, spy_ret)
    print(deviation_ret)
    
    print("\nTest complete!")

