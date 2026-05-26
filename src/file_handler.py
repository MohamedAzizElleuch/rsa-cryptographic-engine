import os
import json


def text_to_int_blocks(text: str, block_size: int) -> list[int]:
    """Splits text into integer blocks small enough for RSA to encrypt."""
    encoded = text.encode("utf-8")
    blocks = []
    for i in range(0, len(encoded), block_size):
        chunk = encoded[i : i + block_size]
        block_int = int.from_bytes(chunk, byteorder="big")
        blocks.append(block_int)
    return blocks


def int_blocks_to_text(blocks: list[int], block_size: int) -> str:
    """Converts integer blocks back into readable text."""
    result = bytearray()
    for block in blocks:
        byte_length = (block.bit_length() + 7) // 8
        chunk = block.to_bytes(max(byte_length, 1), byteorder="big")
        result.extend(chunk)
    return result.decode("utf-8")


def encrypt_file(input_path: str, output_path: str, public_key) -> None:
    """
    Encrypts a text file using the RSA public key.
    For each integer block M: C = M^e mod n
    """
    with open(input_path, "r", encoding="utf-8") as f:
        plaintext = f.read()

    if not plaintext:
        raise ValueError("Input file is empty.")

    # Block size must be smaller than n (in bytes) to avoid overflow
    # We use (bit_length of n // 8) - 1 to stay safely below n
    block_size = (public_key.n.bit_length() // 8) - 1

    blocks = text_to_int_blocks(plaintext, block_size)

    # Encrypt each block: C = M^e mod n
    encrypted_blocks = [pow(block, public_key.e, public_key.n) for block in blocks]

    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)

    payload = {
        "block_size": block_size,
        "cipher_blocks": encrypted_blocks,
    }

    with open(output_path, "w") as f:
        json.dump(payload, f)

    print(f"  Encrypted {len(blocks)} block(s).")


def decrypt_file(input_path: str, output_path: str, private_key) -> None:
    """
    Decrypts an encrypted file using the RSA private key.
    For each ciphertext block C: M = C^d mod n
    """
    with open(input_path, "r") as f:
        payload = json.load(f)

    block_size = payload["block_size"]
    encrypted_blocks = payload["cipher_blocks"]

    # Decrypt each block: M = C^d mod n
    decrypted_blocks = [pow(block, private_key.d, private_key.n) for block in encrypted_blocks]

    plaintext = int_blocks_to_text(decrypted_blocks, block_size)

    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(plaintext)

    print(f"  Decrypted {len(decrypted_blocks)} block(s).")