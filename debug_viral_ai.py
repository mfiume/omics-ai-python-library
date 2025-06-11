#!/usr/bin/env python3
"""
Debug script for Viral AI collections.virusseq.variants table
Quick standalone test to debug JSON Lines parsing issues
"""

import json
import re
import time
from typing import Dict, List, Optional, Any
from urllib.parse import quote
import requests

def parse_json_lines_response(raw_text: str, debug: bool = False) -> Dict[str, Any]:
    """
    Parse JSON Lines response format from Viral AI API.
    
    Expected format:
    {}
    {}
    {}
    {"data": [...], "pagination": {...}, "data_model": {...}}
    """
    if debug:
        print(f"🔍 Debug: Raw response length: {len(raw_text)}")
        print(f"🔍 Debug: First 500 chars: {raw_text[:500]}")
        print(f"🔍 Debug: Last 200 chars: {raw_text[-200:]}")
        print("🔍 Debug: Full raw text:")
        print("=" * 80)
        print(raw_text)
        print("=" * 80)
    
    if not raw_text.strip():
        raise Exception("Empty response received")
    
    # Split by lines and filter out empty lines
    lines = [line.strip() for line in raw_text.strip().split('\n') if line.strip()]
    
    if debug:
        print(f"🔍 Debug: Found {len(lines)} non-empty lines")
        for i, line in enumerate(lines):
            print(f"🔍 Debug: Line {i+1} (len={len(line)}): {line}")
    
    if not lines:
        raise Exception("No valid lines found in response")
    
    # Parse each line as JSON
    json_objects = []
    for i, line in enumerate(lines):
        try:
            obj = json.loads(line)
            json_objects.append(obj)
            if debug:
                keys = list(obj.keys()) if obj else []
                print(f"🔍 Debug: Parsed line {i+1}: keys={keys}")
                if obj and 'data' in obj:
                    print(f"🔍 Debug: Line {i+1} has data array with {len(obj['data'])} items")
        except json.JSONDecodeError as e:
            if debug:
                print(f"🔍 Debug: Failed to parse line {i+1}: {e}")
                print(f"🔍 Debug: Line content: '{line}'")
            if line != "{}":
                print(f"⚠️ Failed to parse line {i+1}: {line[:100]}... - {e}")
    
    if debug:
        print(f"🔍 Debug: Successfully parsed {len(json_objects)} JSON objects")
        for i, obj in enumerate(json_objects):
            keys = list(obj.keys()) if obj else []
            print(f"🔍 Debug: Object {i+1} keys: {keys}")
    
    if not json_objects:
        raise Exception("No valid JSON objects found in response")
    
    # Find the object with data (usually the last non-empty one)
    for obj in reversed(json_objects):
        if obj and 'data' in obj:
            if debug:
                print(f"🔍 Debug: Found data object with {len(obj['data'])} rows")
            return obj
    
    # If no data object found, check for next_page_token (polling case)
    for obj in reversed(json_objects):
        if obj and 'next_page_token' in obj:
            if debug:
                print(f"🔍 Debug: Found next_page_token: {obj['next_page_token'][:50]}...")
            return obj
    
    # If we get here, we have only empty objects {} or unexpected format
    if all(not obj for obj in json_objects):
        # All empty objects - this might be a polling response
        if debug:
            print("🔍 Debug: All objects are empty, treating as polling case")
        return {"next_page_token": "empty_response_poll"}
    
    # Return the last non-empty object
    non_empty_objects = [obj for obj in json_objects if obj]
    if non_empty_objects:
        result = non_empty_objects[-1]
        if debug:
            print(f"🔍 Debug: Returning last non-empty object with keys: {list(result.keys())}")
        return result
    
    raise Exception(f"No data or next_page_token found. Objects: {json_objects}")

class ViralAIClient:
    """Simplified client specifically for Viral AI debugging."""
    
    def __init__(self):
        self.base_url = "https://viral.ai"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'viral-ai-debug-client/1.0',
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        })
    
    def test_connection(self):
        """Test basic connection to Viral AI."""
        print("🔗 Testing connection to Viral AI...")
        try:
            response = self.session.get(f"{self.base_url}/api/collections")
            print(f"✅ Connection successful! Status: {response.status_code}")
            collections = response.json()
            print(f"✅ Found {len(collections)} collections")
            
            # Look for virusseq collection
            virusseq = next((c for c in collections if c.get('slugName') == 'virusseq'), None)
            if virusseq:
                print(f"✅ Found VirusSeq collection: {virusseq['name']}")
                return True
            else:
                print("❌ VirusSeq collection not found")
                print("Available collections:")
                for c in collections[:10]:
                    print(f"   - {c.get('name', 'Unnamed')} ({c.get('slugName', 'no-slug')})")
                return False
        except Exception as e:
            print(f"❌ Connection failed: {e}")
            return False
    
    def test_tables(self):
        """Test listing tables in virusseq collection."""
        print("\n📋 Testing table listing...")
        try:
            response = self.session.get(f"{self.base_url}/api/collections/virusseq/tables")
            print(f"✅ Tables request successful! Status: {response.status_code}")
            tables = response.json()
            print(f"✅ Found {len(tables)} tables in virusseq collection")
            
            for table in tables:
                table_name = table.get('qualified_table_name', table.get('name', 'Unknown'))
                print(f"   - {table_name}")
                if 'variants' in table_name.lower():
                    print(f"     👆 This looks like our target table!")
            
            return len(tables) > 0
        except Exception as e:
            print(f"❌ Tables request failed: {e}")
            return False
    
    def test_schema(self):
        """Test getting schema for variants table."""
        print("\n📊 Testing schema request...")
        try:
            response = self.session.get(f"{self.base_url}/api/collection/virusseq/data-connect/table/collections.virusseq.variants/info")
            print(f"✅ Schema request successful! Status: {response.status_code}")
            schema = response.json()
            
            data_model = schema.get('data_model', {}).get('properties', {})
            print(f"✅ Schema has {len(data_model)} fields")
            
            # Show first few fields
            for i, (field_name, field_spec) in enumerate(list(data_model.items())[:10]):
                field_type = field_spec.get('type', 'unknown')
                print(f"   {i+1}. {field_name}: {field_type}")
            
            return len(data_model) > 0
        except Exception as e:
            print(f"❌ Schema request failed: {e}")
            return False
    
    def test_query(self, debug: bool = True, max_polls: int = 5):
        """Test querying the variants table with debug output."""
        print(f"\n🔍 Testing query with debug={debug}...")
        
        payload = {
            "tableName": "collections.virusseq.variants",
            "filters": {},
            "pagination": {
                "limit": 10,  # Start small
                "offset": 0
            }
        }
        
        endpoint = f"{self.base_url}/api/collections/virusseq/tables/collections.virusseq.variants/filter"
        
        print(f"🔍 Endpoint: {endpoint}")
        print(f"🔍 Payload: {json.dumps(payload, indent=2)}")
        
        for poll_count in range(max_polls):
            print(f"\n🔄 Poll {poll_count + 1}/{max_polls}...")
            
            try:
                response = self.session.post(endpoint, json=payload)
                print(f"✅ Request successful! Status: {response.status_code}")
                print(f"✅ Response headers: {dict(response.headers)}")
                
                # Parse response
                result = parse_json_lines_response(response.text, debug=debug)
                
                # Check result
                if 'data' in result and isinstance(result['data'], list):
                    print(f"🎉 SUCCESS! Got {len(result['data'])} rows of data!")
                    
                    if result['data']:
                        sample_row = result['data'][0]
                        print(f"📊 Sample row keys: {list(sample_row.keys())}")
                        print(f"📝 Sample row: {sample_row}")
                    
                    if 'pagination' in result:
                        print(f"📄 Pagination info: {result['pagination']}")
                    
                    return True
                
                elif 'next_page_token' in result:
                    token = result['next_page_token']
                    print(f"⏳ Got next_page_token, polling again: {token[:50]}...")
                    payload['next_page_token'] = token
                    time.sleep(2)
                
                else:
                    print(f"❓ Unexpected result format: {list(result.keys())}")
                    print(f"❓ Result: {result}")
                    return False
                    
            except Exception as e:
                print(f"❌ Poll {poll_count + 1} failed: {e}")
                return False
        
        print(f"⏰ Query timed out after {max_polls} polls")
        return False

def main():
    """Main debug function."""
    print("🦠 VIRAL AI DEBUG SCRIPT")
    print("=" * 50)
    print("Target: collections.virusseq.variants")
    print("Network: https://viral.ai")
    print("=" * 50)
    
    client = ViralAIClient()
    
    # Test 1: Basic connection
    if not client.test_connection():
        print("❌ Basic connection failed, stopping here")
        return
    
    # Test 2: List tables
    if not client.test_tables():
        print("❌ Table listing failed, stopping here")
        return
    
    # Test 3: Get schema
    if not client.test_schema():
        print("❌ Schema request failed, stopping here")
        return
    
    # Test 4: Query with debug
    print("\n" + "="*50)
    print("🚀 MAIN TEST: Querying variants table")
    print("="*50)
    
    success = client.test_query(debug=True, max_polls=10)
    
    if success:
        print("\n🎉 ALL TESTS PASSED!")
        print("✅ Viral AI query is working correctly")
    else:
        print("\n❌ QUERY TEST FAILED")
        print("💡 Check the debug output above for clues")

if __name__ == "__main__":
    main()