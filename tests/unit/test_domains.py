"""Unit tests for DomainsAPI."""

from __future__ import annotations

import pytest
from namecheap._api.domains import DomainsAPI


@pytest.mark.unit
class TestSetNameservers:
    """Test DomainsAPI.set_nameservers method."""

    def test_set_custom_nameservers(self, mocker):
        """Test setting custom nameservers."""
        mock_request = mocker.patch.object(DomainsAPI, "_request", return_value={"@Updated": "true"})
        api = mocker.Mock(spec=DomainsAPI)
        api._request = mock_request

        domains = DomainsAPI.__new__(DomainsAPI)
        domains._request = mock_request

        result = domains.set_nameservers(
            "example.com",
            ["ns1.cloudflare.com", "ns2.cloudflare.com"]
        )

        assert result is True
        mock_request.assert_called_once_with(
            "namecheap.domains.dns.setCustom",
            {
                "SLD": "example",
                "TLD": "com",
                "Nameservers": "ns1.cloudflare.com,ns2.cloudflare.com",
            },
            path="DomainDNSSetCustomResult",
        )

    def test_set_single_nameserver(self, mocker):
        """Test setting a single custom nameserver."""
        mock_request = mocker.patch.object(DomainsAPI, "_request", return_value={"@Updated": "true"})
        domains = DomainsAPI.__new__(DomainsAPI)
        domains._request = mock_request

        result = domains.set_nameservers(
            "example.com",
            ["ns1.custom.com"]
        )

        assert result is True
        mock_request.assert_called_once_with(
            "namecheap.domains.dns.setCustom",
            {
                "SLD": "example",
                "TLD": "com",
                "Nameservers": "ns1.custom.com",
            },
            path="DomainDNSSetCustomResult",
        )

    def test_reset_to_default(self, mocker):
        """Test resetting to Namecheap BasicDNS."""
        mock_request = mocker.patch.object(DomainsAPI, "_request", return_value={"@Updated": "true"})
        domains = DomainsAPI.__new__(DomainsAPI)
        domains._request = mock_request

        result = domains.set_nameservers("example.com", [], reset=True)

        assert result is True
        mock_request.assert_called_once_with(
            "namecheap.domains.dns.setDefault",
            {"SLD": "example", "TLD": "com"},
            path="DomainDNSSetCustomResult",
        )

    def test_reset_ignores_nameservers(self, mocker):
        """Test that reset=True ignores provided nameservers."""
        mock_request = mocker.patch.object(DomainsAPI, "_request", return_value={"@Updated": "true"})
        domains = DomainsAPI.__new__(DomainsAPI)
        domains._request = mock_request

        result = domains.set_nameservers(
            "example.com",
            ["ns1.cloudflare.com"],
            reset=True,
        )

        assert result is True
        mock_request.assert_called_once_with(
            "namecheap.domains.dns.setDefault",
            {"SLD": "example", "TLD": "com"},
            path="DomainDNSSetCustomResult",
        )

    def test_too_many_nameservers(self):
        """Test that more than 5 nameservers raises error."""
        from namecheap._api.domains import DomainsAPI
        domains = DomainsAPI.__new__(DomainsAPI)

        with pytest.raises(ValueError, match="Maximum 5"):
            domains.set_nameservers(
                "example.com",
                [f"ns{i}.example.com" for i in range(6)],
            )

    def test_empty_nameservers_without_reset(self):
        """Test that empty nameservers without reset raises error."""
        domains = DomainsAPI.__new__(DomainsAPI)

        with pytest.raises(ValueError, match="At least one"):
            domains.set_nameservers("example.com", [])

    def test_invalid_domain(self):
        """Test that invalid domain raises error."""
        domains = DomainsAPI.__new__(DomainsAPI)

        with pytest.raises(ValueError, match="Invalid domain"):
            domains.set_nameservers("notadomain", ["ns1.example.com"])

    def test_domain_with_subdomain(self, mocker):
        """Test strip SLD/TLD from full domain."""
        mock_request = mocker.patch.object(DomainsAPI, "_request", return_value={"@Updated": "true"})
        domains = DomainsAPI.__new__(DomainsAPI)
        domains._request = mock_request

        domains.set_nameservers(
            "www.hochguertel.cyou",
            ["ns1.cloudflare.com"],
        )

        mock_request.assert_called_once_with(
            "namecheap.domains.dns.setCustom",
            {
                "SLD": "hochguertel",
                "TLD": "cyou",
                "Nameservers": "ns1.cloudflare.com",
            },
            path="DomainDNSSetCustomResult",
        )

    def test_failed_api_call_returns_false(self, mocker):
        """Test that failed API call returns False."""
        mock_request = mocker.patch.object(DomainsAPI, "_request", return_value={})
        domains = DomainsAPI.__new__(DomainsAPI)
        domains._request = mock_request

        result = domains.set_nameservers(
            "example.com",
            ["ns1.example.com"],
        )

        assert result is False

    def test_multi_tld_domain(self, mocker):
        """Test domain with multi-part TLD."""
        mock_request = mocker.patch.object(DomainsAPI, "_request", return_value={"@Updated": "true"})
        domains = DomainsAPI.__new__(DomainsAPI)
        domains._request = mock_request

        domains.set_nameservers(
            "example.co.uk",
            ["ns1.example.com"],
        )

        mock_request.assert_called_once_with(
            "namecheap.domains.dns.setCustom",
            {
                "SLD": "example",
                "TLD": "co.uk",
                "Nameservers": "ns1.example.com",
            },
            path="DomainDNSSetCustomResult",
        )
