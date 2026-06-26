import socket
s = socket.socket()
s.settimeout(3)
r = s.connect_ex(('127.0.0.1', 8889))
print('LISTENING' if r == 0 else 'NOT LISTENING')
s.close()
