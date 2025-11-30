from typing import List
from hashid import HashID

class HashIdentifier:
    def __init__(self):
        self.hid = HashID()

    def identify(self, hash_string: str) -> List[str]:
        """
        Identify potential hash types for a given string.
        Returns a list of hash names.
        """
        # identifyHash returns a generator of HashInfo objects
        # We need to extract the name from them
        modes = self.hid.identifyHash(hash_string)
        
        results = []
        for mode in modes:
            results.append(mode.name)
            
        return results
