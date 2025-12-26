"""
S&P 500 Sector Deviation Analysis - Main Entry Point

This is the main script that will orchestrate the analysis.
Currently in development - starting with data fetching.
"""

import pandas as pd
from data_fetcher import fetch_all_data, get_data_info, inspect_sector_data
from returns_calculator import (
    calculate_returns,
    calculate_deviation_returns,
    clean_returns_data,
    get_returns_summary
)
from visualizer import (
    plot_deviation_returns,
    plot_cumulative_deviations,
    plot_sector_subplots
)


def main():
    """
    Main function - will be built out step by step.
    """
    print("S&P 500 Sector Deviation Analysis")
    print("="*60)
    
    # Phase 1: Data Fetching
    print("\n[Phase 1] Fetching data...")
    spy_prices, sector_prices = fetch_all_data(years_back=16)
    
    # Display data info
    get_data_info(spy_prices, sector_prices)
    
    # Inspect data types and structure
    inspect_sector_data(spy_prices, sector_prices)
    
    # Phase 2: Returns Calculation
    print("\n[Phase 2] Calculating returns...")
    
    # Convert prices to returns
    spy_returns = calculate_returns(spy_prices)
    sector_returns = calculate_returns(sector_prices)
    
    # Clean NaN values (from first day)
    spy_returns = clean_returns_data(spy_returns)
    sector_returns = clean_returns_data(sector_returns)
    
    # Calculate deviation returns (sector returns - S&P returns)
    deviation_returns = calculate_deviation_returns(sector_returns, spy_returns)
    
    # Display returns summary
    get_returns_summary(spy_returns, sector_returns, deviation_returns)
    
    print("Phase 2 complete! Returns and deviation returns calculated.")
    
    # Phase 3: Visualization
    print("\n[Phase 3] Creating visualizations...")
    
    # Plot deviation returns over time
    plot_deviation_returns(deviation_returns)
    
    # Plot cumulative deviations
    plot_cumulative_deviations(deviation_returns)
    
    # Plot individual sector subplots
    plot_sector_subplots(deviation_returns)
    
    print("\nPhase 3 complete! All visualizations created.")


if __name__ == "__main__":
    main()
