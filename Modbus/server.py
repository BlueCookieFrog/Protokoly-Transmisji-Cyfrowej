# Echo server program
import socket

HOST = "127.0.0.1"  # Symbolic name meaning all available interfaces
PORT = 5005         # Arbitrary non-privileged port


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen(1)
        conn, addr = s.accept()
        with conn:
            print("Connected by", addr)
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                conn.sendall(data)
                print('Received', repr(data))

if __name__ == "__main__":

    main()