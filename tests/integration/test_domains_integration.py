"""Integration tests for DomainsAPI operations."""

from __future__ import annotations

import pytest
from tests.utils.test_helpers import MockResponse


def make_set_custom_response(domain: str) -> MockResponse:
    """Create a mock setCustom API response."""
    return MockResponse(
        text=f"""<?xml version="1.0" encoding="UTF-8"?>
<ApiResponse Status="OK">
    <Errors/>
    <CommandResponse Type="namecheap.domains.dns.setCustom">
        <DomainDNSSetCustomResult Domain="{domain}" Updated="true"/>
    </CommandResponse>
</ApiResponse>"""
    )


def make_set_default_response(domain: str) -> MockResponse:
    """Create a mock setDefault API response."""
    return MockResponse(
        text=f"""<?xml version="1.0" encoding="UTF-8"?>
<ApiResponse Status="OK">
    <Errors/>
    <CommandResponse Type="namecheap.domains.dns.setDefault">
        <DomainDNSSetCustomResult Domain="{domain}" Updated="true"/>
    </CommandResponse>
</ApiResponse>"""
    )


@pytest.fixture
def client_kwargs():
    """Default kwargs for Namecheap client."""
    return {
        "api_key": "test_api_key_123456789",
        "username": "testuser",
        "api_user": "testuser",
        "client_ip": "192.0.2.1",
        "sandbox": True,
    }


@pytest.mark.integration
class TestSetNameserversIntegration:
    """Integration tests for set_nameservers with mocked HTTP."""

    @pytest.fixture
    def mock_http(self, mocker):
        """Mock httpx.Client and return a pre-configured mock."""
        mock_response = mocker.Mock()
        mock_response.text = ""
        mock_response.raise_for_status.return_value = None

        mock_client = mocker.patch("httpx.Client")
        mock_instance = mock_client.return_value.__enter__.return_value
        mock_instance.get.return_value = mock_response
        return mock_instance, mock_response

    def test_set_custom_sends_correct_http_request(self, mocker, client_kwargs):
        """Test that set_nameservers sends correct HTTP GET params."""
        from namecheap import Namecheap

        mock_response = mocker.Mock()
        mock_response.text = make_set_custom_response("example.com").text
        mock_response.raise_for_status.return_value = None

        mock_client = mocker.patch("httpx.Client")
        mock_client.return_value.get.return_value = mock_response

        nc = Namecheap(**client_kwargs)
        result = nc.domains.set_nameservers(
            "example.com",
            ["ns1.cloudflare.com", "ns2.cloudflare.com"]
        )

        assert result is True
        mock_client.return_value.get.assert_called_once()
        call_params = mock_client.return_value.get.call_args[1]["params"]
        assert call_params["Command"] == "namecheap.domains.dns.setCustom"
        assert call_params["SLD"] == "example"
        assert call_params["TLD"] == "com"
        assert call_params["Nameservers"] == "ns1.cloudflare.com,ns2.cloudflare.com"

    def test_reset_sends_correct_http_request(self, mocker, client_kwargs):
        """Test that reset=True sends setDefault command."""
        from namecheap import Namecheap

        mock_response = mocker.Mock()
        mock_response.text = make_set_default_response("example.com").text
        mock_response.raise_for_status.return_value = None

        mock_client = mocker.patch("httpx.Client")
        mock_client.return_value.get.return_value = mock_response

        nc = Namecheap(**client_kwargs)
        result = nc.domains.set_nameservers("example.com", [], reset=True)

        assert result is True
        mock_client.return_value.get.assert_called_once()
        call_params = mock_client.return_value.get.call_args[1]["params"]
        assert call_params["Command"] == "namecheap.domains.dns.setDefault"
        assert "Nameservers" not in call_params

    def test_sandbox_uses_sandbox_url(self, mocker, client_kwargs):
        """Test that sandbox mode uses sandbox API URL."""
        from namecheap import Namecheap

        mock_response = mocker.Mock()
        mock_response.text = make_set_custom_response("example.com").text
        mock_response.raise_for_status.return_value = None

        mock_client = mocker.patch("httpx.Client")
        mock_client.return_value.get.return_value = mock_response

        nc = Namecheap(**client_kwargs)
        nc.domains.set_nameservers("example.com", ["ns1.cloudflare.com"])

        call_url = mock_client.return_value.get.call_args[0][0]
        assert "sandbox" in call_url

    def test_production_uses_production_url(self, mocker, client_kwargs):
        """Test that production mode uses production API URL."""
        from namecheap import Namecheap

        mock_response = mocker.Mock()
        mock_response.text = make_set_custom_response("example.com").text
        mock_response.raise_for_status.return_value = None

        mock_client = mocker.patch("httpx.Client")
        mock_client.return_value.get.return_value = mock_response

        client_kwargs["sandbox"] = False
        nc = Namecheap(**client_kwargs)
        nc.domains.set_nameservers("example.com", ["ns1.cloudflare.com"])

        call_url = mock_client.return_value.get.call_args[0][0]
        assert "sandbox" not in call_url
        assert "api.namecheap.com" in call_url

    def test_api_error_raises_exception(self, mocker, client_kwargs):
        """Test that API error response raises NamecheapError."""
        from namecheap import Namecheap

        mock_response = mocker.Mock()
        mock_response.text = """<?xml version="1.0" encoding="UTF-8"?>
<ApiResponse Status="ERROR">
    <Errors>
        <Error Number="201116">Domain is not in your account</Error>
    </Errors>
</ApiResponse>"""
        mock_response.raise_for_status.return_value = None

        mock_client = mocker.patch("httpx.Client")
        mock_client.return_value.get.return_value = mock_response

        nc = Namecheap(**client_kwargs)
        with pytest.raises(Exception):
            nc.domains.set_nameservers("example.com", ["ns1.cloudflare.com"])

    def test_includes_auth_params(self, mocker, client_kwargs):
        """Test that auth params are sent with every request."""
        from namecheap import Namecheap

        mock_response = mocker.Mock()
        mock_response.text = make_set_custom_response("example.com").text
        mock_response.raise_for_status.return_value = None

        mock_client = mocker.patch("httpx.Client")
        mock_client.return_value.get.return_value = mock_response

        nc = Namecheap(**client_kwargs)
        nc.domains.set_nameservers("example.com", ["ns1.cloudflare.com"])

        call_params = mock_client.return_value.get.call_args[1]["params"]
        assert call_params["ApiUser"] == "testuser"
        assert call_params["ApiKey"] == "test_api_key_123456789"
        assert call_params["UserName"] == "testuser"
        assert call_params["ClientIp"] == "192.0.2.1"
