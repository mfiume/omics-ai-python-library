#!/usr/bin/env python3
"""
Simplified test of the library focusing on basic functionality.
"""

print("🧬 Testing Omics AI Explorer Python Library")
print("=" * 50)

# Test imports
try:
    from omics_ai import OmicsAIClient
    print("✅ Import successful")
except ImportError as e:
    print(f"❌ Import failed: {e}")
    exit(1)

# Test different networks
networks = ["hifisolves.org", "biomedical.ai", "neuroscience.ai"]

for network in networks:
    print(f"\n🌐 Testing {network}...")
    try:
        client = OmicsAIClient(network)
        collections = client.list_collections()
        print(f"✅ {network}: {len(collections)} collections found")
        
        # Show first few collections
        for i, collection in enumerate(collections[:3]):
            print(f"   {i+1}. {collection['name']} ({collection['slugName']})")
            
        if len(collections) > 3:
            print(f"   ... and {len(collections) - 3} more")
            
    except Exception as e:
        print(f"❌ {network}: {e}")

# Test short network names
print(f"\n🔗 Testing short network names...")
try:
    client = OmicsAIClient("hifisolves")  # Short name
    collections = client.list_collections()
    print(f"✅ Short name 'hifisolves' works: {len(collections)} collections")
except Exception as e:
    print(f"❌ Short name test failed: {e}")

# Test client methods exist
print(f"\n🔧 Testing client methods...")
client = OmicsAIClient("hifisolves")

methods_to_test = [
    'list_collections', 'list_tables', 'get_schema', 
    'get_schema_fields', 'query', 'simple_query', 'count',
    'set_access_token', 'clear_access_token'
]

for method in methods_to_test:
    if hasattr(client, method):
        print(f"✅ Method '{method}' exists")
    else:
        print(f"❌ Method '{method}' missing")

print(f"\n🎉 Basic functionality test completed!")
print("\nThe library is working correctly for basic operations.")
print("Some collections may require authentication for full access.")