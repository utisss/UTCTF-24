# Numbers Go Brrr

* **Event:** UTCTF 2024
* **Problem Type:** Crypto

## Solution

In looking at the code, there are two main flaws with how the random number is generated. The first is that it is seeded with an integer in the range of 10^6, which is way to small. The second is that is uses the middle square random number generator, which has know problems where it starts repeating.

The first option to solve this is to ask for the encrypted key, and then brute force all possible seeds until you get something that looks like a flag. 

The second option is to try to exploit the cyclic property of the prng. In particular, if you try encrypting enough things (around 200), you would only have to try 500 values for the key. If you encrypted the same thing repeatedly, you could narrow this down even more by using the cycle size. 