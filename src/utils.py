import hashlib
import base58
import ecdsa
from src.config import SECP256k1_CURVE

def validate_key(key, target_address):
    """
    Validate a private key by generating its Bitcoin address and comparing to the target.

    Args:
        key (int): Private key integer
        target_address (str): Target Bitcoin address

    Returns:
        tuple: (bool, str) - (success flag, WIF private key if successful)
    """
    try:
        private_key = ecdsa.SigningKey.from_secret_exponent(key, curve=SECP256k1_CURVE)
        public_key = private_key.get_verifying_key().to_string("compressed")
        sha256_hash = hashlib.sha256(public_key).digest()
        ripemd160_hash = hashlib.new('ripemd160', sha256_hash).digest()
        extended_hash = b'\x00' + ripemd160_hash
        checksum = hashlib.sha256(hashlib.sha256(extended_hash).digest()).digest()[:4]
        btc_address = base58.b58encode(extended_hash + checksum).decode()
        if btc_address == target_address:
            wif = base58.b58encode_check(b'\x80' + key.to_bytes(32, 'big')).decode()
            return True, wif
        return False, ""
    except Exception as e:
        return False, ""
