#!/usr/bin/env python3

import sys
import update_portfolio
import generate_summary

def run_production_pipeline():
    """Execute the complete production pipeline"""
    
    print("\n--- Starting Production Pipeline ---\n", file=sys.stderr)
    
    # Step 1: ETL - Update Portfolio
    print("Step 1: Updating portfolio...", file=sys.stderr)
    update_portfolio.main()
    
    # Step 2: Reporting - Generate Summary
    print("\nStep 2: Generating summary report...", file=sys.stderr)
    generate_summary.main()
    
    print("\n--- Production Pipeline Complete ---\n", file=sys.stderr)

if __name__ == "__main__":
    run_production_pipeline()