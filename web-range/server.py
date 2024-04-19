from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import os
from html import escape
from mimetypes import guess_type
import re
from random import randbytes
import signal
import sys
import threading

with open("/setup/flag.txt") as f:
    the_flag = f.read()
os.remove("/setup/flag.txt")

def process_range_request(ranges, content_type, file_len, write_header, write_bytes, write_file_range):
    boundary = randbytes(64).hex()
    for [first, last] in (ranges if ranges != [] else [[None, None]]):
        count = None
        if first is None:
            if last is None:
                first = 0
            else:
                first = file_len - last
                count = last
        elif last is not None:
            count = last - first + 1

        if (count is not None and count < 0) or first < 0:
            return False
        
        content_range_header = "bytes " + str(first) + "-" + (str(first + count - 1 if count is not None else file_len - 1)) + "/" + str(file_len)
        if len(ranges) > 1:
            write_bytes(b"\r\n--" + boundary.encode())
            if content_type:
                write_bytes(b"\r\nContent-Type: " + content_type.encode())
            write_bytes(b"\r\nContent-Range: " + content_range_header.encode())
            write_bytes(b"\r\n\r\n")
        else:
            if content_type:
                write_header("Content-Type", content_type)
            if len(ranges) > 0:
                write_header("Content-Range", content_range_header)
        if not write_file_range(first, count):
            return False
    if len(ranges) > 1:
        write_bytes(b"\r\n--" + boundary.encode() + b"--\r\n")
        write_header("Content-Type", "multipart/byteranges; boundary=" + boundary)
    elif len(ranges) == 0:
        write_header("Accept-Ranges", "bytes")
    return True


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        return self.try_serve_file(self.path[1:])

    def try_serve_file(self, f):
        if f == "":
            f = "."
        try:
            status_code = 200
            range_match = re.match("^bytes=\\d*-\\d*(, *\\d*-\\d*)*$", self.headers.get("range", "none"))
            ranges = []
            if range_match:
                status_code = 206
                ranges = []
                for range in self.headers.get("range").split("=")[1].split(", "):
                    left, right = range.split("-")
                    new_range = [None, None]
                    if left:
                        new_range[0] = int(left)
                    if right:
                        new_range[1] = int(right)
                    if not left and not right:
                        # invalid
                        ranges = [[None, None]]
                        break
                    ranges.append(new_range)

            self.log_message("Serving %s ranges %s", f, repr(ranges))

            (content_type, _) = guess_type(f)

            with open(f, "rb") as io:
                file_length = os.stat(f).st_size

                headers = []
                chunks = []

                def check_file_chunk(first, count):
                    if count is None:
                        if first < 0:
                            return False
                        io.seek(first)
                        if io.read(1) == b"":
                            return False
                    else:
                        if count <= 0 or first < 0:
                            return False
                        io.seek(first + count - 1)
                        if io.read(1) == b"":
                            return False
                    chunks.append({"type": "file", "first": first, "count": count})
                    return True


                ok = process_range_request(ranges, content_type, file_length,
                                           lambda k, v: headers.append((k, v)),
                                           lambda b: chunks.append({"type": "bytes", "bytes": b}),
                                           check_file_chunk)
                if not ok:
                    self.send_response(416)
                    self.send_header("Content-Range", "bytes */" + str(file_length))
                    self.end_headers()
                    return
                
                content_length = 0
                for chunk in chunks:
                    if chunk["type"] == "bytes":
                        content_length += len(chunk["bytes"])
                    elif chunk["type"] == "file":
                        content_length += chunk["count"] if chunk["count"] is not None else file_length - chunk["first"]
                
                self.send_response(status_code)
                for (k, v) in headers:
                    self.send_header(k, v)
                self.send_header("Content-Length", str(content_length))
                self.end_headers()

                for chunk in chunks:
                    if chunk["type"] == "bytes":
                        self.wfile.write(chunk["bytes"])
                    elif chunk["type"] == "file":
                        io.seek(chunk["first"])
                        count = chunk["count"]
                        buf_size = 1024 * 1024
                        while count is None or count > 0:
                            chunk = io.read(min(count if count is not None else buf_size, buf_size))
                            self.wfile.write(chunk)
                            if count is not None:
                                count -= len(chunk)
                            if len(chunk) == 0:
                                break
        except FileNotFoundError:
            print(f)
            self.send_error(404)
        except IsADirectoryError:
            if not f.endswith("/") and f != ".":
                self.send_response(303)
                self.send_header("Location", "/" + f + "/")
                self.end_headers()
            elif os.path.isfile(f + "/index.html"):
                return self.try_serve_file(f + "/index.html")
            else:
                dir_name = os.path.basename(os.path.abspath(f))
                if dir_name == "":
                    dir_name = "/"
                body = (
                    "<!DOCTYPE html><html><head><title>Directory listing of "
                        + escape(dir_name)
                        + "</title><body><h1>Directory listing of " + escape(dir_name) + "</h1><ul>"
                        + "".join(["<li><a href=\"" + escape(child, quote=True) + "\">" + escape(child) + "</a></li>" for child in os.listdir(f)])
                        + "</ul></body></html>"
                    ).encode("utf-8")
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write(body)
                pass
        except OSError as e:
            self.send_error(500, None, e.strerror)

server = ThreadingHTTPServer(("0.0.0.0", 3000), Handler)

def exit_handler(signum, frame):
    sys.stderr.write("Received SIGTERM\n")

    # Needs to run in another thread to avoid blocking the main thread
    def shutdown_server():
        server.shutdown()
    shutdown_thread = threading.Thread(target=shutdown_server)
    shutdown_thread.start()
signal.signal(signal.SIGTERM, exit_handler)

sys.stderr.write("Server ready\n")
server.serve_forever()

with open("/setup/flag.txt", "w") as f:
    f.write(the_flag)
