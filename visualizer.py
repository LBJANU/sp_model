"""
Visualization Module for S&P 500 Sector Analysis

This module handles plotting deviation returns and other visualizations.
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from typing import Optional
import numpy as np


def plot_deviation_returns(
    deviation_returns: pd.DataFrame,
    save_path: Optional[str] = 'sector_deviations.png',
    figsize: tuple = (16, 10)
) -> None:
    """
    Plot deviation returns over time for all sectors.
    
    Args:
        deviation_returns: DataFrame with deviation returns (sector - S&P 500)
        save_path: Path to save the plot (None to not save)
        figsize: Figure size (width, height) in inches
    """
    plt.figure(figsize=figsize)
    
    # Define colors for each sector (distinct colors)
    colors = plt.cm.tab20(np.linspace(0, 1, len(deviation_returns.columns)))
    
    # Plot each sector
    for i, sector in enumerate(deviation_returns.columns):
        plt.plot(
            deviation_returns.index,
            deviation_returns[sector] * 100,  # Convert to percentage
            label=sector,
            alpha=0.7,
            linewidth=1.5,
            color=colors[i]
        )
    
    # Add zero reference line
    plt.axhline(y=0, color='black', linestyle='--', linewidth=1, alpha=0.5, zorder=0)
    
    # Formatting
    plt.title(
        'S&P Sector Deviation Returns vs S&P 500 Over Time',
        fontsize=16,
        fontweight='bold',
        pad=20
    )
    plt.xlabel('Date', fontsize=12)
    plt.ylabel('Deviation Returns (%)', fontsize=12)
    
    # Format x-axis dates
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    plt.gca().xaxis.set_major_locator(mdates.MonthLocator(interval=3))
    plt.xticks(rotation=45)
    
    # Legend
    plt.legend(
        loc='upper left',
        ncol=2,
        fontsize=9,
        framealpha=0.9
    )
    
    # Grid
    plt.grid(True, alpha=0.3, linestyle='--')
    
    # Tight layout
    plt.tight_layout()
    
    # Save if path provided
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"✓ Plot saved to {save_path}")
    
    plt.show()


def plot_cumulative_deviations(
    deviation_returns: pd.DataFrame,
    save_path: Optional[str] = 'cumulative_deviations.png',
    figsize: tuple = (16, 10)
) -> None:
    """
    Plot cumulative deviation returns over time.
    
    Shows the running total of how much each sector has outperformed/underperformed.
    
    Args:
        deviation_returns: DataFrame with deviation returns
        save_path: Path to save the plot (None to not save)
        figsize: Figure size (width, height) in inches
    """
    plt.figure(figsize=figsize)
    
    # Calculate cumulative sum
    cumulative_deviations = deviation_returns.cumsum() * 100  # Convert to percentage
    
    # Define colors for each sector
    colors = plt.cm.tab20(np.linspace(0, 1, len(cumulative_deviations.columns)))
    
    # Plot each sector
    for i, sector in enumerate(cumulative_deviations.columns):
        plt.plot(
            cumulative_deviations.index,
            cumulative_deviations[sector],
            label=sector,
            alpha=0.7,
            linewidth=2,
            color=colors[i]
        )
    
    # Add zero reference line
    plt.axhline(y=0, color='black', linestyle='--', linewidth=1, alpha=0.5, zorder=0)
    
    # Formatting
    plt.title(
        'Cumulative Deviation Returns: Sectors vs S&P 500',
        fontsize=16,
        fontweight='bold',
        pad=20
    )
    plt.xlabel('Date', fontsize=12)
    plt.ylabel('Cumulative Deviation Returns (%)', fontsize=12)
    
    # Format x-axis dates
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    plt.gca().xaxis.set_major_locator(mdates.MonthLocator(interval=3))
    plt.xticks(rotation=45)
    
    # Legend
    plt.legend(
        loc='upper left',
        ncol=2,
        fontsize=9,
        framealpha=0.9
    )
    
    # Grid
    plt.grid(True, alpha=0.3, linestyle='--')
    
    # Tight layout
    plt.tight_layout()
    
    # Save if path provided
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"✓ Plot saved to {save_path}")
    
    plt.show()


def plot_sector_subplots(
    deviation_returns: pd.DataFrame,
    save_path: Optional[str] = 'sector_subplots.png',
    figsize: tuple = (20, 12)
) -> None:
    """
    Plot individual subplots for each sector.
    
    Args:
        deviation_returns: DataFrame with deviation returns
        save_path: Path to save the plot (None to not save)
        figsize: Figure size (width, height) in inches
    """
    n_sectors = len(deviation_returns.columns)
    n_cols = 3
    n_rows = (n_sectors + n_cols - 1) // n_cols  # Ceiling division
    
    fig, axes = plt.subplots(n_rows, n_cols, figsize=figsize)
    axes = axes.flatten() if n_sectors > 1 else [axes]
    
    # Define colors
    colors = plt.cm.tab20(np.linspace(0, 1, n_sectors))
    
    for i, sector in enumerate(deviation_returns.columns):
        ax = axes[i]
        
        # Plot this sector
        ax.plot(
            deviation_returns.index,
            deviation_returns[sector] * 100,  # Convert to percentage
            color=colors[i],
            linewidth=1.5,
            alpha=0.8
        )
        
        # Add zero line
        ax.axhline(y=0, color='black', linestyle='--', linewidth=0.8, alpha=0.5)
        
        # Formatting
        ax.set_title(sector, fontsize=11, fontweight='bold')
        ax.set_ylabel('Deviation (%)', fontsize=9)
        ax.grid(True, alpha=0.3)
        
        # Format x-axis
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
        ax.xaxis.set_major_locator(mdates.MonthLocator(interval=6))
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right')
    
    # Hide extra subplots
    for i in range(n_sectors, len(axes)):
        axes[i].set_visible(False)
    
    # Overall title
    fig.suptitle(
        'Deviation Returns by Sector (Individual Views)',
        fontsize=16,
        fontweight='bold',
        y=0.995
    )
    
    plt.tight_layout(rect=[0, 0, 1, 0.98])
    
    # Save if path provided
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"✓ Plot saved to {save_path}")
    
    plt.show()


if __name__ == "__main__":
    # Test the visualization module with sample data
    print("Testing Visualization Module")
    print("="*60)
    
    # Create sample deviation returns data
    dates = pd.date_range('2023-01-01', periods=100, freq='D')
    np.random.seed(42)
    
    sample_deviations = pd.DataFrame({
        'Technology': np.random.normal(0.1, 1.5, 100) / 100,
        'Healthcare': np.random.normal(0.05, 1.2, 100) / 100,
        'Financials': np.random.normal(-0.05, 1.8, 100) / 100,
    }, index=dates)
    
    print("\nCreating test plots...")
    plot_deviation_returns(sample_deviations, save_path=None)
    print("Test complete!")

