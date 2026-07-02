# Pure RSA Cryptography (Python)

A console-based implementation of the RSA cryptography algorithm, built entirely from scratch in Python **without using any external cryptography libraries**. This was developed as an academic project to explore the underlying number theory and modular arithmetic of public-key cryptography.

## Features

- **RSA Key Generation**: Generates public and private key pairs automatically using randomly generated 16-bit prime numbers, or allows manual entry of custom primes $p$ and $q$.
- **Pure Math Implementations**: Features custom implementations of:
  - **Greatest Common Divisor (GCD)** using Euclidean Algorithm.
  - **Extended Euclidean Algorithm** to calculate coefficients.
  - **Modular Multiplicative Inverse** for the private exponent $d$.
  - **Trial Division Primality Test** to validate $p$ and $q$.
  - **Modular Exponentiation** (via Python's fast native `pow(base, exp, mod)`) for encryption and decryption.
- **Message Encrypter/Decrypter**: Encrypts raw text strings into space-separated ciphertext blocks and decrypts them back, deleting source files in the process to simulate secure transit.
- **Password Strength Validator**: Validates administrator passwords against standard complexity patterns (length, character variety).

## RSA Mathematical Flow

The application follows the classic RSA math sequence:

1. **Prime Selection**: Select two distinct prime numbers, $p$ and $q$.
2. **Compute Modulus**: Compute $n = p \times q$. The length of $n$ is the key size.
3. **Euler's Totient**: Compute $\phi(n) = (p - 1) \times (q - 1)$.
4. **Choose Public Exponent**: Select an integer $e$ such that $1 < e < \phi(n)$ and $\gcd(e, \phi(n)) = 1$ (the project defaults to $65537$).
5. **Compute Private Exponent**: Determine $d$ as the modular multiplicative inverse of $e \pmod{\phi(n)}$, satisfying $d \times e \equiv 1 \pmod{\phi(n)}$ (calculated via the Extended Euclidean Algorithm).
6. **Encryption**: A character message $M$ is converted to its integer ordinal value $m$ and encrypted to ciphertext $c$ using:
   $$c = m^e \pmod n$$
7. **Decryption**: Ciphertext $c$ is decrypted back to $m$ using:
   $$m = c^d \pmod n$$

## Tech Stack

- **Language**: Python 3
- **Libraries**: Only standard libraries (`os`, `re`, `random`, `math`)

## Local Setup & Run Guide

To run this application locally, you only need Python 3 installed. No external packages are required.

### 1. Run the Application

Open a terminal in the project directory and execute:

```bash
python criptografa.py
```

### 2. Basic Flow Demonstration

1. Choose option `1` (Write new message), input an ID (e.g. `test`) and a secret message (e.g. `Hello RSA!`). This saves `test.txt`.
2. Choose option `2` (Encrypt message), input the message ID `test`, verify your administrator password (default is `123`), choose key generation option `1` (Automatic). This deletes `test.txt` and creates the encrypted payload `test.enc`.
3. Choose option `3` (Decrypt message), input ID `test` and the administrator password. This decrypts the payload, deletes `test.enc` and restores the original message in `test.txt`.

---
*Created as a college project to practice pure mathematical RSA logic.*
