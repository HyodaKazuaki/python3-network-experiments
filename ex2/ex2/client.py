import sys
import socket
from contextlib import closing

def main():
    host = '127.0.0.1'
    port = 8888
    bufsize = 4096

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    with closing(sock):
        sock.connect((host, port))
        while True:
            line = sys.stdin.readline().rstrip()
            if len(line) == 0:
                break
            sock.send(line.encode('utf-8'))
            print(sock.recv(bufsize))

if __name__ == "__main__":
    main()