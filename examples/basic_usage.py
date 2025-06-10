#!/usr/bin/env python3
"""
Basic usage examples for the Omics AI Explorer Python library.
"""

from omics_ai import OmicsAIClient


def explore_collections():
    """Example: Discover available collections and tables."""
    print("🔍 Exploring HiFi Solves collections...")
    
    # Connect to HiFi Solves
    client = OmicsAIClient("hifisolves")
    
    # List all collections
    collections = client.list_collections()
    print(f"Found {len(collections)} collections:")
    
    for collection in collections[:5]:  # Show first 5
        print(f"  📂 {collection['name']} ({collection['slugName']})")
        if collection.get('description'):
            desc = collection['description'][:100] + "..." if len(collection['description']) > 100 else collection['description']
            print(f"     {desc}")
        print()


def explore_tables():
    """Example: Browse tables in a specific collection."""
    print("📊 Exploring tables in gnomAD collection...")
    
    client = OmicsAIClient("hifisolves")
    
    try:
        tables = client.list_tables("gnomad")
        print(f"Found {len(tables)} tables in gnomAD:")
        
        for table in tables:
            size_str = f"{table['size']:,}" if table['size'] else "Unknown"
            print(f"  📈 {table['display_name']}")
            print(f"     Table: {table['qualified_table_name']}")
            print(f"     Size: {size_str} rows")
            print()
            
    except Exception as e:
        print(f"Error: {e}")


def inspect_schema():
    """Example: Examine table schema before querying."""
    print("🔬 Inspecting table schema...")
    
    client = OmicsAIClient("hifisolves")
    
    try:
        # Pick a common table that's likely to exist
        collection = "gnomad"
        table = "collections.gnomad.variants"  # This might need adjustment
        
        print(f"Schema for {table}:")
        fields = client.get_schema_fields(collection, table)
        
        print(f"Found {len(fields)} fields:")
        for field in fields[:10]:  # Show first 10 fields
            print(f"  🔖 {field['field']}: {field['type']}")
            if field['sql_type']:
                print(f"     SQL Type: {field['sql_type']}")
        
        if len(fields) > 10:
            print(f"  ... and {len(fields) - 10} more fields")
            
    except Exception as e:
        print(f"Error: {e}")


def simple_query_example():
    """Example: Perform a simple query."""
    print("🔎 Performing a simple query...")
    
    client = OmicsAIClient("hifisolves")
    
    try:
        # Simple query example
        collection = "gnomad"
        table = "collections.gnomad.variants"
        
        print(f"Querying {table} for chromosome 22 variants...")
        
        # This is a simple example - adjust fields based on actual schema
        results = client.simple_query(
            collection,
            table,
            chrom="chr22"  # This field name might need adjustment
        )
        
        print(f"Found {len(results)} results")
        
        # Show first few results
        for i, row in enumerate(results[:3]):
            print(f"  Result {i+1}: {dict(list(row.items())[:5])}...")  # Show first 5 fields
            
    except Exception as e:
        print(f"Error: {e}")
        print("Note: This example uses placeholder field names that may not exist in the actual schema")


def count_example():
    """Example: Count results without fetching all data."""
    print("🔢 Counting query results...")
    
    client = OmicsAIClient("hifisolves")
    
    try:
        collection = "gnomad"
        table = "collections.gnomad.variants"
        
        # Count all variants
        total_count = client.count(collection, table)
        print(f"Total variants in {table}: {total_count:,}")
        
        # Count with filter
        filters = {
            "chrom": [{"operation": "EQ", "value": "chr22", "type": "STRING"}]
        }
        chr22_count = client.count(collection, table, filters=filters)
        print(f"Variants on chr22: {chr22_count:,}")
        
    except Exception as e:
        print(f"Error: {e}")


def multiple_networks_example():
    """Example: Working with multiple Explorer networks."""
    print("🌐 Exploring multiple networks...")
    
    networks = ["hifisolves", "neuroscience", "biomedical"]
    
    for network in networks:
        try:
            print(f"\n--- {network.upper()} NETWORK ---")
            client = OmicsAIClient(network)
            collections = client.list_collections()
            print(f"Collections available: {len(collections)}")
            
            # Show first collection
            if collections:
                first_collection = collections[0]
                print(f"Example: {first_collection['name']}")
                
        except Exception as e:
            print(f"Error accessing {network}: {e}")


if __name__ == "__main__":
    print("🧬 Omics AI Explorer Python Library Examples\n")
    
    # Run examples
    explore_collections()
    print("-" * 60)
    
    explore_tables()
    print("-" * 60)
    
    inspect_schema()
    print("-" * 60)
    
    simple_query_example()
    print("-" * 60)
    
    count_example()
    print("-" * 60)
    
    multiple_networks_example()
    
    print("\n✨ Examples completed!")
    print("Note: Some examples may fail if the expected collections/tables don't exist.")
    print("Adjust the collection and table names based on what's actually available.")