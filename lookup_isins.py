#!/usr/bin/env python3
"""
Helper script to look up ISINs and generate mapping.yaml entries.
Uses Yahoo Finance search API to look up ticker symbols for ISINs.
"""

import sys
import requests
import time
from typing import Optional, Dict

def lookup_isin(isin: str) -> Optional[Dict[str, str]]:
    """
    Look up an ISIN using Yahoo Finance search API.
    Returns dict with 'symbol' and 'name' if found, None otherwise.
    """
    try:
        # Yahoo Finance search endpoint
        url = f"https://query1.finance.yahoo.com/v1/finance/search"
        params = {
            'q': isin,
            'quotesCount': 1,
            'newsCount': 0
        }
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(url, params=params, headers=headers, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        if 'quotes' in data and len(data['quotes']) > 0:
            quote = data['quotes'][0]
            return {
                'symbol': quote.get('symbol', ''),
                'name': quote.get('longname', quote.get('shortname', '')),
                'exchange': quote.get('exchange', '')
            }
    except Exception as e:
        print(f"Error looking up {isin}: {e}", file=sys.stderr)
    
    return None

def main():
    if len(sys.argv) < 2:
        print("Usage: python lookup_isins.py ISIN1 [ISIN2 ...]")
        print("\nExample:")
        print("  python lookup_isins.py US11135F1012 US09290D1019")
        sys.exit(1)
    
    isins = sys.argv[1:]
    
    print("# Suggested mappings for ISINs\n")
    print("symbol_mapping:")
    
    for isin in isins:
        result = lookup_isin(isin)
        if result:
            symbol = result['symbol']
            name = result['name']
            exchange = result['exchange']
            
            print(f"  # {name} ({exchange})")
            print(f"  {isin}: {symbol}")
        else:
            print(f"  # {isin}: NOT FOUND - Please look up manually")
            print(f"  # {isin}: TICKER_HERE")
        
        # Be nice to the API
        time.sleep(0.5)
    
    print("\n# Copy the mappings above to your mapping.yaml file")
    print("# Remove the 'NOT FOUND' entries and fill in manually if needed")

if __name__ == '__main__':
    main()
