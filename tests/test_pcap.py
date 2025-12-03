import pytest
from unittest.mock import patch, MagicMock
from omnicrack.pcap import PcapAnalyzer

@pytest.fixture
def analyzer():
    return PcapAnalyzer()

@patch("omnicrack.pcap.rdpcap")
def test_analyze_success(mock_rdpcap, analyzer):
    # Mock packets
    # Packet 1: Beacon (contains SSID)
    beacon = MagicMock()
    beacon.haslayer.return_value = True
    beacon.info = b"TestWiFi"
    beacon.addr2 = "00:11:22:33:44:55" # BSSID
    
    # Packet 2: EAPOL (Handshake)
    eapol = MagicMock()
    def side_effect(layer):
        if isinstance(layer, str):
            return layer == "EAPOL"
        return layer.__name__ == "EAPOL"
    eapol.haslayer.side_effect = side_effect
    eapol.addr1 = "AA:BB:CC:DD:EE:FF" # Station
    eapol.addr2 = "00:11:22:33:44:55" # BSSID
    
    mock_rdpcap.return_value = [beacon, eapol]
    
    result = analyzer.analyze("dummy.pcap")
    
    assert result["ssid"] == "TestWiFi"
    assert result["bssid"] == "00:11:22:33:44:55"
    assert result["handshake_found"] is True
    assert result["station"] == "AA:BB:CC:DD:EE:FF"

@patch("omnicrack.pcap.rdpcap")
def test_analyze_no_handshake(mock_rdpcap, analyzer):
    # Only beacon
    beacon = MagicMock()
    def side_effect(layer):
        if isinstance(layer, str):
            return layer in ["Dot11Beacon", "Dot11"]
        return layer.__name__ in ["Dot11Beacon", "Dot11"]
    beacon.haslayer.side_effect = side_effect
    beacon.info = b"TestWiFi"
    beacon.addr2 = "00:11:22:33:44:55"
    
    mock_rdpcap.return_value = [beacon]
    
    result = analyzer.analyze("dummy.pcap")
    
    assert result["ssid"] == "TestWiFi"
    assert result["handshake_found"] is False
