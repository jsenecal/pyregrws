"""Tests for custom types in regrws.models.types"""

from ipaddress import IPv4Address, IPv6Address

import pytest

from regrws.models.types import _validate_ip_address


class TestValidateIPAddress:
    """Tests for the _validate_ip_address function."""

    def test_valid_ipv4(self):
        """Test standard IPv4 address parsing."""
        result = _validate_ip_address("192.168.1.1")
        assert result == IPv4Address("192.168.1.1")

    def test_valid_ipv6(self):
        """Test standard IPv6 address parsing."""
        result = _validate_ip_address("2001:db8::1")
        assert result == IPv6Address("2001:db8::1")

    def test_zero_padded_ipv4(self):
        """Test zero-padded IPv4 address parsing (ARIN format)."""
        result = _validate_ip_address("010.000.000.001")
        assert result == IPv4Address("10.0.0.1")

    def test_zero_padded_ipv4_mixed(self):
        """Test partially zero-padded IPv4 address."""
        result = _validate_ip_address("192.168.001.010")
        assert result == IPv4Address("192.168.1.10")

    def test_invalid_ip_non_numeric_octet(self):
        """Test that non-numeric octets raise ValueError."""
        with pytest.raises(ValueError, match="Invalid IP address"):
            _validate_ip_address("192.168.abc.1")

    def test_invalid_ip_completely_invalid(self):
        """Test that completely invalid strings raise ValueError."""
        with pytest.raises(ValueError, match="Invalid IP address"):
            _validate_ip_address("not-an-ip-address")
