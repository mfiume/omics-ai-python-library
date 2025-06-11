"""
Omics AI Explorer Python Library

A simple Python library for interacting with Omics AI Explorer instances.
Supports multiple networks like hifisolves.org, neuroscience.ai, and cloud.parkinsonsroadmap.org.
"""

from typing import Dict, List, Optional, Any
from .client import OmicsAIClient
from .exceptions import OmicsAIError, AuthenticationError, NetworkError, ValidationError

__version__ = "0.1.0"

# Export both class-based and functional APIs
__all__ = [
    "OmicsAIClient", 
    "OmicsAIError", 
    "AuthenticationError", 
    "NetworkError", 
    "ValidationError",
    # Functional API
    "list_collections",
    "list_tables", 
    "get_schema_fields",
    "query",
    "count"
]


# Functional API - no need to create client instances
def list_collections(network: str, access_token: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    List all collections in an Explorer network.
    
    Args:
        network: Network URL (e.g., 'hifisolves.org') or short name (e.g., 'hifisolves')
        access_token: Optional access token for authenticated requests
        
    Returns:
        List of collection dictionaries
        
    Example:
        >>> collections = list_collections("hifisolves")
        >>> for collection in collections:
        ...     print(collection['name'])
    """
    client = OmicsAIClient(network, access_token)
    return client.list_collections()


def list_tables(network: str, collection_slug: str, access_token: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    List all tables in a collection.
    
    Args:
        network: Network URL or short name
        collection_slug: The slug name of the collection
        access_token: Optional access token for authenticated requests
        
    Returns:
        List of table dictionaries
        
    Example:
        >>> tables = list_tables("hifisolves", "gnomad")
        >>> for table in tables:
        ...     print(table['display_name'])
    """
    client = OmicsAIClient(network, access_token)
    return client.list_tables(collection_slug)


def get_schema_fields(network: str, collection_slug: str, table_name: str, 
                     access_token: Optional[str] = None) -> List[Dict[str, str]]:
    """
    Get the schema fields for a table.
    
    Args:
        network: Network URL or short name
        collection_slug: The slug name of the collection  
        table_name: The qualified table name
        access_token: Optional access token for authenticated requests
        
    Returns:
        List of field dictionaries with 'field', 'type', and 'sql_type' keys
        
    Example:
        >>> fields = get_schema_fields("hifisolves", "gnomad", "collections.gnomad.variants")
        >>> for field in fields:
        ...     print(f"{field['field']}: {field['type']}")
    """
    client = OmicsAIClient(network, access_token)
    return client.get_schema_fields(collection_slug, table_name)


def query(network: str, collection_slug: str, table_name: str,
          filters: Optional[Dict[str, Any]] = None,
          limit: int = 100,
          offset: int = 0,
          order_by: Optional[Dict[str, str]] = None,
          max_polls: int = 10,
          poll_interval: float = 2.0,
          access_token: Optional[str] = None) -> Dict[str, Any]:
    """
    Query a table with optional filters and pagination.
    
    Args:
        network: Network URL or short name
        collection_slug: The slug name of the collection
        table_name: The qualified table name
        filters: Dictionary of filters to apply
        limit: Maximum number of rows to return (default: 100)
        offset: Number of rows to skip (default: 0)
        order_by: Optional ordering specification
        max_polls: Maximum number of polling attempts (default: 10)
        poll_interval: Seconds to wait between polls (default: 2.0)
        access_token: Optional access token for authenticated requests
        
    Returns:
        Dictionary containing 'data' (list of rows) and pagination info
        
    Example:
        >>> result = query("hifisolves", "gnomad", "collections.gnomad.variants", limit=10)
        >>> for row in result['data']:
        ...     print(row)
    """
    client = OmicsAIClient(network, access_token)
    return client.query(collection_slug, table_name, filters, limit, offset, order_by, max_polls, poll_interval)


def count(network: str, collection_slug: str, table_name: str,
          filters: Optional[Dict[str, Any]] = None,
          access_token: Optional[str] = None) -> int:
    """
    Count the number of rows matching the given filters.
    
    Args:
        network: Network URL or short name
        collection_slug: The slug name of the collection
        table_name: The qualified table name
        filters: Dictionary of filters to apply
        access_token: Optional access token for authenticated requests
        
    Returns:
        Number of matching rows
        
    Example:
        >>> total = count("hifisolves", "gnomad", "collections.gnomad.variants")
        >>> print(f"Total variants: {total}")
    """
    client = OmicsAIClient(network, access_token)
    return client.count(collection_slug, table_name, filters)