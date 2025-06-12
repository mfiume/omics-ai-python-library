#!/usr/bin/env python3
"""
Test script for SQL query functionality in omics-ai-python-library.
"""

from omics_ai import sql_query

def test_sql_query():
    """Test the SQL query functionality."""
    
    print("🧬 Testing Omics AI SQL Query Functionality")
    print("=" * 50)
    
    # Test 1: Simple SELECT 1 query
    print("\n📋 Test 1: Simple SELECT 1")
    try:
        result = sql_query(
            "hifisolves",
            "consortium-of-long-read-sequencing-colors", 
            "SELECT 1 as test_value"
        )
        print(f"✅ SUCCESS: {result}")
    except Exception as e:
        print(f"❌ FAILED: {e}")
    
    # Test 2: Count query
    print("\n📋 Test 2: Count variants")
    try:
        result = sql_query(
            "hifisolves",
            "consortium-of-long-read-sequencing-colors",
            'SELECT COUNT(*) as total_variants FROM "collections"."consortium_of_long_read_sequencing_colors"."small_variants"'
        )
        if result.get('data'):
            total = result['data'][0]['total_variants']
            print(f"✅ SUCCESS: Found {total:,} total variants")
        else:
            print(f"⚠️  Empty result: {result}")
    except Exception as e:
        print(f"❌ FAILED: {e}")
    
    # Test 3: Query with WHERE clause
    print("\n📋 Test 3: Query chrM variants")
    try:
        result = sql_query(
            "hifisolves", 
            "consortium-of-long-read-sequencing-colors",
            'SELECT * FROM "collections"."consortium_of_long_read_sequencing_colors"."small_variants" WHERE chrom = \'chrM\' LIMIT 5'
        )
        if result.get('data'):
            print(f"✅ SUCCESS: Found {len(result['data'])} chrM variants")
            print("First variant:", result['data'][0] if result['data'] else "None")
        else:
            print(f"⚠️  Empty result: {result}")
    except Exception as e:
        print(f"❌ FAILED: {e}")
    
    # Test 4: Show available chromosomes
    print("\n📋 Test 4: Show available chromosomes")
    try:
        result = sql_query(
            "hifisolves",
            "consortium-of-long-read-sequencing-colors", 
            'SELECT DISTINCT chrom FROM "collections"."consortium_of_long_read_sequencing_colors"."small_variants" ORDER BY chrom LIMIT 10'
        )
        if result.get('data'):
            chroms = [row['chrom'] for row in result['data']]
            print(f"✅ SUCCESS: Available chromosomes: {chroms}")
        else:
            print(f"⚠️  Empty result: {result}")
    except Exception as e:
        print(f"❌ FAILED: {e}")

if __name__ == "__main__":
    test_sql_query()