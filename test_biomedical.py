#!/usr/bin/env python3
"""
Test with biomedical.ai which may have more public collections.
"""

print("🧬 Testing with biomedical.ai")
print("=" * 40)

from omics_ai import OmicsAIClient

# Connect to biomedical.ai
client = OmicsAIClient("biomedical.ai")

# List collections
collections = client.list_collections()
print(f"📂 Found {len(collections)} collections:")

for i, collection in enumerate(collections[:5]):
    print(f"  {i+1}. {collection['name']} ({collection['slugName']})")

# Try to access gnomAD which is likely public
print(f"\n📊 Testing gnomAD collection...")
try:
    tables = client.list_tables("gnomad")
    print(f"✅ gnomAD has {len(tables)} tables:")
    
    for i, table in enumerate(tables[:3]):
        size_str = f"{table['size']:,}" if table.get('size') else "Unknown"
        print(f"  {i+1}. {table.get('display_name', 'Unnamed')}")
        print(f"     Size: {size_str} rows")
        print(f"     ID: {table.get('qualified_table_name', 'N/A')}")
        
    if tables:
        # Try to get schema
        print(f"\n🔬 Getting schema for first table...")
        table_name = tables[0]['qualified_table_name']
        schema_fields = client.get_schema_fields("gnomad", table_name)
        print(f"✅ Found {len(schema_fields)} fields:")
        
        for i, field in enumerate(schema_fields[:5]):
            print(f"  {i+1}. {field['field']}: {field['type']}")
            
        # Try a count query
        print(f"\n🔢 Counting rows in table...")
        count = client.count("gnomad", table_name)
        print(f"✅ Total rows: {count:,}")
        
        # Try a small query
        print(f"\n🔎 Fetching sample data...")
        results = client.query("gnomad", table_name, limit=1)
        if results.get('data'):
            sample = results['data'][0]
            print(f"✅ Sample row has {len(sample)} fields")
            print(f"   Fields: {list(sample.keys())[:5]}...")
        
except Exception as e:
    print(f"❌ Error with gnomAD: {e}")

print(f"\n🎉 biomedical.ai test completed!")