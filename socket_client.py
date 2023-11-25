from socket import *


def ascii_game_client_program():

    client_host = '127.0.0.1'  # local host
    client_port = 65535  # limit as 2^16 port numbers
    print(f"Host: {client_host}")
    print(f"Port: {client_port}")

    hello_string = "hello"
    encoded_string = encode_string(hello_string)
    print(encoded_string)
    decoded_string = decode_string(encoded_string)
    print(decoded_string)

    # connect to socket set up by server
    client_socket = socket(AF_INET, SOCK_STREAM)
    client_socket.connect((client_host, client_port))

   # send data
    client_socket.send(encoded_string)

   # print data received from server
    data = client_socket.recv(125)  # can hang here
    print('Received: ',data.decode())
    client_socket.close()


def decode_string(str):
    return str.decode('utf-8')

def encode_string(str):
    return str.encode('utf-8')


ascii_game_client_program()
