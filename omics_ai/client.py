"""
Main client class for interacting with Omics AI Explorer instances.
"""

import json
import re
import time
from typing import Dict, List, Optional, Any, Union
from urllib.parse import urlencode, quote

import requests

from .exceptions import OmicsAIError, AuthenticationError, NetworkError, ValidationError


class OmicsAIClient:
    """
    Client for interacting with Omics AI Explorer instances.
    
    This client provides a simple interface to:
    - List collections across different Explorer networks
    - List tables within collections
    - Get table schemas
    - Perform queries on tables
    
    Example:
        >>> client = OmicsAIClient("hifisolves.org")
        >>> collections = client.list_collections()
        >>> tables = client.list_tables("gnomad")
        >>> schema = client.get_schema("gnomad", "collections.gnomad.variants")
        >>> results = client.query("gnomad", "collections.gnomad.variants", filters={"chrom": "chr1"})
    """
    
    # Common Explorer instances
    KNOWN_NETWORKS = {
        "hifisolves": "hifisolves.org",
        "neuroscience": "neuroscience.ai", 
        "asap": "cloud.parkinsonsroadmap.org",  # Aligning Science Across Parkinson's
        "parkinsons": "cloud.parkinsonsroadmap.org",  # Keep backward compatibility
        "biomedical": "biomedical.ai",
        "viral": "viral.ai",
        "targetals": "dataportal.targetals.org"  # Target ALS
    }
    
    def __init__(self, network: str = "hifisolves.org", access_token: Optional[str] = None):
        """
        Initialize the Omics AI client.
        
        Args:
            network: The Explorer network domain (e.g., 'hifisolves.org') or short name
            access_token: Optional access token for authenticated requests
        """
        # Handle short network names
        if network in self.KNOWN_NETWORKS:
            network = self.KNOWN_NETWORKS[network]
            
        # Ensure network has protocol
        if not network.startswith(('http://', 'https://')):
            network = f"https://{network}"
            
        self.network = network.rstrip('/')
        self.access_token = access_token
        self.session = requests.Session()
        
        # Set up default headers
        headers = {
            'User-Agent': 'omics-ai-python-client/0.1.0',
            'Accept': 'application/json'
        }
        
        if self.access_token:
            headers['Authorization'] = f'Bearer {self.access_token}'
            
        self.session.headers.update(headers)
    
    def _make_request(self, method: str, endpoint: str, **kwargs) -> requests.Response:
        """Make an HTTP request to the Explorer API."""
        url = f"{self.network}{endpoint}"
        
        try:
            response = self.session.request(method, url, **kwargs)
            response.raise_for_status()
            return response
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 401:
                raise AuthenticationError(f"Authentication failed: {e}")
            elif e.response.status_code == 403:
                raise AuthenticationError(f"Access forbidden: {e}")
            else:
                raise OmicsAIError(f"HTTP error {e.response.status_code}: {e}")
        except requests.exceptions.RequestException as e:
            raise NetworkError(f"Network error: {e}")
    
    def list_collections(self) -> List[Dict[str, Any]]:
        """
        List all collections in this Explorer network.
        
        Returns:
            List of collection dictionaries with metadata like name, slug, description, etc.
            
        Example:
            >>> collections = client.list_collections()
            >>> for collection in collections:
            ...     print(f"{collection['name']} ({collection['slugName']})")
        """
        response = self._make_request('GET', '/api/collections')
        collections = response.json()
        
        if not isinstance(collections, list):
            raise OmicsAIError("Expected list of collections but got something else")
            
        return collections
    
    def list_tables(self, collection_slug: str) -> List[Dict[str, Any]]:
        """
        List all tables in a collection.
        
        Args:
            collection_slug: The slug name of the collection (e.g., 'gnomad')
            
        Returns:
            List of table dictionaries with metadata like name, size, type, etc.
            
        Example:
            >>> tables = client.list_tables("gnomad")
            >>> for table in tables:
            ...     print(f"{table['display_name']} - {table['size']} rows")
        """
        if not collection_slug:
            raise ValidationError("Collection slug is required")
            
        endpoint = f"/api/collections/{quote(collection_slug)}/tables"
        response = self._make_request('GET', endpoint)
        tables = response.json()
        
        if not isinstance(tables, list):
            raise OmicsAIError("Expected list of tables but got something else")
            
        return tables
    
    def get_schema(self, collection_slug: str, table_name: str) -> Dict[str, Any]:
        """
        Get the schema (field definitions) for a table.
        
        Args:
            collection_slug: The slug name of the collection
            table_name: The qualified table name (e.g., 'collections.gnomad.variants')
            
        Returns:
            Dictionary containing the table schema with field names, types, and metadata
            
        Example:
            >>> schema = client.get_schema("gnomad", "collections.gnomad.variants")
            >>> fields = schema['data_model']['properties']
            >>> for field_name, field_spec in fields.items():
            ...     print(f"{field_name}: {field_spec.get('type', 'unknown')}")
        """
        if not collection_slug or not table_name:
            raise ValidationError("Both collection_slug and table_name are required")
            
        endpoint = f"/api/collection/{quote(collection_slug)}/data-connect/table/{quote(table_name)}/info"
        response = self._make_request('GET', endpoint)
        schema = response.json()
        
        return schema
    
    def get_schema_fields(self, collection_slug: str, table_name: str) -> List[Dict[str, str]]:
        """
        Get a simplified list of fields from a table schema.
        
        Args:
            collection_slug: The slug name of the collection
            table_name: The qualified table name
            
        Returns:
            List of dictionaries with 'field', 'type', and 'sql_type' keys
            
        Example:
            >>> fields = client.get_schema_fields("gnomad", "collections.gnomad.variants")
            >>> for field in fields:
            ...     print(f"{field['field']}: {field['type']}")
        """
        schema = self.get_schema(collection_slug, table_name)
        data_model = schema.get('data_model', {}).get('properties', {})
        
        if not data_model:
            raise OmicsAIError("No schema (data_model.properties) found in response")
            
        fields = []
        for field_name, field_spec in data_model.items():
            # Handle type which can be a string or list
            field_type = field_spec.get('type', '')
            if isinstance(field_type, list):
                field_type = ', '.join(field_type)
            
            # Handle array types with items
            if field_type == 'array' and 'items' in field_spec:
                item_type = field_spec['items'].get('type', '')
                if isinstance(item_type, list):
                    item_type = ', '.join(item_type)
                field_type = f"array<{item_type}>"
            
            fields.append({
                'field': field_name,
                'type': field_type,
                'sql_type': field_spec.get('sqlType', '')
            })
            
        return fields
    
    def query_with_polling(self, 
                          collection_slug: str, 
                          table_name: str, 
                          filters: Optional[Dict[str, Any]] = None,
                          limit: int = 100,
                          offset: int = 0,
                          order_by: Optional[Dict[str, str]] = None,
                          max_polls: int = 10,
                          poll_interval: float = 2.0) -> Dict[str, Any]:
        """
        Query a table with polling for async results.
        
        The query endpoint is asynchronous:
        1. First call returns next_page_token but no data
        2. Poll with the token until data is ready
        3. Eventually get data array + next_page_tokens for pagination
        
        Args:
            collection_slug: The slug name of the collection
            table_name: The qualified table name
            filters: Dictionary of filters to apply (field_name -> filter_spec)
            limit: Maximum number of rows to return (default: 100)
            offset: Number of rows to skip (default: 0)
            order_by: Optional ordering specification {'field': 'column_name', 'direction': 'ASC'|'DESC'}
            max_polls: Maximum number of polling attempts (default: 10)
            poll_interval: Seconds to wait between polls (default: 2.0)
            
        Returns:
            Dictionary containing 'data' (list of rows) and pagination info
        """
        if not collection_slug or not table_name:
            raise ValidationError("Both collection_slug and table_name are required")
            
        if filters is None:
            filters = {}
            
        payload = {
            "tableName": table_name,
            "filters": filters,
            "pagination": {
                "limit": limit,
                "offset": offset
            }
        }
        
        if order_by:
            payload["order"] = order_by
            
        endpoint = f"/api/collections/{quote(collection_slug)}/tables/{quote(table_name)}/filter"
        
        for poll_count in range(max_polls):
            response = self._make_request(
                'POST', 
                endpoint,
                json=payload,
                headers={'Content-Type': 'application/json'}
            )
            
            # The API returns JSON Lines format - extract the final JSON object
            raw_text = response.text
            json_objects = re.findall(r'\{[^}]*\}(?=\s*\{|\s*$)', raw_text, re.DOTALL)
            
            if not json_objects:
                raise OmicsAIError("No valid JSON objects found in response")
                
            try:
                result = json.loads(json_objects[-1])  # Take the last JSON object
            except json.JSONDecodeError as e:
                raise OmicsAIError(f"Failed to parse JSON response: {e}")
            
            # Check if we have data or need to poll
            if 'data' in result and isinstance(result['data'], list):
                return result
            elif 'next_page_token' in result:
                # Update payload with next page token for polling
                payload['next_page_token'] = result['next_page_token']
                if poll_count < max_polls - 1:  # Don't sleep on last attempt
                    time.sleep(poll_interval)
            else:
                raise OmicsAIError(f"Unexpected response format: {list(result.keys())}")
        
        raise OmicsAIError(f"Query timed out after {max_polls} polls ({max_polls * poll_interval}s)")

    def query(self, 
              collection_slug: str, 
              table_name: str, 
              filters: Optional[Dict[str, Any]] = None,
              limit: int = 100,
              offset: int = 0,
              order_by: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """
        Query a table with optional filters and pagination (with auto-polling for async queries).
        
        Args:
            collection_slug: The slug name of the collection
            table_name: The qualified table name
            filters: Dictionary of filters to apply (field_name -> filter_spec)
            limit: Maximum number of rows to return (default: 100)
            offset: Number of rows to skip (default: 0)
            order_by: Optional ordering specification {'field': 'column_name', 'direction': 'ASC'|'DESC'}
            
        Returns:
            Dictionary containing 'data' (list of rows) and pagination info
            
        Note:
            This method automatically handles asynchronous queries by polling for results.
            For more control over polling behavior, use query_with_polling() directly.
            
        Example:
            >>> # Simple query with filters
            >>> results = client.query(
            ...     "gnomad", 
            ...     "collections.gnomad.variants",
            ...     filters={"chrom": [{"operation": "EQ", "value": "chr1", "type": "STRING"}]},
            ...     limit=10
            ... )
            >>> for row in results['data']:
            ...     print(row)
        """
        # Use polling by default to handle async queries
        return self.query_with_polling(collection_slug, table_name, filters, limit, offset, order_by)
    
    def simple_query(self, 
                     collection_slug: str, 
                     table_name: str,
                     **field_filters) -> List[Dict[str, Any]]:
        """
        Perform a simple query using field=value syntax.
        
        This is a convenience method that automatically converts simple
        field=value pairs into the proper filter format.
        
        Args:
            collection_slug: The slug name of the collection
            table_name: The qualified table name
            **field_filters: Simple field=value filters
            
        Returns:
            List of matching rows
            
        Example:
            >>> # Simple equality filters
            >>> results = client.simple_query(
            ...     "gnomad",
            ...     "collections.gnomad.variants", 
            ...     chrom="chr1",
            ...     pos=12345
            ... )
        """
        filters = {}
        for field, value in field_filters.items():
            # Auto-detect type based on value
            if isinstance(value, str):
                field_type = "STRING"
            elif isinstance(value, int):
                field_type = "INTEGER"
            elif isinstance(value, float):
                field_type = "FLOAT"
            elif isinstance(value, bool):
                field_type = "BOOLEAN"
            else:
                field_type = "STRING"
                value = str(value)
                
            filters[field] = [{
                "operation": "EQ",
                "value": value,
                "type": field_type
            }]
            
        result = self.query(collection_slug, table_name, filters=filters)
        return result.get('data', [])
    
    def count(self, 
              collection_slug: str, 
              table_name: str,
              filters: Optional[Dict[str, Any]] = None) -> int:
        """
        Count the number of rows matching the given filters.
        
        Args:
            collection_slug: The slug name of the collection
            table_name: The qualified table name
            filters: Dictionary of filters to apply
            
        Returns:
            Number of matching rows
        """
        if not collection_slug or not table_name:
            raise ValidationError("Both collection_slug and table_name are required")
            
        if filters is None:
            filters = {}
            
        payload = {
            "filters": filters
        }
        
        endpoint = f"/api/collections/{quote(collection_slug)}/tables/{quote(table_name)}/filter/count"
        
        response = self._make_request(
            'POST',
            endpoint, 
            json=payload,
            headers={'Content-Type': 'application/json'}
        )
        
        # Parse the JSON Lines response
        raw_text = response.text
        json_objects = re.findall(r'\{[^}]*\}(?=\s*\{|\s*$)', raw_text, re.DOTALL)
        
        if not json_objects:
            raise OmicsAIError("No valid JSON objects found in count response")
            
        try:
            result = json.loads(json_objects[-1])
            return result.get('count', 0)
        except (json.JSONDecodeError, KeyError):
            raise OmicsAIError("Failed to parse count from response")
    
    def set_access_token(self, token: str):
        """
        Set or update the access token for authenticated requests.
        
        Args:
            token: The access token
        """
        self.access_token = token
        self.session.headers['Authorization'] = f'Bearer {token}'
    
    def clear_access_token(self):
        """Remove the access token."""
        self.access_token = None
        if 'Authorization' in self.session.headers:
            del self.session.headers['Authorization']