"""
Visualization Module for S&P 500 Sector Analysis

This module handles plotting deviation returns and other visualizations.
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from typing import Optional
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px


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


# ============================================================================
# PLOTLY VERSIONS (Interactive HTML Export)
# ============================================================================

def plot_deviation_returns_plotly(
    deviation_returns: pd.DataFrame,
    save_path: Optional[str] = 'sector_deviations.html',
    figsize: tuple = (1400, 800)
) -> go.Figure:
    """
    Plot deviation returns over time for all sectors using Plotly (interactive).
    
    Args:
        deviation_returns: DataFrame with deviation returns (sector - S&P 500)
        save_path: Path to save the HTML file (None to not save)
        figsize: Figure size (width, height) in pixels
    
    Returns:
        Plotly Figure object
    """
    fig = go.Figure()
    
    # Define colors for each sector
    colors = px.colors.qualitative.Set3 + px.colors.qualitative.Pastel
    
    # Plot each sector
    for i, sector in enumerate(deviation_returns.columns):
        fig.add_trace(go.Scatter(
            x=deviation_returns.index,
            y=deviation_returns[sector] * 100,  # Convert to percentage
            mode='lines',
            name=sector,
            line=dict(width=2, color=colors[i % len(colors)]),
            hovertemplate=f'<b>{sector}</b><br>' +
                         'Date: %{x}<br>' +
                         'Deviation: %{y:.2f}%<extra></extra>'
        ))
    
    # Add zero reference line
    fig.add_hline(
        y=0,
        line_dash="dash",
        line_color="black",
        opacity=0.5,
        annotation_text="S&P 500 Reference"
    )
    
    # Update layout
    fig.update_layout(
        title={
            'text': 'S&P Sector Deviation Returns vs S&P 500 Over Time',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 20, 'family': 'Arial Black'}
        },
        xaxis_title='Date',
        yaxis_title='Deviation Returns (%)',
        hovermode='x unified',
        width=figsize[0],
        height=figsize[1],
        legend=dict(
            orientation="v",
            yanchor="top",
            y=1,
            xanchor="left",
            x=1.01
        ),
        template='plotly_white',
        xaxis=dict(
            showgrid=True,
            gridwidth=1,
            gridcolor='lightgray'
        ),
        yaxis=dict(
            showgrid=True,
            gridwidth=1,
            gridcolor='lightgray'
        )
    )
    
    # Save if path provided
    if save_path:
        fig.write_html(save_path)
        print(f"✓ Interactive plot saved to {save_path}")
    
    return fig


def plot_cumulative_deviations_plotly(
    deviation_returns: pd.DataFrame,
    save_path: Optional[str] = 'cumulative_deviations.html',
    figsize: tuple = (1400, 800)
) -> go.Figure:
    """
    Plot cumulative deviation returns over time using Plotly (interactive).
    
    Args:
        deviation_returns: DataFrame with deviation returns
        save_path: Path to save the HTML file (None to not save)
        figsize: Figure size (width, height) in pixels
    
    Returns:
        Plotly Figure object
    """
    # Calculate cumulative sum
    cumulative_deviations = deviation_returns.cumsum() * 100  # Convert to percentage
    
    fig = go.Figure()
    
    # Define colors
    colors = px.colors.qualitative.Set3 + px.colors.qualitative.Pastel
    
    # Plot each sector
    for i, sector in enumerate(cumulative_deviations.columns):
        fig.add_trace(go.Scatter(
            x=cumulative_deviations.index,
            y=cumulative_deviations[sector],
            mode='lines',
            name=sector,
            line=dict(width=2.5, color=colors[i % len(colors)]),
            hovertemplate=f'<b>{sector}</b><br>' +
                         'Date: %{x}<br>' +
                         'Cumulative Deviation: %{y:.2f}%<extra></extra>'
        ))
    
    # Add zero reference line
    fig.add_hline(
        y=0,
        line_dash="dash",
        line_color="black",
        opacity=0.5,
        annotation_text="S&P 500 Reference"
    )
    
    # Update layout
    fig.update_layout(
        title={
            'text': 'Cumulative Deviation Returns: Sectors vs S&P 500',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 20, 'family': 'Arial Black'}
        },
        xaxis_title='Date',
        yaxis_title='Cumulative Deviation Returns (%)',
        hovermode='x unified',
        width=figsize[0],
        height=figsize[1],
        legend=dict(
            orientation="v",
            yanchor="top",
            y=1,
            xanchor="left",
            x=1.01
        ),
        template='plotly_white',
        xaxis=dict(
            showgrid=True,
            gridwidth=1,
            gridcolor='lightgray'
        ),
        yaxis=dict(
            showgrid=True,
            gridwidth=1,
            gridcolor='lightgray'
        )
    )
    
    # Save if path provided
    if save_path:
        fig.write_html(save_path)
        print(f"✓ Interactive plot saved to {save_path}")
    
    return fig


def plot_sector_subplots_plotly(
    deviation_returns: pd.DataFrame,
    save_path: Optional[str] = 'sector_subplots.html',
    figsize: tuple = (1800, 1200)
) -> go.Figure:
    """
    Plot individual subplots for each sector using Plotly (interactive).
    
    Args:
        deviation_returns: DataFrame with deviation returns
        save_path: Path to save the HTML file (None to not save)
        figsize: Figure size (width, height) in pixels
    
    Returns:
        Plotly Figure object
    """
    n_sectors = len(deviation_returns.columns)
    n_cols = 3
    n_rows = (n_sectors + n_cols - 1) // n_cols  # Ceiling division
    
    # Create subplots
    fig = make_subplots(
        rows=n_rows,
        cols=n_cols,
        subplot_titles=list(deviation_returns.columns),
        vertical_spacing=0.08,
        horizontal_spacing=0.1
    )
    
    # Define colors
    colors = px.colors.qualitative.Set3 + px.colors.qualitative.Pastel
    
    # Plot each sector
    for i, sector in enumerate(deviation_returns.columns):
        row = (i // n_cols) + 1
        col = (i % n_cols) + 1
        
        fig.add_trace(
            go.Scatter(
                x=deviation_returns.index,
                y=deviation_returns[sector] * 100,  # Convert to percentage
                mode='lines',
                name=sector,
                line=dict(width=2, color=colors[i % len(colors)]),
                showlegend=False,
                hovertemplate=f'<b>{sector}</b><br>' +
                             'Date: %{x}<br>' +
                             'Deviation: %{y:.2f}%<extra></extra>'
            ),
            row=row,
            col=col
        )
        
        # Add zero line to each subplot
        fig.add_hline(
            y=0,
            line_dash="dash",
            line_color="black",
            opacity=0.3,
            row=row,
            col=col
        )
    
    # Update layout
    fig.update_layout(
        title={
            'text': 'Deviation Returns by Sector (Individual Views)',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 20, 'family': 'Arial Black'},
            'y': 0.98
        },
        height=figsize[1],
        width=figsize[0],
        template='plotly_white',
        showlegend=False
    )
    
    # Update x and y axis labels
    for i in range(1, n_rows + 1):
        for j in range(1, n_cols + 1):
            fig.update_xaxes(
                title_text="Date" if i == n_rows else "",
                showgrid=True,
                gridwidth=1,
                gridcolor='lightgray',
                row=i,
                col=j
            )
            fig.update_yaxes(
                title_text="Deviation (%)" if j == 1 else "",
                showgrid=True,
                gridwidth=1,
                gridcolor='lightgray',
                row=i,
                col=j
            )
    
    # Save if path provided
    if save_path:
        fig.write_html(save_path)
        print(f"✓ Interactive plot saved to {save_path}")
    
    return fig


def plot_moving_average_plotly_50day(
    deviation_returns: pd.DataFrame,
    window: int = 50,
    save_path: Optional[str] = 'moving_average_50day.html',
    figsize: tuple = (1400, 800)
) -> go.Figure:
    """
    Plot 50-day moving average of deviation returns for all sectors using Plotly.
    
    Args:
        deviation_returns: DataFrame with deviation returns (sector - S&P 500)
        window: Number of days for moving average (default: 50)
        save_path: Path to save the HTML file (None to not save)
        figsize: Figure size (width, height) in pixels
    
    Returns:
        Plotly Figure object
    """
    # Calculate moving average
    moving_avg = deviation_returns.rolling(window=window).mean()
    
    # Drop NaN values (from first 'window' days)
    moving_avg = moving_avg.dropna()
    
    if moving_avg.empty:
        print(f"⚠ Warning: Moving average is empty. Need at least {window} days of data.")
        return go.Figure()
    
    fig = go.Figure()
    
    # Define colors for each sector
    colors = px.colors.qualitative.Set3 + px.colors.qualitative.Pastel
    
    # Plot each sector's moving average
    for i, sector in enumerate(moving_avg.columns):
        fig.add_trace(go.Scatter(
            x=moving_avg.index,
            y=moving_avg[sector] * 100,  # Convert to percentage
            mode='lines',
            name=sector,
            line=dict(width=3, color=colors[i % len(colors)]),
            hovertemplate=f'<b>{sector}</b><br>' +
                         'Date: %{x}<br>' +
                         f'{window}-Day MA: %{{y:.2f}}%<extra></extra>'
        ))
    
    # Add zero reference line
    fig.add_hline(
        y=0,
        line_dash="dash",
        line_color="black",
        opacity=0.5,
        annotation_text="S&P 500 Reference"
    )
    
    # Update layout
    fig.update_layout(
        title={
            'text': f'S&P Sector Deviation Returns - {window}-Day Moving Average',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 20, 'family': 'Arial Black'}
        },
        xaxis_title='Date',
        yaxis_title=f'Deviation Returns - {window}-Day MA (%)',
        hovermode='x unified',
        width=figsize[0],
        height=figsize[1],
        legend=dict(
            orientation="v",
            yanchor="top",
            y=1,
            xanchor="left",
            x=1.01
        ),
        template='plotly_white',
        xaxis=dict(
            showgrid=True,
            gridwidth=1,
            gridcolor='lightgray'
        ),
        yaxis=dict(
            showgrid=True,
            gridwidth=1,
            gridcolor='lightgray'
        )
    )
    
    # Save if path provided
    if save_path:
        fig.write_html(save_path)
        print(f"✓ Interactive moving average plot saved to {save_path}")
    
    return fig

def plot_moving_average_plotly_100day(
    deviation_returns: pd.DataFrame,
    window: int = 100,
    save_path: Optional[str] = 'moving_average_100day.html',
    figsize: tuple = (1400, 800)
) -> go.Figure:
    """
    Plot 100-day moving average of deviation returns for all sectors using Plotly.
    
    Args:
        deviation_returns: DataFrame with deviation returns (sector - S&P 500)
        window: Number of days for moving average (default: 100)
        save_path: Path to save the HTML file (None to not save)
        figsize: Figure size (width, height) in pixels
    
    Returns:
        Plotly Figure object
    """
    # Calculate moving average
    moving_avg = deviation_returns.rolling(window=window).mean()
    
    # Drop NaN values (from first 'window' days)
    moving_avg = moving_avg.dropna()
    
    if moving_avg.empty:
        print(f"⚠ Warning: Moving average is empty. Need at least {window} days of data.")
        return go.Figure()
    
    fig = go.Figure()
    
    # Define colors for each sector
    colors = px.colors.qualitative.Set3 + px.colors.qualitative.Pastel
    
    # Plot each sector's moving average
    for i, sector in enumerate(moving_avg.columns):
        fig.add_trace(go.Scatter(
            x=moving_avg.index,
            y=moving_avg[sector] * 100,  # Convert to percentage
            mode='lines',
            name=sector,
            line=dict(width=3, color=colors[i % len(colors)]),
            hovertemplate=f'<b>{sector}</b><br>' +
                         'Date: %{x}<br>' +
                         f'{window}-Day MA: %{{y:.2f}}%<extra></extra>'
        ))
    
    # Add zero reference line
    fig.add_hline(
        y=0,
        line_dash="dash",
        line_color="black",
        opacity=0.5,
        annotation_text="S&P 500 Reference"
    )
    
    # Update layout
    fig.update_layout(
        title={
            'text': f'S&P Sector Deviation Returns - {window}-Day Moving Average',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 20, 'family': 'Arial Black'}
        },
        xaxis_title='Date',
        yaxis_title=f'Deviation Returns - {window}-Day MA (%)',
        hovermode='x unified',
        width=figsize[0],
        height=figsize[1],
        legend=dict(
            orientation="v",
            yanchor="top",
            y=1,
            xanchor="left",
            x=1.01
        ),
        template='plotly_white',
        xaxis=dict(
            showgrid=True,
            gridwidth=1,
            gridcolor='lightgray'
        ),
        yaxis=dict(
            showgrid=True,
            gridwidth=1,
            gridcolor='lightgray'
        )
    )
    
    # Save if path provided
    if save_path:
        fig.write_html(save_path)
        print(f"✓ Interactive moving average plot saved to {save_path}")
    
    return fig

def plot_moving_average_plotly_170day(
    deviation_returns: pd.DataFrame,
    window: int = 170,
    save_path: Optional[str] = 'moving_average_170day.html',
    figsize: tuple = (1400, 800)
) -> go.Figure:
    """
    Plot 170-day moving average of deviation returns for all sectors using Plotly.
    
    Args:
        deviation_returns: DataFrame with deviation returns (sector - S&P 500)
        window: Number of days for moving average (default: 170)
        save_path: Path to save the HTML file (None to not save)
        figsize: Figure size (width, height) in pixels
    
    Returns:
        Plotly Figure object
    """
    # Calculate moving average
    moving_avg = deviation_returns.rolling(window=window).mean()
    
    # Drop NaN values (from first 'window' days)
    moving_avg = moving_avg.dropna()
    
    if moving_avg.empty:
        print(f"⚠ Warning: Moving average is empty. Need at least {window} days of data.")
        return go.Figure()
    
    fig = go.Figure()
    
    # Define colors for each sector
    colors = px.colors.qualitative.Set3 + px.colors.qualitative.Pastel
    
    # Plot each sector's moving average
    for i, sector in enumerate(moving_avg.columns):
        fig.add_trace(go.Scatter(
            x=moving_avg.index,
            y=moving_avg[sector] * 100,  # Convert to percentage
            mode='lines',
            name=sector,
            line=dict(width=3, color=colors[i % len(colors)]),
            hovertemplate=f'<b>{sector}</b><br>' +
                         'Date: %{x}<br>' +
                         f'{window}-Day MA: %{{y:.2f}}%<extra></extra>'
        ))
    
    # Add zero reference line
    fig.add_hline(
        y=0,
        line_dash="dash",
        line_color="black",
        opacity=0.5,
        annotation_text="S&P 500 Reference"
    )
    
    # Update layout
    fig.update_layout(
        title={
            'text': f'S&P Sector Deviation Returns - {window}-Day Moving Average',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 20, 'family': 'Arial Black'}
        },
        xaxis_title='Date',
        yaxis_title=f'Deviation Returns - {window}-Day MA (%)',
        hovermode='x unified',
        width=figsize[0],
        height=figsize[1],
        legend=dict(
            orientation="v",
            yanchor="top",
            y=1,
            xanchor="left",
            x=1.01
        ),
        template='plotly_white',
        xaxis=dict(
            showgrid=True,
            gridwidth=1,
            gridcolor='lightgray'
        ),
        yaxis=dict(
            showgrid=True,
            gridwidth=1,
            gridcolor='lightgray'
        )
    )
    
    # Save if path provided
    if save_path:
        fig.write_html(save_path)
        print(f"✓ Interactive moving average plot saved to {save_path}")
    
    return fig

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

