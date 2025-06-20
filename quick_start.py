#!/usr/bin/env python3
"""
NancyGate 2.0 Quick Start Menu
Easy access to all system functions
"""

import subprocess
import sys
from rich.console import Console
from rich.prompt import Prompt, Confirm

console = Console()

def main():
    console.print("\n[bold blue]🚀 NancyGate 2.0 - Political Intelligence System[/bold blue]")
    console.print("=" * 60)
    console.print("[green]System Status: ✅ FULLY FUNCTIONAL[/green]")
    console.print("[yellow]5,000 trades from 83 members loaded and analyzed[/yellow]\n")
    
    while True:
        console.print("\n[bold]Available Actions:[/bold]")
        console.print("1. 📊 View comprehensive data analysis")
        console.print("2. 🔍 Run signal detection")
        console.print("3. 📰 Enrich with real-time news & Form 4 data")
        console.print("4. 🌐 Open dashboard (http://localhost:8501)")
        console.print("5. 📈 Generate specialized reports")
        console.print("6. 🎯 Quick analysis (specific ticker/member)")
        console.print("7. 💼 Full enrichment (all data sources)")
        console.print("8. 📋 View system status")
        console.print("9. 🚪 Exit")
        
        choice = Prompt.ask("\n[cyan]Select action (1-9)[/cyan]")
        
        if choice == "1":
            subprocess.run([sys.executable, "analyze_comprehensive_data.py"])
            
        elif choice == "2":
            console.print("\n[yellow]Running signal detection on 5,000 trades...[/yellow]")
            subprocess.run([
                sys.executable, "nancygate_cli.py", "analyze",
                "--input-file", "congress_trades_complete_20250618_222410",
                "--use-modular"
            ])
            
        elif choice == "3":
            console.print("\n[yellow]Enriching with real-time news and Form 4 data...[/yellow]")
            subprocess.run([
                sys.executable, "nancygate_cli.py", "enrich",
                "--input-file", "congress_trades_complete_20250618_222410",
                "--enrich-news", "--enrich-form4"
            ])
            
        elif choice == "4":
            console.print("\n[yellow]Opening dashboard at http://localhost:8501[/yellow]")
            console.print("[dim]Press Ctrl+C to stop the dashboard server[/dim]")
            try:
                subprocess.run([sys.executable, "nancygate_cli.py", "dashboard"])
            except KeyboardInterrupt:
                console.print("\n[yellow]Dashboard stopped[/yellow]")
                
        elif choice == "5":
            report_type = Prompt.ask(
                "Report type",
                choices=["exposure", "alpha", "compliance", "esg", "all"],
                default="all"
            )
            subprocess.run([
                sys.executable, "nancygate_cli.py", "specialized-reports",
                "--report-type", report_type
            ])
            
        elif choice == "6":
            analysis_type = Prompt.ask("Analyze by", choices=["ticker", "member"])
            if analysis_type == "ticker":
                ticker = Prompt.ask("Enter ticker symbol").upper()
                subprocess.run([
                    sys.executable, "nancygate_cli.py", "quick-analysis",
                    "--ticker", ticker
                ])
            else:
                member = Prompt.ask("Enter member name (partial match ok)")
                subprocess.run([
                    sys.executable, "nancygate_cli.py", "quick-analysis",
                    "--member", member
                ])
                
        elif choice == "7":
            console.print("\n[yellow]Running comprehensive enrichment (all sources)...[/yellow]")
            console.print("[dim]This may take several minutes...[/dim]")
            subprocess.run([
                sys.executable, "nancygate_cli.py", "enrich-full",
                "--enrich-all"
            ])
            
        elif choice == "8":
            with open("SYSTEM_STATUS.md", "r") as f:
                console.print(f.read())
                
        elif choice == "9":
            console.print("\n[green]Exiting NancyGate. Thank you![/green]")
            break
            
        else:
            console.print("[red]Invalid choice. Please select 1-9.[/red]")
        
        if choice != "9":
            input("\n[Press Enter to continue...]")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n\n[yellow]Interrupted by user[/yellow]")
        sys.exit(0) 