# Simple Signature

* **Event:** UTCTF 2024
* **Problem Type:** Crypto

## Solution

When getting the signature for the same message twice, it becomes clear that something strange is going on since the signature is not the same. We can take the given signature, compute the message, and see that the message it computes is not the same as the one we put in. This is true normally, as messages are usually hashed before they are signed, but the manner in which the message has been modified is abnormal. After testing a few values, we can see that the message is incremented by the number of prior signatures, and we can use this information to create a valid signature. We can for example, request it to sign 4, and then provide a message of 3 and the signature it gave us earlier as our signature message pair. 