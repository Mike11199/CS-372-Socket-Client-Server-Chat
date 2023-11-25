from socket import *


def ascii_game_server_program():

    server_host = '127.0.0.1' # local host
    server_port = 65535  # limit as 2^16 port numbers
    print(f"Host: {server_host}")
    print(f"Port: {server_port}")

    # set up socket
    server_socket = socket(AF_INET, SOCK_STREAM)

    """Reference project instructions, SO_REUSEADDR prevents switching host/port
    each time we restart the server."""
    server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    server_socket.bind((server_host, server_port))

    # max num of queued connections is 1
    server_socket.listen(1)
    print("Server is now listening...")

    # reference: https://docs.python.org/3/library/socket.html
    # reference textbook pg. 164
    # accept incoming connection, send back string, then close socket
    while True:
        print("restarting loop")
        conn_client_socket, conn_client_addr = server_socket.accept() # michael - can hang here
        print(conn_client_socket)
        print(conn_client_addr)
        buffer_string = b'buffer'
        while buffer_string:
            buffer_string = conn_client_socket.recv(1024)
            print("Received: ")
            print(buffer_string)
        print("Sending Response: ")
        print(buffer_string)
        conn_client_socket.send(buffer_string)


def decode_string(str):
    return str.decode('utf-8')

def encode_string(str):
    return str.encode('utf-8')


ascii_game_server_program()


