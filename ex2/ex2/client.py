import argparse
import sys
import socket
from contextlib import closing

parser = argparse.ArgumentParser(description='echo client')
parser.add_argument('address', help='Destination IP address')
parser.add_argument('-p', '--port', default=8888, type=int, help='Port address')

def main():
    args = parser.parse_args()
    host = args.address
    port = args.port
    bufsize = 4096

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    with closing(sock):
        sock.connect((host, port))
        print("Connected {0}:{1}".format(host, port))
        while True:
            line = sys.stdin.readline().rstrip()
            if len(line) == 0:
                break
            sock.send(line.encode('utf-8'))
            print(sock.recv(bufsize))

if __name__ == "__main__":
    main()