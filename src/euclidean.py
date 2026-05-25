def gcd(a: int, b: int) -> int:
    """Standard Euclidean Algorithm — finds Greatest Common Divisor."""
    while b:
        a, b = b, a % b
    return a


def extended_gcd(a: int, b: int) -> tuple[int, int, int]:
    """
    Extended Euclidean Algorithm.
    Returns (gcd, x, y) such that: a*x + b*y = gcd(a, b)
    This is the mathematical engine for finding modular inverses.
    """
    if a == 0:
        return b, 0, 1

    gcd_val, x1, y1 = extended_gcd(b % a, a)

    x = y1 - (b // a) * x1
    y = x1

    return gcd_val, x, y


def modular_inverse(e: int, phi: int) -> int:
    """
    Finds the modular inverse of e mod phi.
    This computes d such that: (e * d) % phi == 1
    d becomes the private key exponent.
    """
    gcd_val, x, _ = extended_gcd(e, phi)

    if gcd_val != 1:
        raise ValueError(f"Modular inverse does not exist. gcd({e}, {phi}) = {gcd_val}")

    return x % phi