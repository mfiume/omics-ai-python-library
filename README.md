# Omics AI Explorer Python Library

A simple Python client library for interacting with [Omics AI Explorer](https://omics.ai) instances. This library provides easy access to genomics data across multiple Explorer networks including HiFi Solves, Neuroscience AI, and Parkinson's Roadmap.

## Features

- **Simple API**: Intuitive methods for common operations
- **Multiple Networks**: Support for hifisolves.org, neuroscience.ai, cloud.parkinsonsroadmap.org, and more
- **Comprehensive Operations**: List collections, browse tables, get schemas, and query data
- **Authentication**: Support for authenticated requests with access tokens
- **Type Hints**: Full type annotations for better IDE support
- **Error Handling**: Clear error messages and exception types

## Installation

```bash
pip install omics-ai-explorer
```

Or install from source:

```bash
git clone https://github.com/dnastack/omics-ai-cli.git
cd omics-ai-cli
pip install -e .
```

## Quick Start

```python
from omics_ai import OmicsAIClient

# Connect to HiFi Solves
client = OmicsAIClient("hifisolves.org")

# List all collections
collections = client.list_collections()
for collection in collections:
    print(f"{collection['name']} ({collection['slugName']})")

# List tables in a collection
tables = client.list_tables("gnomad")
for table in tables:
    print(f"{table['display_name']} - {table['size']} rows")

# Get table schema
schema_fields = client.get_schema_fields("gnomad", "collections.gnomad.variants")
for field in schema_fields:
    print(f"{field['field']}: {field['type']}")

# Simple query
results = client.simple_query(
    "gnomad",
    "collections.gnomad.variants",
    chrom="chr1",
    pos=12345
)
```

## Supported Networks

The library comes pre-configured with several known Explorer networks:

```python
# Using short names
client = OmicsAIClient("hifisolves")      # -> hifisolves.org
client = OmicsAIClient("neuroscience")    # -> neuroscience.ai
client = OmicsAIClient("parkinsons")      # -> cloud.parkinsonsroadmap.org
client = OmicsAIClient("biomedical")      # -> biomedical.ai

# Or use full domains
client = OmicsAIClient("hifisolves.org")
client = OmicsAIClient("custom-domain.com")
```

## Core Operations

### 1. List Collections

```python
collections = client.list_collections()

# Collections contain metadata like:
# - name: Human-readable name
# - slugName: URL-safe identifier
# - description: Detailed description
# - createdAt/updatedAt: Timestamps
# - tags: Associated tags
```

### 2. List Tables

```python
tables = client.list_tables("collection-slug")

# Tables contain metadata like:
# - qualified_table_name: Full table identifier
# - display_name: Human-readable name
# - type: Table type
# - size: Number of rows
# - description: Table description
```

### 3. Get Table Schema

```python
# Get full schema object
schema = client.get_schema("collection-slug", "table-name")

# Get simplified field list
fields = client.get_schema_fields("collection-slug", "table-name")
for field in fields:
    print(f"{field['field']}: {field['type']} ({field['sql_type']})")
```

### 4. Query Data

#### Simple Queries

```python
# Simple equality filters
results = client.simple_query(
    "gnomad",
    "collections.gnomad.variants",
    chrom="chr1",
    pos=12345
)

# Results is a list of dictionaries (rows)
for row in results:
    print(row)
```

#### Advanced Queries

```python
# Complex filters with operators
filters = {
    "chrom": [{"operation": "EQ", "value": "chr1", "type": "STRING"}],
    "pos": [{"operation": "GT", "value": 1000000, "type": "INTEGER"}],
    "af": [{"operation": "LT", "value": 0.01, "type": "FLOAT"}]
}

results = client.query(
    "gnomad",
    "collections.gnomad.variants",
    filters=filters,
    limit=50,
    order_by={"field": "pos", "direction": "ASC"}
)

# Access data and pagination info
data = results['data']
pagination = results.get('pagination', {})
```

#### Count Results

```python
count = client.count(
    "gnomad",
    "collections.gnomad.variants",
    filters={"chrom": [{"operation": "EQ", "value": "chr1", "type": "STRING"}]}
)
print(f"Found {count} variants on chr1")
```

## Authentication

For collections requiring authentication, provide an access token:

```python
client = OmicsAIClient("hifisolves.org", access_token="your-token-here")

# Or set it later
client.set_access_token("your-token-here")

# Clear authentication
client.clear_access_token()
```

## Filter Operations

The library supports various filter operations:

- `EQ`: Equals
- `NEQ`: Not equals
- `GT`: Greater than
- `GTE`: Greater than or equal
- `LT`: Less than
- `LTE`: Less than or equal
- `LIKE`: String pattern matching
- `REGEX`: Regular expression matching
- `BETWEEN`: Range queries
- `NULL`: Is null
- `NOT_NULL`: Is not null

## Data Types

When creating filters, specify the appropriate data type:

- `STRING`: Text data
- `INTEGER`: Whole numbers
- `FLOAT`: Decimal numbers
- `BOOLEAN`: True/false values
- `DATE`: Date values
- `DATE-TIME`: Date and time values

## Error Handling

The library provides specific exception types:

```python
from omics_ai import OmicsAIClient, OmicsAIError, AuthenticationError, NetworkError

try:
    client = OmicsAIClient("hifisolves.org")
    results = client.simple_query("collection", "table", field="value")
except AuthenticationError:
    print("Authentication failed - check your access token")
except NetworkError as e:
    print(f"Network error: {e}")
except OmicsAIError as e:
    print(f"API error: {e}")
```

## Examples

### Finding Variants by Position

```python
# Search for variants at a specific genomic position
client = OmicsAIClient("hifisolves")
variants = client.simple_query(
    "gnomad",
    "collections.gnomad.variants",
    chrom="chr17",
    pos=43094692  # BRCA1 region
)

for variant in variants:
    print(f"{variant['chrom']}:{variant['pos']} {variant['ref']}>{variant['alt']}")
```

### Exploring Collection Structure

```python
# Discover what's available in a network
client = OmicsAIClient("neuroscience")

print("Available collections:")
for collection in client.list_collections():
    print(f"  {collection['slugName']}: {collection['name']}")
    
    # Show tables in each collection
    tables = client.list_tables(collection['slugName'])
    for table in tables[:3]:  # Show first 3 tables
        print(f"    - {table['display_name']} ({table['size']} rows)")
```

### Schema Inspection

```python
# Understand table structure before querying
client = OmicsAIClient("hifisolves")
fields = client.get_schema_fields("gnomad", "collections.gnomad.variants")

print("Available fields:")
for field in fields:
    print(f"  {field['field']}: {field['type']}")
    
# Now you know what fields are available for filtering
```

## Development

To set up for development:

```bash
git clone https://github.com/dnastack/omics-ai-cli.git
cd omics-ai-cli
pip install -e ".[dev]"

# Run tests
pytest

# Format code
black omics_ai/

# Type checking
mypy omics_ai/
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For questions and support:

- GitHub Issues: [https://github.com/dnastack/omics-ai-cli/issues](https://github.com/dnastack/omics-ai-cli/issues)
- Documentation: [https://omics.ai](https://omics.ai)
- Email: support@dnastack.com