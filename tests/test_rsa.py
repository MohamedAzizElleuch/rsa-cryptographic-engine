import sys
import os
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.primes import is_miller_rabin_prime, generate_prime
from src.euclidean import gcd, extended_gcd, modular_inverse
from src.rsa_core import generate_rsa_keypair


class TestPrimes(unittest.TestCase):

    def test_known_primes(self):
        for p in [2, 3, 5, 7, 11, 13, 97, 7919]:
            self.assertTrue(is_miller_rabin_prime(p), f"{p} should be prime")

    def test_known_composites(self):
        for n in [1, 4, 9, 15, 100, 561]:
            self.assertFalse(is_miller_rabin_prime(n), f"{n} should NOT be prime")

    def test_generated_prime_is_prime(self):
        p = generate_prime(512)
        self.assertTrue(is_miller_rabin_prime(p))


class TestEuclidean(unittest.TestCase):

    def test_gcd(self):
        self.assertEqual(gcd(48, 18), 6)
        self.assertEqual(gcd(100, 75), 25)
        self.assertEqual(gcd(7, 5), 1)

    def test_extended_gcd(self):
        g, x, y = extended_gcd(30, 20)
        self.assertEqual(g, 10)
        self.assertEqual(30 * x + 20 * y, g)

    def test_modular_inverse(self):
        d = modular_inverse(65537, 3120)
        self.assertEqual((65537 * d) % 3120, 1)


class TestRSA(unittest.TestCase):

    def test_encrypt_decrypt_roundtrip(self):
        """Core test: encrypting then decrypting must return the original number."""
        pub, priv = generate_rsa_keypair(1024)  # Use 1024 for test speed
        message = 42
        ciphertext = pow(message, pub.e, pub.n)
        plaintext = pow(ciphertext, priv.d, priv.n)
        self.assertEqual(message, plaintext)


if __name__ == "__main__":
    unittest.main(verbosity=2)