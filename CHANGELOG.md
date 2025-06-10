# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2025-01-10

### Added
- Initial release of Omics AI Explorer Python library
- Support for multiple Explorer networks (hifisolves.org, neuroscience.ai, biomedical.ai, etc.)
- Core operations: list collections, list tables, get schema, query data
- Authentication support with access tokens
- Simple and advanced query interfaces
- Comprehensive error handling with custom exception types
- Type hints for better IDE support
- Examples and documentation
- Support for short network names (e.g., "hifisolves" → "hifisolves.org")

### Features
- `OmicsAIClient` - Main client class for interacting with Explorer instances
- `list_collections()` - Browse available collections across networks
- `list_tables()` - List tables within collections
- `get_schema()` - Retrieve table schemas and field definitions
- `query()` - Perform complex queries with filters and pagination
- `simple_query()` - Easy field=value query interface
- `count()` - Count results without fetching all data
- Authentication methods for protected collections
- Pre-configured support for known Explorer networks

### Documentation
- Comprehensive README with usage examples
- Basic usage examples for getting started
- Advanced query examples with complex filters
- HiFi Solves specific examples including allele frequency lookups