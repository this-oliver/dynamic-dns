from unittest.mock import patch, MagicMock
from ip import is_ip_address, get_ip_address

def test_is_ip_address_valid():
    assert is_ip_address("192.168.1.1") == True
    assert is_ip_address("0.0.0.0") == True
    assert is_ip_address("255.255.255.255") == True

def test_is_ip_address_invalid():
    assert is_ip_address("192.168.1") == False
    assert is_ip_address("192.168.1.1.1") == False
    assert is_ip_address("abc.def.ghi.jkl") == False

@patch('ip.requests.get')
def test_get_ip_address_success(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.text = "192.168.1.1\n"
    mock_get.return_value = mock_response
    assert get_ip_address() == "192.168.1.1"

@patch('ip.requests.get')
def test_get_ip_address_invalid_ip(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.text = "invalid-ip\n"
    mock_get.return_value = mock_response
    assert get_ip_address() is None

@patch('ip.requests.get')
def test_get_ip_address_non_200_status(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 404
    mock_get.return_value = mock_response
    assert get_ip_address() is None
