from typing import Dict, Any
from scapy.all import rdpcap

class PcapAnalyzer:
    def analyze(self, file_path: str) -> Dict[str, Any]:
        """
        Analyze a .pcap file for EAPOL handshakes.
        Returns a dictionary with details.
        """
        packets = rdpcap(file_path)
        
        result = {
            "ssid": None,
            "bssid": None,
            "station": None,
            "handshake_found": False
        }
        
        for pkt in packets:
            # Check for Beacon frames to get SSID/BSSID
            if pkt.haslayer("Dot11Beacon") or (pkt.haslayer("Dot11") and pkt.type == 0 and pkt.subtype == 8):
                try:
                    # SSID is usually in the info field of the beacon layer
                    if hasattr(pkt, "info"):
                        result["ssid"] = pkt.info.decode("utf-8", errors="ignore")
                    if hasattr(pkt, "addr2"):
                        result["bssid"] = pkt.addr2
                except Exception:
                    pass

            # Check for EAPOL frames
            if pkt.haslayer("EAPOL"):
                result["handshake_found"] = True
                if hasattr(pkt, "addr1"):
                    result["station"] = pkt.addr1
                if hasattr(pkt, "addr2") and not result["bssid"]:
                     result["bssid"] = pkt.addr2

        return result
