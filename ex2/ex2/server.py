import argparse
import socket
import select

parser = argparse.ArgumentParser(description='echo server')
parser.add_argument('--address', default='127.0.0.1', help='Listen IP address')
parser.add_argument('-p', '--port', default=8888, type=int, help='Port address')

def main():
    args = parser.parse_args()
    host = args.address
    port = args.port
    backlog = 10
    bufsize = 4096

    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    readfds = [server_sock]
    try:
        server_sock.bind((host, port))
        server_sock.listen(backlog)
        print("Listen {}:{}".format(host, port))

        while True:
            rready, wready, xready = select.select(readfds, [], [])
            for sock in rready:
                print("Someone requesting")
                if sock is server_sock:
                    conn, (remote_addr, remote_port) = server_sock.accept()
                    print("Accept connection {}:{}".format(remote_addr, remote_port))
                    readfds.append(conn)
                else:
                    msg = sock.recv(bufsize)
                    if len(msg) == 0:
                        sock.close()
                        readfds.remove(sock)
                    else:
                        print(msg)
                        sock.send(msg)
    finally:
        for sock in readfds:
            sock.close()

if __name__ == "__main__":
    main()