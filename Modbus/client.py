import socket
import sys

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 5005         # The port used by the server

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(bytes(" ".join(sys.argv[1:]),'utf-8'))
        data = s.recv(1024)

    print('Received', repr(data))

if __name__ == "__main__":

    main()