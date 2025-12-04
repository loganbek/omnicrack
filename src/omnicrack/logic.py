from typing import List, Optional, Tuple

def map_hash_type_to_mode(possible_types: List[str]) -> Tuple[str, str]:
    """
    Maps a list of possible hash types (from HashIdentifier) to a Hashcat mode.
    Returns a tuple (hash_type_name, hash_mode_id).
    Defaults to ("MD5", "0") if uncertain but MD5 is present, or if mapping fails.
    """
    # Priority based mapping
    # This is a simplified logic. In a real scenario, we might want user input or smarter heuristics.
    
    if "Bcrypt" in possible_types or "Blowfish(OpenBSD)" in possible_types:
        return "Bcrypt", "3200"
        
    if "SHA-1" in possible_types:
        return "SHA-1", "100"
        
    if "MD5" in possible_types:
        return "MD5", "0"
        
    # Default fallback
    return "Unknown (Defaulting to MD5)", "0"
