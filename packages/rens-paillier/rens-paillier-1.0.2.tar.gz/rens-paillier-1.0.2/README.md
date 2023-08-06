# Paillier encryption

`python3.8` package for [Paillier encryption](https://en.wikipedia.org/wiki/Paillier_cryptosystem).

### Example usage

#### Setup
    from paillier.keygen import generate_keys
    from paillier.crypto import encrypt, decrypt

    pk, sk = generate_keys()

#### Basic encryption and decryption
    m1 = 45336
    ciphertext = encrypt(pk, m1)
    assert m1 == decrypt(pk, sk, ciphertext)

#### Homomorphic things
    from paillier.crypto import secure_addition, scalar_multiplication, secure_subtraction

    n, _ = pk
    m2 = 30381

    # Secure addition
    e1 = encrypt(pk, m1)
    e2 = encrypt(pk, m2)
    addition = secure_addition(e1, e2, n)
    assert m1 + m2 == decrypt(pk, sk, addition)

    # Scalar multiplication
    k = 23  # some scalar
    e1 = encrypt(pk, m1)
    multiplied = scalar_multiplication(e1, k, n)
    assert (m1 * k) % n == decrypt(pk, sk, multiplied)

    # Secure subtraction
    assert m1 > m2, "m2 should be bigger than m1 in order to subtract m2 from m1"
    e1 = encrypt(pk, m1)
    e2 = encrypt(pk, m2)
    subtracted = secure_subtraction(e1, e2, n)
    assert m1 - m2 == decrypt(pk, sk, subtracted)