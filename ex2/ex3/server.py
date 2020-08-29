import argparse
import socket
import select
import os

parser = argparse.ArgumentParser(description='echo server')
parser.add_argument('--address', default='127.0.0.1', help='Listen IP address')
parser.add_argument('-p', '--port', default=8888, type=int, help='Port address')
parser.add_argument('-s', '--source', default='html', help='Source file directory path')

def load_not_found_page(path):
    if os.path.exists(path):
        with open(path) as f:
            return f.read()
    return "404 not found."

def main():
    args = parser.parse_args()
    host = args.address
    port = args.port
    source = args.source
    backlog = 10
    bufsize = 4096
    not_found = load_not_found_page(os.path.join(source, "404.html"))

    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    readfds = [server_sock]
    try:
        server_sock.bind((host, port))
        server_sock.listen(backlog)
        print("Listen {}:{}".format(host, port))

        while True:
            rready, wready, xready = select.select(readfds, [], [])
            for sock in rready:
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
                        request_type, file_uri = msg.split(' ')
                        if request_type == 'GET':
                            file_path = os.path.join(source, file_uri)
                            response_data = not_found
                            if os.path.isfile(file_path):
                                with open(file_path) as f:
                                    response_data = f.read()
                            sock.send(response_data)
    finally:
        for sock in readfds:
            sock.close()

if __name__ == "__main__":
    main()