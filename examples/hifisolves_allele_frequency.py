#!/usr/bin/env python3
"""
HiFi Solves specific example: Allele frequency lookups using Questions API.

This example demonstrates how to use the Questions API for allele frequency
lookups, similar to the JavaScript HiFiSolvesAlleleFrequency function.
"""

import json
from omics_ai import OmicsAIClient


class HiFiSolvesClient(OmicsAIClient):
    """Extended client with HiFi Solves specific functionality."""
    
    def __init__(self, access_token: str = None):
        super().__init__("hifisolves.org", access_token)
    
    def allele_frequency_lookup(self, chromosome: str, position: int) -> dict:
        """
        Perform allele frequency lookup using the Questions API.
        
        This replicates the HiFiSolvesAlleleFrequency function from the JavaScript code.
        
        Args:
            chromosome: Chromosome (e.g., "chr15")
            position: Genomic position (e.g., 64314563)
            
        Returns:
            Dictionary containing allele frequency results from multiple collections
        """
        endpoint = "/api/questions/allele-frequency/query"
        
        payload = {
            "inputs": {
                "chromosome": chromosome,
                "position": str(position)
            },
            "collections": None
        }
        
        response = self._make_request('POST', endpoint, json=payload)
        return response.json()
    
    def get_aggregated_allele_frequency(self, chromosome: str, position: int) -> float:
        """
        Calculate aggregated allele frequency across all collections.
        
        This replicates the HiFiSolvesAggregativeAlleleFrequency function.
        
        Args:
            chromosome: Chromosome (e.g., "chr15")
            position: Genomic position
            
        Returns:
            Aggregated allele frequency (total count / total number)
        """
        data = self.allele_frequency_lookup(chromosome, position)
        
        if not data.get('results'):
            return 0.0
            
        total_count = 0
        total_number = 0
        
        for result in data['results']:
            result_data = result.get('results', {}).get('data', [])
            if result_data:
                row = result_data[0]  # First row contains the data
                
                allele_count = row.get('Allele Count', 0)
                allele_number = row.get('Allele Number', 0)
                
                if isinstance(allele_count, (int, float)) and isinstance(allele_number, (int, float)):
                    if allele_count > 0 and allele_number == 0:
                        raise ValueError(f"Non-zero allele count with zero allele number in {result.get('collectionSlug', 'unknown')}")
                    
                    total_count += allele_count
                    total_number += allele_number
        
        return total_count / total_number if total_number > 0 else 0.0


def allele_frequency_example():
    """Example: Look up allele frequency for a specific variant."""
    print("🧬 HiFi Solves Allele Frequency Lookup Example")
    
    # Initialize HiFi Solves client
    # Note: You may need an access token for some collections
    client = HiFiSolvesClient()
    
    # Example variant - adjust chromosome and position as needed
    chromosome = "chr15"
    position = 64314563
    
    print(f"Looking up allele frequency for {chromosome}:{position}...")
    
    try:
        # Get detailed results
        results = client.allele_frequency_lookup(chromosome, position)
        
        if not results.get('results'):
            print("No results found")
            return
            
        print(f"Found results from {len(results['results'])} collections:")
        
        # Display results from each collection
        for result in results['results']:
            collection_name = result.get('collectionSlug', 'Unknown')
            result_data = result.get('results', {}).get('data', [])
            
            if result_data:
                row = result_data[0]
                allele_count = row.get('Allele Count', 'N/A')
                allele_number = row.get('Allele Number', 'N/A')
                allele_freq = row.get('Allele Frequency', 'N/A')
                
                print(f"  📊 {collection_name}:")
                print(f"     Count: {allele_count}")
                print(f"     Number: {allele_number}")
                print(f"     Frequency: {allele_freq}")
            else:
                print(f"  📊 {collection_name}: No data")
        
        # Calculate aggregated frequency
        try:
            agg_freq = client.get_aggregated_allele_frequency(chromosome, position)
            print(f"\n🔢 Aggregated Allele Frequency: {agg_freq:.6f}")
            
        except Exception as e:
            print(f"\n❌ Error calculating aggregated frequency: {e}")
            
    except Exception as e:
        print(f"Error: {e}")


def batch_allele_frequency_example():
    """Example: Batch lookup of multiple variants."""
    print("\n📋 Batch Allele Frequency Lookup Example")
    
    client = HiFiSolvesClient()
    
    # List of variants to look up
    variants = [
        ("chr17", 43094692),  # BRCA1 region
        ("chr13", 32338111),  # BRCA2 region
        ("chr15", 64314563),  # Example variant
    ]
    
    print(f"Looking up allele frequencies for {len(variants)} variants...")
    
    results = []
    
    for chromosome, position in variants:
        try:
            agg_freq = client.get_aggregated_allele_frequency(chromosome, position)
            results.append({
                'variant': f"{chromosome}:{position}",
                'frequency': agg_freq
            })
            print(f"  ✅ {chromosome}:{position} -> {agg_freq:.6f}")
            
        except Exception as e:
            print(f"  ❌ {chromosome}:{position} -> Error: {e}")
            results.append({
                'variant': f"{chromosome}:{position}",
                'frequency': None,
                'error': str(e)
            })
    
    # Summary
    print(f"\n📊 Summary:")
    valid_results = [r for r in results if r.get('frequency') is not None]
    
    if valid_results:
        frequencies = [r['frequency'] for r in valid_results]
        avg_freq = sum(frequencies) / len(frequencies)
        max_freq = max(frequencies)
        min_freq = min(frequencies)
        
        print(f"  Valid lookups: {len(valid_results)}/{len(variants)}")
        print(f"  Average frequency: {avg_freq:.6f}")
        print(f"  Range: {min_freq:.6f} - {max_freq:.6f}")
    else:
        print("  No valid results obtained")


def explore_questions_api():
    """Example: Explore what questions are available."""
    print("\n❓ Exploring Available Questions")
    
    client = HiFiSolvesClient()
    
    try:
        # Try to get available collections to understand the structure
        collections = client.list_collections()
        
        print("Available collections in HiFi Solves:")
        for collection in collections[:5]:  # Show first 5
            print(f"  📂 {collection['name']} ({collection['slugName']})")
            
            # Try to get questions for this collection if the API supports it
            try:
                # This endpoint might exist based on the OpenAPI spec
                collection_id = collection['slugName']
                endpoint = f"/api/v2/collection/{collection_id}/items"
                response = client._make_request('GET', endpoint)
                items = response.json()
                
                questions = [item for item in items if item.get('type') == 'question']
                if questions:
                    print(f"     Questions available: {len(questions)}")
                    for question in questions[:2]:  # Show first 2
                        print(f"       - {question.get('name', 'Unnamed')}")
                        
            except Exception:
                # Questions API might not be accessible or might have different structure
                pass
                
    except Exception as e:
        print(f"Error exploring questions: {e}")


if __name__ == "__main__":
    print("🧬 HiFi Solves Allele Frequency Examples\n")
    
    # Note: These examples require access to HiFi Solves
    # Some functionality may require authentication
    
    print("Note: These examples may require authentication for full access.")
    print("If you get authentication errors, you may need to provide an access token.\n")
    
    try:
        allele_frequency_example()
        batch_allele_frequency_example()
        explore_questions_api()
        
    except Exception as e:
        print(f"\n❌ Examples failed: {e}")
        print("\nThis might be due to:")
        print("1. Network connectivity issues")
        print("2. Need for authentication (access token)")
        print("3. Changes in the HiFi Solves API structure")
        print("4. The specific questions or collections not being available")
    
    print("\n✨ HiFi Solves examples completed!")
    print("\nTo use with authentication:")
    print("client = HiFiSolvesClient(access_token='your-token-here')")