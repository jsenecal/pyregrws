# pyregrws Examples

This directory contains practical examples demonstrating how to use the pyregrws library for common ARIN Reg-RWS operations.

## Examples

### reassignment_example.py

A comprehensive example showing how to perform IP network reassignments using ARIN's "Reassign Simple" method. This example demonstrates:

- Finding existing ARIN network records
- Creating customer records for reassignments  
- Performing network reassignments
- Error handling and validation
- Dry-run capabilities for testing

**Key Features:**
- Standalone script (no external dependencies beyond pyregrws)
- Support for both IPv4 and IPv6 networks
- Automatic network name generation
- Customer record creation with proper addressing
- Comprehensive error handling

**Usage:**
```bash
# Set your ARIN API key
export ARIN_API_KEY="your-api-key-here"

# Run the example
python reassignment_example.py
```

**Configuration:**
- Modify the `network` variable to use your own IP space
- Update `customer_info` with real customer details
- Change `base_url` from test environment to production when ready
- Uncomment the actual reassignment line when ready to perform real operations

## Getting Started

1. **Get ARIN API Access:**
   - Register for an ARIN Online account
   - Request API access through ARIN
   - Obtain your API key

2. **Test Environment:**
   - Use `https://reg.ote.arin.net/rws` for testing
   - Use `https://reg.arin.net/rws` for production

3. **Required Permissions:**
   - You must have authority over the IP space you're trying to reassign
   - Ensure your ARIN account has appropriate permissions

## Important Notes

- **Always test first:** Use the test environment and dry-run capabilities
- **IP Authority:** You can only reassign networks you have authority over
- **Rate Limits:** Be mindful of ARIN API rate limits
- **Documentation:** Follow ARIN's guidelines for network reassignments

## Error Handling

The examples include comprehensive error handling for common scenarios:
- Network not found
- Insufficient permissions
- Invalid customer data
- API communication errors

## Support

For questions about ARIN policies and procedures, consult:
- [ARIN Documentation](https://www.arin.net/resources/manage/regrws/)
- [ARIN Number Resource Policy Manual](https://www.arin.net/resources/manage/nrpm/)