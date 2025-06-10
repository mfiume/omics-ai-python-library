#!/usr/bin/env python3
"""
Test script to validate the Quick Start example from README.
"""

print("🧬 Testing Omics AI Explorer Python Library - Quick Start")
print("=" * 60)

try:
    from omics_ai import OmicsAIClient
    print("✅ Successfully imported OmicsAIClient")
except ImportError as e:
    print(f"❌ Import failed: {e}")
    exit(1)

# Connect to HiFi Solves
print("\n🔗 Connecting to HiFi Solves...")
try:
    client = OmicsAIClient("hifisolves.org")
    print("✅ Successfully created client for hifisolves.org")
except Exception as e:
    print(f"❌ Client creation failed: {e}")
    exit(1)

# List all collections
print("\n📂 Listing collections...")
try:
    collections = client.list_collections()
    print(f"✅ Found {len(collections)} collections:")
    
    for i, collection in enumerate(collections[:5]):  # Show first 5
        print(f"  {i+1}. {collection['name']} ({collection['slugName']})")
        if collection.get('description'):
            desc = collection['description'][:80] + "..." if len(collection['description']) > 80 else collection['description']
            # Clean up HTML tags for display
            import re
            desc = re.sub('<[^<]+?>', '', desc)
            print(f"     {desc}")
    
    if len(collections) > 5:
        print(f"     ... and {len(collections) - 5} more collections")
        
except Exception as e:
    print(f"❌ List collections failed: {e}")
    print("This might be due to network issues or API changes")

# Try to list tables in collections (try multiple until we find one that works)
tables = []
collection_slug = None

if collections:
    print(f"\n📊 Looking for accessible collections...")
    
    for collection in collections:
        try:
            collection_slug = collection['slugName']
            print(f"   Trying: {collection_slug}...")
            tables = client.list_tables(collection_slug)
            print(f"✅ Found {len(tables)} tables in '{collection_slug}':")
            
            for i, table in enumerate(tables[:3]):  # Show first 3
                size_str = f"{table['size']:,}" if table.get('size') else "Unknown size"
                print(f"  {i+1}. {table.get('display_name', table.get('name', 'Unnamed'))}")
                print(f"     Table ID: {table.get('qualified_table_name', 'N/A')}")
                print(f"     Size: {size_str} rows")
                
            if len(tables) > 3:
                print(f"     ... and {len(tables) - 3} more tables")
            break  # Found a working collection
            
        except Exception as e:
            print(f"   ❌ {collection_slug}: {e}")
            continue
    
    if not tables:
        print("⚠️  Could not access tables in any collection (may require authentication)")

# Try to get schema for the first table
schema_fields = []
if tables:
    print(f"\n🔬 Getting schema for first table...")
    try:
        table_name = tables[0]['qualified_table_name']
        schema_fields = client.get_schema_fields(collection_slug, table_name)
        print(f"✅ Found {len(schema_fields)} fields:")
        
        for i, field in enumerate(schema_fields[:5]):  # Show first 5
            print(f"  {i+1}. {field['field']}: {field['type']}")
            if field.get('sql_type'):
                print(f"     SQL Type: {field['sql_type']}")
                
        if len(schema_fields) > 5:
            print(f"     ... and {len(schema_fields) - 5} more fields")
            
    except Exception as e:
        print(f"❌ Get schema failed: {e}")
        schema_fields = []

# Try a simple query if we have field info
if schema_fields:
    print(f"\n🔎 Testing simple query...")
    try:
        # Find a likely string field to query
        string_fields = [f for f in schema_fields if 'string' in f['type'].lower() or 'varchar' in f.get('sql_type', '').lower()]
        
        if string_fields:
            field_name = string_fields[0]['field']
            print(f"Attempting query with field: {field_name}")
            
            # Try a simple count first (safer than fetching data)
            count = client.count(collection_slug, table_name)
            print(f"✅ Total rows in table: {count:,}")
            
            # Try a simple query with limit
            results = client.query(collection_slug, table_name, limit=1)
            if results.get('data'):
                print(f"✅ Successfully queried data (1 row sample)")
                sample_row = results['data'][0]
                print(f"   Sample fields: {list(sample_row.keys())[:5]}...")
            else:
                print("⚠️  Query returned no data")
                
        else:
            print("⚠️  No suitable string fields found for simple query test")
            
    except Exception as e:
        print(f"❌ Simple query failed: {e}")
        print("This might be due to access restrictions or API changes")

print("\n" + "=" * 60)
print("🎉 Quick Start test completed!")
print("\nNote: Some operations may fail due to:")
print("- Network connectivity issues")
print("- Authentication requirements")
print("- API changes or access restrictions")
print("- Collection/table availability")