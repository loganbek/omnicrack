import pytest
from unittest.mock import patch, MagicMock
from omnicrack.pcap import PcapAnalyzer

@pytest.fixture
def analyzer():
    return PcapAnalyzer()

@patch("scapy.all.rdpcap")
def test_analyze_success(mock_rdpcap, analyzer):
    # Mock packets
    # Packet 1: Beacon (contains SSID)
    beacon = MagicMock()
    beacon.haslayer.return_value = True
    beacon.info = b"TestWiFi"
    beacon.addr2 = "00:11:22:33:44:55" # BSSID
    
    # Packet 2: EAPOL (Handshake)
    eapol = MagicMock()
    eapol.haslayer.side_effect = lambda layer: layer.__name__ == "EAPOL"
    eapol.addr1 = "AA:BB:CC:DD:EE:FF" # Station
    eapol.addr2 = "00:11:22:33:44:55" # BSSID
    
    mock_rdpcap.return_value = [beacon, eapol]
    
    result = analyzer.analyze("dummy.pcap")
    
    assert result["ssid"] == "TestWiFi"
    assert result["bssid"] == "00:11:22:33:44:55"
    assert result["handshake_found"] is True
    assert result["station"] == "AA:BB:CC:DD:EE:FF"

@patch("scapy.all.rdpcap")
def test_analyze_no_handshake(mock_rdpcap, analyzer):
    # Only beacon
    beacon = MagicMock()
    beacon.haslayer.return_value = True
    beacon.info = b"TestWiFi"
    beacon.addr2 = "00:11:22:33:44:55"
    
    mock_rdpcap.return_value = [beacon]
    
    result = analyzer.analyze("dummy.pcap")
    
    assert result["ssid"] == "TestWiFi"
    assert result["handshake_found"] is False
