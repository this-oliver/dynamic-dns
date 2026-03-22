from pytest import raises
from unittest.mock import patch
from src.common.record import Record
from src.providers.cloudflare import CloudflareProvider, CloudflareApiRecord

@patch('src.providers.cloudflare.CloudflareProvider._get_zones')
def test_update_dns_record_with_empty_get_zones(mocker):
    mocker.return_value = []  # Mock _get_zones to return an empty list
    provider = CloudflareProvider("test_token")
    record = Record(provider="cloudflare", domain_name="example.com", token="test_token")

    with raises(Exception) as e:
        provider.update_dns_record(record, "192.168.1.1")
    
    assert str(e.value).startswith("DNS record for") and "not found" in str(e.value)


@patch('src.providers.cloudflare.CloudflareProvider._get_single_dns_record')
def test_update_dns_record_with_non_a_record(mocker):
    zone_name = "example.com"

    # Mock _get_single_dns_record to return a list with a non-A record    
    mocker.return_value = CloudflareApiRecord(id="record_id", zone="1234", type="CNAME", name=zone_name, content="cname.example.com", ttl=3600, proxied=True)
    
    record = Record(provider="cloudflare", domain_name=f"www.{zone_name}", token="test_token")
    provider = CloudflareProvider(record.token)

    with raises(Exception) as e:
        provider.update_dns_record(record, "192.168.1.1")
    
    assert "Only 'A' records can be updated with an IP address." in str(e.value)
