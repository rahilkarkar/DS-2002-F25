#!/usr/bin/env python3

import pandas as pd
import json
import os
import sys

def _load_lookup_data(lookup_dir):
    """Load and process JSON card data from lookup directory"""
    all_lookup_df = []
    
    for filename in os.listdir(lookup_dir):
        if filename.endswith('.json'):
            filepath = os.path.join(lookup_dir, filename)
            
            with open(filepath, 'r') as f:
                data = json.load(f)
            
            df = pd.json_normalize(data['data'])
            
            # Price calculation - prioritize holofoil, then normal, then 0
            # Handle cases where columns might not exist
            holofoil_price = df.get('tcgplayer.prices.holofoil.market', pd.Series([None] * len(df)))
            normal_price = df.get('tcgplayer.prices.normal.market', pd.Series([None] * len(df)))
            
            df['card_market_value'] = holofoil_price.fillna(normal_price).fillna(0.0)
            
            # Rename columns
            df = df.rename(columns={
                'id': 'card_id',
                'name': 'card_name',
                'number': 'card_number',
                'set.id': 'set_id',
                'set.name': 'set_name'
            })
            
            # Keep only required columns
            required_cols = ['card_id', 'card_name', 'card_number', 'set_id', 'set_name', 'card_market_value']
            all_lookup_df.append(df[required_cols].copy())
    
    # Concatenate all dataframes
    if not all_lookup_df:
        return pd.DataFrame(columns=['card_id', 'card_name', 'card_number', 'set_id', 'set_name', 'card_market_value'])
    
    lookup_df = pd.concat(all_lookup_df, ignore_index=True)
    
    # Remove duplicates, keeping the first (after sorting by value)
    lookup_df = lookup_df.sort_values('card_market_value', ascending=False)
    lookup_df = lookup_df.drop_duplicates(subset=['card_id'], keep='first')
    
    return lookup_df

def _load_inventory_data(inventory_dir):
    """Load CSV inventory data and create unified card_id"""
    inventory_data = []
    
    for filename in os.listdir(inventory_dir):
        if filename.endswith('.csv'):
            filepath = os.path.join(inventory_dir, filename)
            df = pd.read_csv(filepath)
            inventory_data.append(df)
    
    if not inventory_data:
        return pd.DataFrame()
    
    inventory_df = pd.concat(inventory_data, ignore_index=True)
    
    # Create unified card_id key
    inventory_df['card_id'] = (inventory_df['set_id'].astype(str) + '-' + 
                                inventory_df['card_number'].astype(str))
    
    return inventory_df

def update_portfolio(inventory_dir, lookup_dir, output_file):
    """Main ETL orchestration function"""
    # Load data from both sources
    lookup_df = _load_lookup_data(lookup_dir)
    inventory_df = _load_inventory_data(inventory_dir)
    
    # Handle empty inventory
    if inventory_df.empty:
        print("Error: No inventory data found.", file=sys.stderr)
        # Create empty portfolio with headers
        pd.DataFrame(columns=['index', 'card_name', 'set_name', 'card_id', 
                             'binder_name', 'page_number', 'slot_number', 
                             'card_market_value']).to_csv(output_file, index=False)
        return
    
    # Merge inventory with lookup data
    portfolio_df = pd.merge(
        inventory_df,
        lookup_df[['card_id', 'card_name', 'set_name', 'card_market_value']],
        on='card_id',
        how='left',
        suffixes=('_inventory', '_lookup')
    )
    
    # Fill missing values and handle duplicate columns
    portfolio_df['card_market_value'] = portfolio_df['card_market_value'].fillna(0.0)
    portfolio_df['set_name'] = portfolio_df['set_name'].fillna('NOT_FOUND')
    
    # Use the lookup card_name (from API) if available, otherwise use inventory
    if 'card_name_lookup' in portfolio_df.columns:
        portfolio_df['card_name'] = portfolio_df['card_name_lookup'].fillna(portfolio_df['card_name_inventory'])
        portfolio_df = portfolio_df.drop(columns=['card_name_inventory', 'card_name_lookup'])
    else:
        portfolio_df['card_name'] = portfolio_df['card_name'].fillna('UNKNOWN')
    
    # Create index column
    portfolio_df['index'] = (portfolio_df['binder_name'].astype(str) + '-' +
                             portfolio_df['page_number'].astype(str) + '-' +
                             portfolio_df['slot_number'].astype(str))
    
    # Define final columns
    final_cols = ['index', 'card_name', 'set_name', 'card_id', 
                  'binder_name', 'page_number', 'slot_number', 'card_market_value']
    
    # Write to CSV
    portfolio_df[final_cols].to_csv(output_file, index=False)
    print(f"Portfolio successfully written to {output_file}")

def main():
    """Production mode"""
    update_portfolio('./card_inventory/', './card_set_lookup/', 'card_portfolio.csv')

def test():
    """Test mode"""
    update_portfolio('./card_inventory_test/', './card_set_lookup_test/', 'test_card_portfolio.csv')

if __name__ == "__main__":
    print("Starting in Test Mode...", file=sys.stderr)
    test()