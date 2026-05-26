import json
import os
from dataclasses import dataclass
from .primes import generate_prime
from .euclidean import gcd, modular_inverse


# Public exponent — 65537 is the standard choice in real RSA (it's prime and efficient)
PUBLIC_EXPONENT = 65537


@dataclass
class RSAPublicKey:
    n: int  # modulus
    e: int  # public exponent

    def to_dict(self) -> dict:
        return {"n": self.n, "e": self.e, "key_type": "RSA_PUBLIC"}


@dataclass
class RSAPrivateKey:
    n: int  # modulus
    d: int  # private exponent
    p: int  # prime factor 1
    q: int  # prime factor 2

    def to_dict(self) -> dict:
        return {"n": self.n, "d": self.d, "p": self.p, "q": self.q, "key_type": "RSA_PRIVATE"}


def generate_rsa_keypair(bit_length: int = 2048) -> tuple[RSAPublicKey, RSAPrivateKey]:
    """
    Generates an RSA public/private key pair.

    The math:
    1. Pick two large primes p and q
    2. Compute n = p * q  (the modulus)
    3. Compute φ(n) = (p-1)(q-1)  (Euler's totient)
    4. Choose e = 65537  (public exponent, must be coprime to φ(n))
    5. Compute d = modular_inverse(e, φ(n))  (private exponent)
    """
    half_bits = bit_length // 2

    # Step 1: Generate two distinct large primes
    print(f"  Generating prime p ({half_bits} bits)...")
    p = generate_prime(half_bits)

    print(f"  Generating prime q ({half_bits} bits)...")
    q = generate_prime(half_bits)

    # Ensure p and q are distinct
    while p == q:
        q = generate_prime(half_bits)

    # Step 2: Compute the modulus
    n = p * q

    # Step 3: Compute Euler's totient function
    phi_n = (p - 1) * (q - 1)

    # Step 4: Verify e and phi(n) are coprime (they almost always are with e=65537)
    e = PUBLIC_EXPONENT
    if gcd(e, phi_n) != 1:
        raise ValueError("e and phi(n) are not coprime. Regenerate keys.")

    # Step 5: Compute the private exponent using Extended Euclidean Algorithm
    d = modular_inverse(e, phi_n)

    public_key = RSAPublicKey(n=n, e=e)
    private_key = RSAPrivateKey(n=n, d=d, p=p, q=q)

    return public_key, private_key


def save_keys(public_key: RSAPublicKey, private_key: RSAPrivateKey, keys_dir: str = "keys"):
    """Saves keys as JSON files."""
    os.makedirs(keys_dir, exist_ok=True)

    pub_path = os.path.join(keys_dir, "public_key.json")
    priv_path = os.path.join(keys_dir, "private_key.json")

    with open(pub_path, "w") as f:
        json.dump(public_key.to_dict(), f, indent=2)

    with open(priv_path, "w") as f:
        json.dump(private_key.to_dict(), f, indent=2)

    return pub_path, priv_path


def load_public_key(path: str) -> RSAPublicKey:
    with open(path, "r") as f:
        data = json.load(f)
    return RSAPublicKey(n=data["n"], e=data["e"])


def load_private_key(path: str) -> RSAPrivateKey:
    with open(path, "r") as f:
        data = json.load(f)
    return RSAPrivateKey(n=data["n"], d=data["d"], p=data["p"], q=data["q"])