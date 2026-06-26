import socket

s = socket.socket()
s.settimeout(5)
try:
    s.connect(('127.0.0.1', 8889))
    req = b"GET /search?q=test&format=json HTTP/1.1\r\nHost: localhost:8889\r\nConnection: close\r\n\r\n"
    s.sendall(req)
    data = b""
    while True:
        chunk = s.recv(4096)
        if not chunk:
            break
        data += chunk
    print(data.decode('utf-8', errors='replace'))
except Exception as e:
    print(f"ERROR: {e}")
finally:
    s.close()
