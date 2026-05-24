# 🔐 RSA Cryptographic Engine

A command-line tool that implements RSA encryption **from mathematical primitives** — 
no cryptography libraries. Built to demonstrate Discrete Math and algorithms in action.

## The Math Behind It
| Algorithm | Purpose |
|---|---|
| Miller-Rabin Primality Test | Generate large prime numbers p and q |
| Euler's Totient φ(n) = (p-1)(q-1) | Compute the key space |
| Extended Euclidean Algorithm | Find the modular inverse for the private key |
| Modular Exponentiation M^e mod n | Encrypt and decrypt blocks |

## Features
- Generate 1024 / 2048 / 4096-bit RSA key pairs
- Encrypt any `.txt` file with a public key
- Decrypt `.enc.json` files with the matching private key
- Beautiful terminal UI via `rich`

## Setup
\`\`\`bash
git clone https://github.com/YOUR_USERNAME/rsa-cryptographic-engine.git
cd rsa-cryptographic-engine
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python src/cli.py
\`\`\`

## Tests
\`\`\`bash
python -m pytest tests/ -v
\`\`\`