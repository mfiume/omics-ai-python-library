#!/usr/bin/env python3
"""
Advanced query examples for the Omics AI Explorer Python library.
"""

from omics_ai import OmicsAIClient


def complex_filters_example():
    """Example: Using complex filters with multiple conditions."""
    print("🔍 Complex filtering example...")
    
    client = OmicsAIClient("hifisolves")
    
    try:
        collection = "gnomad"
        table = "collections.gnomad.variants"
        
        # Complex filter: rare variants in a specific region
        filters = {
            "chrom": [{"operation": "EQ", "value": "chr17", "type": "STRING"}],
            "pos": [
                {"operation": "GTE", "value": 43000000, "type": "INTEGER"},
                {"operation": "LTE", "value": 43200000, "type": "INTEGER"}
            ],
            "af": [{"operation": "LT", "value": 0.01, "type": "FLOAT"}]  # Allele frequency < 1%
        }
        
        print("Searching for rare variants in BRCA1 region (chr17:43M-43.2M, AF < 1%)...")
        
        results = client.query(
            collection,
            table,
            filters=filters,
            limit=20,
            order_by={"field": "pos", "direction": "ASC"}
        )
        
        print(f"Found {len(results.get('data', []))} variants")
        
        for variant in results.get('data', [])[:5]:
            # Adjust field names based on actual schema
            pos = variant.get('pos', 'Unknown')
            ref = variant.get('ref', 'Unknown')
            alt = variant.get('alt', 'Unknown')
            af = variant.get('af', 'Unknown')
            print(f"  chr17:{pos} {ref}>{alt} (AF: {af})")
            
    except Exception as e:
        print(f"Error: {e}")


def pattern_matching_example():
    """Example: Using pattern matching and regex filters."""
    print("🔤 Pattern matching example...")
    
    client = OmicsAIClient("hifisolves")
    
    try:
        collection = "gnomad"
        table = "collections.gnomad.variants"
        
        # Find variants with specific patterns
        filters = {
            # Example: Find variants where consequence contains "missense"
            "consequence": [{"operation": "LIKE", "value": "%missense%", "type": "STRING"}],
            # Example: Find high-impact variants using regex
            "impact": [{"operation": "REGEX", "value": "HIGH|MODERATE", "type": "STRING"}]
        }
        
        print("Searching for missense variants with high/moderate impact...")
        
        results = client.query(collection, table, filters=filters, limit=10)
        
        print(f"Found {len(results.get('data', []))} variants")
        
        for variant in results.get('data', [])[:3]:
            consequence = variant.get('consequence', 'Unknown')
            impact = variant.get('impact', 'Unknown')
            print(f"  Consequence: {consequence}, Impact: {impact}")
            
    except Exception as e:
        print(f"Error: {e}")


def range_queries_example():
    """Example: Range queries and BETWEEN operations."""
    print("📏 Range queries example...")
    
    client = OmicsAIClient("hifisolves")
    
    try:
        collection = "gnomad"
        table = "collections.gnomad.variants"
        
        # Range query: variants in a specific quality score range
        filters = {
            "qual": [{"operation": "BETWEEN", "value": [100, 500], "type": "FLOAT"}],
            "dp": [{"operation": "GTE", "value": 10, "type": "INTEGER"}]  # Depth >= 10
        }
        
        print("Searching for variants with quality scores between 100-500 and depth >= 10...")
        
        count = client.count(collection, table, filters=filters)
        print(f"Total matching variants: {count:,}")
        
        if count > 0:
            results = client.query(collection, table, filters=filters, limit=5)
            
            for variant in results.get('data', []):
                qual = variant.get('qual', 'Unknown')
                dp = variant.get('dp', 'Unknown')
                print(f"  Quality: {qual}, Depth: {dp}")
                
    except Exception as e:
        print(f"Error: {e}")


def null_value_handling_example():
    """Example: Handling null values in queries."""
    print("🚫 Null value handling example...")
    
    client = OmicsAIClient("hifisolves")
    
    try:
        collection = "gnomad"
        table = "collections.gnomad.variants"
        
        # Find variants where certain fields are not null
        filters = {
            "gene": [{"operation": "NOT_NULL", "value": None, "type": "STRING"}],
            "clinvar_significance": [{"operation": "NULL", "value": None, "type": "STRING"}]
        }
        
        print("Searching for variants with gene annotations but no ClinVar significance...")
        
        count = client.count(collection, table, filters=filters)
        print(f"Found {count:,} variants")
        
    except Exception as e:
        print(f"Error: {e}")


def pagination_example():
    """Example: Working with large result sets using pagination."""
    print("📄 Pagination example...")
    
    client = OmicsAIClient("hifisolves")
    
    try:
        collection = "gnomad"
        table = "collections.gnomad.variants"
        
        # Simple filter for demonstration
        filters = {
            "chrom": [{"operation": "EQ", "value": "chr22", "type": "STRING"}]
        }
        
        print("Fetching variants from chr22 in batches...")
        
        page_size = 50
        offset = 0
        total_fetched = 0
        max_results = 200  # Limit for this example
        
        while total_fetched < max_results:
            results = client.query(
                collection,
                table,
                filters=filters,
                limit=page_size,
                offset=offset
            )
            
            data = results.get('data', [])
            if not data:
                break
                
            print(f"  Fetched {len(data)} variants (offset {offset})")
            total_fetched += len(data)
            offset += page_size
            
            # Process the batch
            for variant in data[:2]:  # Show first 2 from each batch
                pos = variant.get('pos', 'Unknown')
                print(f"    chr22:{pos}")
                
            if len(data) < page_size:
                break  # Last page
                
        print(f"Total fetched: {total_fetched} variants")
        
    except Exception as e:
        print(f"Error: {e}")


def aggregation_example():
    """Example: Using counts for aggregation-like queries."""
    print("📊 Aggregation example...")
    
    client = OmicsAIClient("hifisolves")
    
    try:
        collection = "gnomad"
        table = "collections.gnomad.variants"
        
        # Count variants by chromosome
        chromosomes = ["chr1", "chr2", "chr3", "chrX", "chrY"]
        
        print("Variant counts by chromosome:")
        
        for chrom in chromosomes:
            filters = {
                "chrom": [{"operation": "EQ", "value": chrom, "type": "STRING"}]
            }
            
            count = client.count(collection, table, filters=filters)
            print(f"  {chrom}: {count:,} variants")
            
        # Count by variant type
        print("\nVariant counts by type:")
        variant_types = ["SNV", "INDEL", "MNV"]
        
        for vtype in variant_types:
            filters = {
                "variant_type": [{"operation": "EQ", "value": vtype, "type": "STRING"}]
            }
            
            count = client.count(collection, table, filters=filters)
            print(f"  {vtype}: {count:,} variants")
            
    except Exception as e:
        print(f"Error: {e}")


def multi_collection_search():
    """Example: Searching across multiple collections."""
    print("🔍 Multi-collection search example...")
    
    client = OmicsAIClient("hifisolves")
    
    # Get all collections
    collections = client.list_collections()
    
    search_term = "BRCA"
    print(f"Searching for collections containing '{search_term}'...")
    
    matching_collections = []
    for collection in collections:
        name = collection.get('name', '').lower()
        description = collection.get('description', '').lower()
        
        if search_term.lower() in name or search_term.lower() in description:
            matching_collections.append(collection)
            
    print(f"Found {len(matching_collections)} matching collections:")
    for collection in matching_collections:
        print(f"  📂 {collection['name']} ({collection['slugName']})")
        
        # Try to get table count
        try:
            tables = client.list_tables(collection['slugName'])
            print(f"     Contains {len(tables)} tables")
        except:
            print("     Could not access tables")


if __name__ == "__main__":
    print("🧬 Advanced Omics AI Explorer Query Examples\n")
    
    examples = [
        complex_filters_example,
        pattern_matching_example,
        range_queries_example,
        null_value_handling_example,
        pagination_example,
        aggregation_example,
        multi_collection_search
    ]
    
    for i, example in enumerate(examples):
        print(f"\n{'='*60}")
        print(f"Example {i+1}: {example.__name__.replace('_', ' ').title()}")
        print('='*60)
        
        try:
            example()
        except Exception as e:
            print(f"Example failed: {e}")
    
    print("\n✨ Advanced examples completed!")
    print("Note: These examples use placeholder field names that may not exist in actual schemas.")
    print("Always inspect the schema first using get_schema_fields() before querying.")