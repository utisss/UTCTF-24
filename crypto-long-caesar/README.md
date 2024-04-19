# How the txt file was created:
I took the flag, and surrounded it with a random assortment of a-z, {, }, and _. I then ran the entire thing through a caesar cipher for the letters only, resulting in the flag (and the random letters) being scrambled. The ciphered flag is somewhere in the txt file.

# How to solve:
The participant must run all a-z letters in the file through a caesar cipher 25 times (for all the remaining letters), checking each time if the string "utflag{" exists in the file.

It's kinda hard to give hints for this problem, so just make sure anyone asking understand the problem, since the solution is just to brute-force the cipher until the string "utflag{" exists (using something like Python). 


