# Home on the Range

This is a web server that deals with "obscure HTTP headers". Observing the response indicates that
there's an `Accept-Ranges` header, which lets you read portions of files. This seems redundant but will
come into play later.

By playing around with the web server, you can discover that there's a path traversal vulnerability
that you can use to read all files on the server (send a request to `/../../`). It includes the
source code for the web server (at `/../../server.py`), which shows that there used to be a flag
file at `/setup/flag.txt` but that it was deleted.

As it happens, that flag is still in the server's memory. On Linux, you can read from a process's memory
using various files in the `/proc` directory; the current process (i.e. the web server) is always under
`/proc/self/`. The `maps` file gives an index of all used portions of memory in the process, and the `mem` file
gives all of the memory. The problem is that the `mem` file is as large as all of memory, so you can't read
it directly. But we can use the HTTP range-related headers to read just the relevant portions of the `mem` file.

Dumping all the readable portions of memory will eventually show the flag in one of those portions. Search for
the string "utflag".

## FAQ

**The flag file is missing**: That's expected behavior.

**You're not spec-compliant in X way:** Just deal with it. Figure out how my implementation works yourself.
(Officer note: it's possible to dump the server source as seen above, and my solve script in dump.py works for this server.
The HTTP range stuff is really just an excuse.)

**I've read all of the memory regions from /../../proc/self/maps and there isn't a flag there:** Several possible issues.

* Make sure the you're not using an old version of the file. ASLR means that the memory locations can change if the program gets restarted.
* If you're looking at the section of memory labeled "stack" or "heap": Python doesn't store all its stack/heap data in those sections. In this case, the flag generally ends up in an unlabeled section of memory.
* You may have an off-by-one error in the range header. The bounds are inclusive, not exclusive (so 0-99 gives the first 100 bytes). If that extra byte happens to be in an unmapped page, then the whole request may return an error.

**I'm trying to dump /proc/self/mem but getting an I/O error:** The offset you read into /proc/self/mem corresponds to the memory address. If you read the file normally, then the first byte you read from is memory address 0, which is the definition of dereferencing a null pointer. The point of the Range headers is so that you can pick what offsets to read from.

**What approaches are invalid?**

* Trying to crash/shutdown/SIGTERM the server
* Performance or race conditions
* Brute force / dirbuster
* Exploits of the Python interpreter
(I don't consider dumping all the mapped memory regions to be brute force or a Python exploit.)

**Why did you include code to write the flag file back if you don't need to crash the server?** Both as a "just in case" thing and so that we as admins could stop and restart the container manually if need be. Restarting the container wouldn't automatically put the flag file back, so that would prevent the server from starting back up if it crashed.