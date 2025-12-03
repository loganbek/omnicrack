import pytest
from omnicrack.identifier import HashIdentifier

@pytest.fixture
def identifier():
    return HashIdentifier()

def test_identify_md5(identifier):
    # Standard MD5
    hash_str = "5d41402abc4b2a76b9719d911017c592"
    results = identifier.identify(hash_str)
    assert "MD5" in results

def test_identify_sha1(identifier):
    # Standard SHA1
    hash_str = "a9993e364706816aba3e25717850c26c9cd0d89d"
    results = identifier.identify(hash_str)
    assert "SHA-1" in results

def test_identify_bcrypt(identifier):
    # Bcrypt
    hash_str = "$2y$12$QjSH496pcT5CEbzjD/vtVeH03tfHKFy36d4J0Ltp3lRtee9NIeslG"
    results = identifier.identify(hash_str)
    assert "Blowfish(OpenBSD)" in results or "Bcrypt" in results

def test_identify_unknown(identifier):
    # Garbage string
    hash_str = "This is definitely not a hash string!"
    results = identifier.identify(hash_str)
    assert results == []
