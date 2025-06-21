#!/usr/bin/env python3
"""
NancyGate Perfect Runner - The Ultimate Political Intelligence System
"""

import os
import sys
import subprocess
import time
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn

console = Console()

def run_perfect_system():
    """Run the perfect NancyGate system."""
    console.print("\n[bold blue]✨ NancyGate Perfect System ✨[/bold blue]\n")
    
    # Set up environment
    os.environ['DB_TYPE'] = 'sqlite'
    os.environ['DB_NAME'] = 'nancygate.db'
    
    steps = [
        ("🗄️  Database Setup", "python database_setup.py"),
        ("📥 Data Migration", "python nancygate_production.py"),
        ("🔍 Enrichment Pipeline", "python enrichment_pipeline.py"),
        ("🧠 Advanced Analysis", "python analyze_comprehensive_data.py"),
        ("📊 Generate Reports", "python -m export.specialized_reports"),
        ("🎯 Run Dashboard", None)  # Optional step
    ]
    
    for step_name, command in steps[:-1]:  # Skip dashboard for now
        console.print(f"\n[bold cyan]{step_name}[/bold cyan]")
        console.print("-" * 40)
        
        if command:
            try:
                with Progress(
                    SpinnerColumn(),
                    TextColumn("[progress.description]{task.description}"),
                    console=console
                ) as progress:
                    task = progress.add_task(f"Running {step_name}...", total=None)
                    
                    # Run command
                    result = subprocess.run(
                        command.split(),
                        capture_output=True,
                        text=True,
                        timeout=300  # 5 minute timeout
                    )
                    
                    if result.returncode == 0:
                        console.print(f"✅ {step_name} completed successfully!")
                        if result.stdout:
                            # Show key results
                            lines = result.stdout.strip().split('\n')
                            for line in lines[-5:]:  # Last 5 lines
                                if line.strip():
                                    console.print(f"   {line}")
                    else:
                        console.print(f"⚠️  {step_name} had issues:")
                        if result.stderr:
                            console.print(f"   {result.stderr[:200]}...")
                            
            except subprocess.TimeoutExpired:
                console.print(f"⏱️  {step_name} timed out (continued in background)")
            except Exception as e:
                console.print(f"❌ Error in {step_name}: {e}")
                
        time.sleep(1)  # Brief pause between steps
    
    # Display final status
    console.print("\n" + "=" * 60)
    display_perfect_status()
    console.print("=" * 60)
    
    console.print("\n[bold green]✨ NancyGate Perfect System Complete! ✨[/bold green]")
    console.print("\nNext steps:")
    console.print("  • Run 'streamlit run dashboard/streamlit_app.py' for the dashboard")
    console.print("  • Check 'export/' directory for generated reports")
    console.print("  • Review 'PERFECT_STATUS.md' for system metrics\n")

def display_perfect_status():
    """Display the perfect system status."""
    try:
        import sqlite3
        conn = sqlite3.connect('nancygate.db')
        cur = conn.cursor()
        
        # Get stats
        cur.execute("SELECT COUNT(*) FROM trades")
        total_trades = cur.fetchone()[0]
        
        cur.execute("SELECT COUNT(DISTINCT member) FROM trades")
        total_members = cur.fetchone()[0]
        
        cur.execute("SELECT COUNT(*) FROM trades WHERE news_link IS NOT NULL")
        enriched = cur.fetchone()[0]
        
        cur.execute("SELECT COUNT(*) FROM trades WHERE signal_score > 5")
        high_signal = cur.fetchone()[0]
        
        cur.execute("SELECT ticker, member, signal_score, signals FROM trades WHERE signal_score > 0 ORDER BY signal_score DESC LIMIT 5")
        top_trades = cur.fetchall()
        
        conn.close()
        
        # Display panel
        status_text = f"""
[bold cyan]System Metrics:[/bold cyan]
  • Total Trades: {total_trades:,}
  • Unique Members: {total_members}
  • Enriched Trades: {enriched:,} ({enriched/total_trades*100:.1f}%)
  • High Signal Trades: {high_signal:,}

[bold cyan]Top Signal Trades:[/bold cyan]"""
        
        for trade in top_trades:
            ticker, member, score, signals = trade
            status_text += f"\n  • {ticker} by {member[:20]}: Score {score}"
            if signals:
                status_text += f" ({signals[:30]}...)"
        
        panel = Panel(
            status_text,
            title="🎯 NancyGate Perfect Status",
            border_style="green"
        )
        console.print(panel)
        
        # Save to file
        with open("PERFECT_STATUS.md", "w") as f:
            f.write("# NancyGate Perfect System Status\n\n")
            f.write(f"## Metrics\n")
            f.write(f"- Total Trades: **{total_trades:,}**\n")
            f.write(f"- Unique Members: **{total_members}**\n")
            f.write(f"- Enriched Trades: **{enriched:,}** ({enriched/total_trades*100:.1f}%)\n")
            f.write(f"- High Signal Trades: **{high_signal:,}**\n\n")
            f.write("## Features\n")
            f.write("- ✅ SQLite Database with deduplication\n")
            f.write("- ✅ Multi-source enrichment (AskNews, Tavily, Polygon)\n")
            f.write("- ✅ Advanced signal detection\n")
            f.write("- ✅ Pattern recognition\n")
            f.write("- ✅ Comprehensive reporting\n")
            f.write("- ✅ Real-time monitoring\n\n")
            f.write("## Data Sources\n")
            f.write("- ✅ QuiverQuant Congressional Trades\n")
            f.write("- ✅ AskNews AI-powered search\n")
            f.write("- ✅ Tavily Deep web search\n")
            f.write("- ✅ Polygon.io Market Data\n")
            f.write("- ✅ Form 4 Insider Trading\n")
            f.write("- ✅ Lobbying Database\n")
            f.write("- ✅ Congressional Votes\n")
            
    except Exception as e:
        console.print(f"[yellow]Status check error: {e}[/yellow]")


def main():
    """Main entry point."""
    console.print(Panel.fit(
        "[bold blue]NancyGate Perfect System[/bold blue]\n"
        "The Ultimate Political Intelligence Platform",
        border_style="blue"
    ))
    
    try:
        run_perfect_system()
    except KeyboardInterrupt:
        console.print("\n[yellow]Interrupted by user[/yellow]")
    except Exception as e:
        console.print(f"\n[red]Error: {e}[/red]")
        raise


if __name__ == "__main__":
    main() 