import pytest
from omnicrack.logic import map_hash_type_to_mode

def test_map_md5():
    assert map_hash_type_to_mode(["MD5", "MD4"]) == ("MD5", "0")

def test_map_sha1():
    assert map_hash_type_to_mode(["SHA-1"]) == ("SHA-1", "100")

def test_map_bcrypt():
    assert map_hash_type_to_mode(["Bcrypt", "MD5"]) == ("Bcrypt", "3200")

def test_map_priority():
    # If both SHA1 and MD5 are present (unlikely for same string but possible in loose identification),
    # we need to define which one wins. Our logic says SHA1 > MD5.
    assert map_hash_type_to_mode(["SHA-1", "MD5"]) == ("SHA-1", "100")

def test_map_unknown():
    assert map_hash_type_to_mode(["WeirdHash"]) == ("Unknown (Defaulting to MD5)", "0")
