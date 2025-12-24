import socket
import os

HOST = '127.0.0.1'
PORT = 65433
FILENAME = 'my_text.txt'

if not os.path.exists(FILENAME):
    with open(FILENAME, 'w') as f:
        f.write("This is a test file for socket transfer.")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    with open(FILENAME, 'rb') as f:
        data = f.read()
        s.sendall(data)