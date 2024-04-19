# Bits and Pieces

* **Event:** UTCTF 2024
* **Problem Type:** Crypto

## Solution

The problem consisted of 3 encrypted messages that made up the flag. Even though the lengths of the keys were sufficient, the key generation itself was bad. For the first message, p and q were too close together, so it's easily factorable. Both Fermat's factorization method and the elliptic curve factorization method work (you could implement this yourself or use something like https://www.alpertron.com.ar/ECM.HTM). Once you have factored n to get p and q, the rest is just straigtforward RSA decryption.

The last 2 parts of the flag is actually one part of the question (thus the comment about it being the challenge being a two-parter in the challenge description). In particular, they share a prime. Becuase of this, we can use the Euclidean algorithm to find the shared prime. From there we can divide to get the other prime number (for both messages) and then decrypt the messages. 