import random


def is_miller_rabin_prime(n: int, k: int = 128) -> bool:
    """
    Miller-Rabin probabilistic primality test.
    k = number of rounds. Higher k = more accuracy.
    Returns True if n is PROBABLY prime, False if definitely composite.
    """
    # Handle base cases
    if n < 2:
        return False
    if n == 2 or n == 3:
        return True
    if n % 2 == 0:
        return False

    # Write (n - 1) as 2^r * d where d is odd
    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1
        d //= 2

    # Witness loop — run k times
    for _ in range(k):
        a = random.randrange(2, n - 1)
        x = pow(a, d, n)  # Python's built-in modular exponentiation (fast)

        if x == 1 or x == n - 1:
            continue

        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False  # Composite

    return True  # Probably prime


def generate_prime(bit_length: int) -> int:
    """
    Generates a random prime number of the specified bit length.
    Keeps generating random odd numbers until one passes the primality test.
    """
    while True:
        # Generate a random odd number of the correct bit length
        candidate = random.getrandbits(bit_length)
        # Ensure it's the right bit length (set MSB and LSB)
        candidate |= (1 << (bit_length - 1))  # Set most significant bit
        candidate |= 1                          # Ensure it's odd

        if is_miller_rabin_prime(candidate):
            return candidate