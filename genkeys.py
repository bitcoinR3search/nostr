from pynostr.key import PrivateKey

private_key = PrivateKey()
public_key = private_key.public_key
print(f"Private key: {private_key.bech32()}")
print(f"Private key hex: {private_key.hex()}")
print(f"Public key: {public_key.bech32()}")
print(f"Public key hex: {public_key.hex()}")