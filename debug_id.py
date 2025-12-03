import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "src")))
from omnicrack.identifier import HashIdentifier

def debug_identifier():
    identifier = HashIdentifier()
    
    print("--- MD5 ---")
    res = identifier.identify("5d41402abc4b2a76b9719d911017c592")
    print(res)

    print("--- SHA1 ---")
    res = identifier.identify("a9993e364706816aba3e25717850c26c9cd0d89d")
    print(res)

    print("--- Bcrypt ---")
    res = identifier.identify("$2y$12$QjSH496pcT5CEbzjD/vtVeH03tfHKFy36d4J0Ltp3lRtee9NIeslG")
    print(res)

if __name__ == "__main__":
    debug_identifier()
