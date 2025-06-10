"""
Basic tests for the OmicsAIClient.
"""

import pytest
from unittest.mock import Mock, patch
from omics_ai import OmicsAIClient, OmicsAIError, NetworkError, ValidationError


class TestOmicsAIClient:
    """Test cases for OmicsAIClient."""
    
    def test_client_initialization(self):
        """Test client initialization with different network formats."""
        # Test with full URL
        client = OmicsAIClient("https://hifisolves.org")
        assert client.network == "https://hifisolves.org"
        
        # Test with domain only
        client = OmicsAIClient("hifisolves.org")
        assert client.network == "https://hifisolves.org"
        
        # Test with short name
        client = OmicsAIClient("hifisolves")
        assert client.network == "https://hifisolves.org"
    
    def test_known_networks(self):
        """Test that known network short names resolve correctly."""
        test_cases = [
            ("hifisolves", "https://hifisolves.org"),
            ("neuroscience", "https://neuroscience.ai"),
            ("parkinsons", "https://cloud.parkinsonsroadmap.org"),
            ("biomedical", "https://biomedical.ai"),
        ]
        
        for short_name, expected_url in test_cases:
            client = OmicsAIClient(short_name)
            assert client.network == expected_url
    
    def test_access_token_management(self):
        """Test access token setting and clearing."""
        client = OmicsAIClient("hifisolves")
        
        # Test setting token
        test_token = "test-token-123"
        client.set_access_token(test_token)
        assert client.access_token == test_token
        assert client.session.headers["Authorization"] == f"Bearer {test_token}"
        
        # Test clearing token
        client.clear_access_token()
        assert client.access_token is None
        assert "Authorization" not in client.session.headers
    
    def test_validation_errors(self):
        """Test that validation errors are raised for invalid inputs."""
        client = OmicsAIClient("hifisolves")
        
        # Test empty collection slug
        with pytest.raises(ValidationError):
            client.list_tables("")
        
        # Test missing parameters for schema
        with pytest.raises(ValidationError):
            client.get_schema("", "table")
        
        with pytest.raises(ValidationError):
            client.get_schema("collection", "")
    
    @patch('requests.Session.request')
    def test_successful_api_call(self, mock_request):
        """Test successful API calls."""
        # Mock successful response
        mock_response = Mock()
        mock_response.json.return_value = [{"name": "test", "slugName": "test"}]
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response
        
        client = OmicsAIClient("hifisolves")
        result = client.list_collections()
        
        assert len(result) == 1
        assert result[0]["name"] == "test"
    
    @patch('requests.Session.request')
    def test_network_error_handling(self, mock_request):
        """Test network error handling."""
        import requests
        
        # Mock network error
        mock_request.side_effect = requests.exceptions.ConnectionError("Network error")
        
        client = OmicsAIClient("hifisolves")
        
        with pytest.raises(NetworkError):
            client.list_collections()
    
    @patch('requests.Session.request')
    def test_authentication_error_handling(self, mock_request):
        """Test authentication error handling."""
        import requests
        
        # Mock 401 response
        mock_response = Mock()
        mock_response.status_code = 401
        mock_error = requests.exceptions.HTTPError()
        mock_error.response = mock_response
        mock_request.side_effect = mock_error
        
        client = OmicsAIClient("hifisolves")
        
        with pytest.raises(OmicsAIError):
            client.list_collections()


class TestClientMethods:
    """Test specific client methods."""
    
    @patch('requests.Session.request')
    def test_simple_query_conversion(self, mock_request):
        """Test that simple_query properly converts parameters to filters."""
        # Mock successful response
        mock_response = Mock()
        mock_response.text = '{"data": []}'
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response
        
        client = OmicsAIClient("hifisolves")
        
        # Call simple_query with various types
        client.simple_query("collection", "table", chrom="chr1", pos=12345, af=0.01)
        
        # Verify the request was made with proper filter format
        mock_request.assert_called_once()
        call_args = mock_request.call_args
        
        # Check that JSON payload was sent
        assert call_args[1]["json"] is not None
        payload = call_args[1]["json"]
        
        # Verify filters were properly converted
        assert "filters" in payload
        filters = payload["filters"]
        
        # Check string field
        assert "chrom" in filters
        assert filters["chrom"][0]["operation"] == "EQ"
        assert filters["chrom"][0]["value"] == "chr1"
        assert filters["chrom"][0]["type"] == "STRING"
        
        # Check integer field
        assert "pos" in filters
        assert filters["pos"][0]["operation"] == "EQ"
        assert filters["pos"][0]["value"] == 12345
        assert filters["pos"][0]["type"] == "INTEGER"
        
        # Check float field
        assert "af" in filters
        assert filters["af"][0]["operation"] == "EQ"
        assert filters["af"][0]["value"] == 0.01
        assert filters["af"][0]["type"] == "FLOAT"


if __name__ == "__main__":
    pytest.main([__file__])