# pyregrws

[![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/jsenecal/pyregrws/ci.yml?label=CI&style=for-the-badge)](https://github.com/jsenecal/pyregrws/actions/workflows/ci.yml)[![PyPI](https://img.shields.io/pypi/v/pyregrws?style=for-the-badge)](https://pypi.org/project/pyregrws/)[![Codecov](https://img.shields.io/codecov/c/github/jsenecal/pyregrws?style=for-the-badge)](https://codecov.io/github/jsenecal/pyregrws)

A Python library for interacting with ARIN's Reg-RWS (Registry RESTful Web Service) API. This library provides pydantic-xml models for ARIN payloads and a comprehensive REST client for CRUD operations on ARIN resources like POCs, Customers, Organizations, and Networks.

## Features

- **Type-safe models**: Built with pydantic-xml for robust XML serialization/deserialization
- **Complete CRUD operations**: Create, read, update, and delete ARIN resources
- **Automatic manager integration**: Each model type has an associated manager for API operations
- **Error handling**: Built-in error response handling with proper HTTP status code mapping
- **Environment configuration**: Configurable via environment variables with sensible defaults

## Installation

Install from PyPI using pip:

```bash
pip install pyregrws
```

Or using poetry:

```bash
poetry add pyregrws
```

## Quick Start

```python
from regrws.api.core import Api
from regrws.models import Poc, Org, Net, Customer

# Initialize the API client
api = Api(
    base_url="https://reg.arin.net/",  # Optional, defaults to ARIN production
    api_key="your-api-key-here"           # Or set REGRWS_API_KEY env var
)

# Retrieve a POC by handle
poc = api.poc.from_handle("EXAMPLE-ARIN")
print(f"POC: {poc.first_name} {poc.last_name}")

# Create a new POC
new_poc = api.poc.create(
    contact_type="PERSON",
    first_name="John",
    last_name="Doe",
    company_name="Example Corp",
    iso3166_1={"name": "United States", "code2": "US", "code3": "USA", "e164": "1"},
    street_address=[{"line": "123 Main St"}],
    city="Anytown",
    iso3166_2="VA",
    postal_code="12345",
    phones=[{"type": {"code": "O"}, "number": "555-123-4567"}]
)

# Update and save changes
poc.city = "New City"
updated_poc = poc.save()

# Delete a resource
poc.delete()
```

## Configuration

The library can be configured via environment variables or by passing parameters directly to the `Api` class:

### Environment Variables

- `REGRWS_BASE_URL`: Base URL for the ARIN Reg-RWS API (default: `https://reg.arin.net/`)
- `REGRWS_API_KEY`: Your ARIN API key (required)

> **Warning:** For testing purposes, use ARIN's Operational Test and Evaluation (OTE) environment (`https://reg.ote.arin.net/`) instead of the production URL. The OTE environment provides a safe sandbox that will not affect real registration data.

### Direct Configuration

```python
from regrws.api.core import Api
from regrws.settings import Settings

# Method 1: Pass parameters directly
api = Api(
    base_url="https://reg.arin.net/",
    api_key="your-api-key"
)

# Method 2: Use Settings object
settings = Settings(
    base_url="https://reg.arin.net/",
    api_key="your-api-key"
)
api = Api(settings=settings)
```

## API Reference

### Core Classes

#### Api

The main entry point for the library. Automatically creates manager instances for each supported model type.

```python
api = Api(base_url=None, api_key=None, settings=None)
```

**Attributes:**
- `poc`: Manager for POC operations
- `org`: Manager for Organization operations  
- `net`: Manager for Network operations
- `customer`: Manager for Customer operations

#### BaseManager

All model managers inherit from `BaseManager` and provide these methods:

- `create(**kwargs)`: Create a new resource
- `from_handle(handle)`: Retrieve a resource by handle
- `save(instance)`: Update an existing resource
- `delete(instance)`: Delete a resource

### Models

All models inherit from `BaseModel` which provides:

- `save()`: Save changes to the resource
- `delete()`: Delete the resource
- `absolute_url`: Get the full API URL for this resource
- `manager`: Access to the associated API manager

## Currently Supported Payloads

### Core Resources
- [POC](https://www.arin.net/resources/manage/regrws/payloads/#poc-payload) - Point of Contact
- [Customer](https://www.arin.net/resources/manage/regrws/payloads/#customer-payload) - Customer records
- [ORG](https://www.arin.net/resources/manage/regrws/payloads/#org-payload) - Organization records
- [NET](https://www.arin.net/resources/manage/regrws/payloads/#net-payload) - Network records
- [NET Block](https://www.arin.net/resources/manage/regrws/payloads/#net-block-payload) - Network block records
- [POC Link](https://www.arin.net/resources/manage/regrws/payloads/#poc-link-payload) - POC associations

### Ticketing
- [Ticketed Request Payload](https://www.arin.net/resources/manage/regrws/payloads/#ticketed-request-payload)
- [Ticket Payload](https://www.arin.net/resources/manage/regrws/payloads/#ticket-payload)

### Error Handling
- [Error](https://www.arin.net/resources/manage/regrws/payloads/#error-payload) - API error responses

## Examples

### Working with POCs

```python
# Retrieve an existing POC
poc = api.poc.from_handle("EXAMPLE-ARIN")

# Create a new person POC
person_poc = api.poc.create(
    contact_type="PERSON",
    first_name="Jane",
    last_name="Smith",
    company_name="ACME Corp",
    iso3166_1={"name": "United States", "code2": "US", "code3": "USA", "e164": "1"},
    street_address=[{"line": "456 Oak Ave"}, {"line": "Suite 100"}],
    city="Springfield",
    iso3166_2="IL", 
    postal_code="62701",
    phones=[
        {"type": {"code": "O"}, "number": "217-555-0123"},
        {"type": {"code": "F"}, "number": "217-555-0124"}
    ],
    comment=[{"line": "Technical contact for ACME Corp"}]
)

# Create a role POC
role_poc = api.poc.create(
    contact_type="ROLE",
    last_name="Network Operations Center",  # Role name goes in last_name
    company_name="ACME Corp",
    iso3166_1={"name": "United States", "code2": "US", "code3": "USA", "e164": "1"},
    street_address=[{"line": "789 Tech Dr"}],
    city="Austin",
    iso3166_2="TX",
    postal_code="78701",
    phones=[{"type": {"code": "O"}, "number": "512-555-0100"}]
)
```

### Working with Organizations

```python
# Retrieve an organization
org = api.org.from_handle("EXAMPLE-ARIN")

# Update organization details
org.company_name = "Updated Company Name"
updated_org = org.save()
```

### Working with Networks

```python
# Retrieve a network
net = api.net.from_handle("NET-192-0-2-0-1")

# Update network information
net.net_name = "UPDATED-NET-NAME"
updated_net = net.save()
```

### Error Handling

```python
from regrws.models import Error

try:
    poc = api.poc.from_handle("NONEXISTENT-HANDLE")
except Exception as e:
    # The library automatically handles error responses
    print(f"Error occurred: {e}")
```

## Development

### Setup

```bash
# Clone the repository
git clone https://github.com/jsenecal/pyregrws.git
cd pyregrws

# Install dependencies
poetry install
```

### Running Tests

```bash
# Run all tests with coverage
poetry run pytest --cov -n 2 --cov-report xml --cov-report term-missing

# Run a specific test
poetry run pytest tests/test_api.py::TestAPI::test_manager_from_handle
```

### Code Quality

```bash
# Lint code
poetry run ruff check

# Format code  
poetry run ruff format
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests for your changes
5. Ensure all tests pass and code is formatted
6. Commit your changes (`git commit -m 'Add amazing feature'`)
7. Push to the branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## Links

- [ARIN Reg-RWS Documentation](https://www.arin.net/resources/manage/regrws/)
- [ARIN Reg-RWS Payloads](https://www.arin.net/resources/manage/regrws/payloads/)
- [PyPI Package](https://pypi.org/project/pyregrws/)
- [GitHub Repository](https://github.com/jsenecal/pyregrws)
