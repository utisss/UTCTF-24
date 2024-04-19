from Crypto.Cipher import DES
from pwn import remote
import re


CK_A = bytes.fromhex('dae55498c4325458')
CK_B = bytes.fromhex('26fb153885bcb06b')
cipher_A = DES.new(CK_A, DES.MODE_ECB)
cipher_B = DES.new(CK_B, DES.MODE_ECB)

# from chatgpt
def binary_to_ascii(binary_string):
    # Split the binary string into 8-bit chunks
    chunks = [binary_string[i:i+8] for i in range(0, len(binary_string), 8)]

    # Convert each 8-bit chunk to its decimal equivalent and then to ASCII
    ascii_string = ''.join(chr(int(chunk, 2)) for chunk in chunks)

    return ascii_string

def check_cvv(PAN, date, code):
    key = (PAN + date + code)
    key += '0' * (32 - len(key))
    f_half = key[:16]
    s_half = key[16:]
    step1 = cipher_A.encrypt(bytes.fromhex(f_half))
    step2 = bytes(a ^ b for a,b in zip(step1, bytes.fromhex(s_half)))
    step3 = cipher_A.encrypt(step2)
    step4 = cipher_B.decrypt(step3)
    step5 = cipher_A.encrypt(step4)
    result = "".join(i for i in step5.hex() if i.isdigit())[:3]
    return result

flag = ''
con = remote('puffer.utctf.live', 8625)
con.recvuntil(b'          \n')
try:
    while True:
        card = con.recvuntil(b'\n').strip()
        nums = re.findall(r'\d+', card.decode())
        print(nums)
        check = check_cvv(nums[0], nums[1], nums[2])
        con.recvuntil(b'Valid? \n')
        if int(check) == int(nums[3]):
            con.sendline(b'1')
            flag += '1'
        else:
            con.sendline(b'0')
            flag += '0'
        con.recvuntil(b'\n').strip().decode()
except EOFError:
    con.close()
except IndexError:
    con.close()

print(binary_to_ascii(flag)[1:])
