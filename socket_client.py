import socket
from socket import AF_INET, SOCK_STREAM
import sys

# Reference:  https://enzircle.hashnode.dev/handling-message-boundaries-in-socket-programming#heading-method-3-message-length-header

client_socket = None # global so I can keyboard interrupt close the connection

def ascii_game_client_program() -> None:
    """
    This function acts as a client program.

    It attempts to connect via a socket to an existing server running on that socket's host/port combination.

    Messages can then be sent and received from the server via this socket.
    """

    client_host = '127.0.0.1'  # local host
    client_port = 65535  # limit as (2^16 - 1) port numbers
    print(f"Host: {client_host}")
    print(f"Port: {client_port}")

    # connect to socket set up by server
    global client_socket

    try:
        client_socket = socket.socket(AF_INET, SOCK_STREAM)
        client_socket.connect((client_host, client_port))
        print("Connected to the server!  Please type /q to close the connection.")
    except ConnectionRefusedError:
        print("Error, server is not running.")
        sys.exit(0)

    while True:

        # send message to server
        message = input("\nEnter Input > ")
        if message == '/q':
            print("Sending /q to end connection with server!")
            send_message_to_server(message, client_socket)
            sys.exit(0)
        send_message_to_server(message, client_socket)

        # get response from server
        print("Awaiting response from server...")
        server_response_len = get_message_len(client_socket)
        msg_from_server = get_message_str_from_server(client_socket, server_response_len)
        print(f"Message from server: {msg_from_server}")
        if msg_from_server == '/q':
            print("Server closed connection!")
            sys.exit(0)
        if msg_from_server == 'play blackjack':
            print("Entering multiplayer")
            sys.exit(0)


def send_message_to_server(message: str, socket_conn: socket.socket) -> None:
    """
    This function sends a message to the server.  It first takes the message to be sent and calculates its size as a 32 bit integer.
    The integer is then sent to the server so that it knows how much data to expect from the incoming message.

    Then, the actual message is sent as a stream of bytes to the server.

    If there is some type of exception, the client exits.
    """
    # https://realpython.com/python-sockets/
    message_to_bytes = encode_string(message)
    message_len = len(message_to_bytes)
    message_len_to_fixed_byte_size = message_len.to_bytes(4, byteorder='big')
    # print(f"Sending Bytes to Server (Hex 0x): {hex(int.from_bytes(message_len_to_fixed_byte_size, byteorder='big'))}")
    try:
        socket_conn.send(message_len_to_fixed_byte_size)
        socket_conn.send(message_to_bytes)
    except ConnectionResetError:
        print("Server closed connection!")
        sys.exit(0)


# Reference:
# https://enzircle.hashnode.dev/handling-message-boundaries-in-socket-programming#heading-method-3-message-length-header
def get_message_len(socket_conn: socket.socket) -> int:
    """
    This function should get the message length expected from the server.  The below recv() will hang until we receive data.

    We loop while we haven't received the expected number of bytes as we might not receive everything at once.  This function should always receive 4 bytes,
    for a 32 bit integer, telling us the length of the expected message to be received.

    If the server unexpectedly closes recv() will return an empty bytes object b''.  This is handled by the client simply exiting and printing the reason
    to the terminal.
    """
    expected_num_bytes = 4
    data_buffer = b""
    while len(data_buffer) < expected_num_bytes:
        remaining_bytes = expected_num_bytes - len(data_buffer)
        message_from_server = socket_conn.recv(remaining_bytes)
        if message_from_server == b'':
            print("Server closed connection unexpectedly!")
            sys.exit(0)
        data_buffer += message_from_server
    msg_len = int.from_bytes(data_buffer, byteorder="big")
    # print(f"Message length is : {msg_len}")
    return msg_len

# Reference:
# https://enzircle.hashnode.dev/handling-message-boundaries-in-socket-programming#heading-method-3-message-length-header
def get_message_str_from_server(socket_conn: socket.socket, message_len_byte_expected: int) -> int:
    """
    This function should get a full message from the server.  The below recv() will hang until we receive data.

    We loop while we haven't received the expected number of bytes as we might not receive everything at once.  The length of the expected message is
    received earlier and passed into this function.

    If the server unexpectedly closes recv() will return an empty bytes object b''.  This is handled by the client simply exiting and printing the reason
    to the terminal.
    """
    data_buffer = b""
    while len(data_buffer) < message_len_byte_expected:
        remaining_bytes = message_len_byte_expected - len(data_buffer)
        message_from_server = socket_conn.recv(remaining_bytes)
        if message_from_server == b'':
            print("Server closed connection unexpectedly!")
            sys.exit(0)
        data_buffer += message_from_server
    msg = decode_string(data_buffer)
    # print(f"Message from client: {msg}")
    return msg


def decode_string(message: str) -> str:
    return message.decode('utf-8')

def encode_string(message: str) -> bytes:
    return message.encode('utf-8')


# https://stackoverflow.com/questions/21120947/catching-keyboardinterrupt-in-python-during-program-shutdown
# use try/except with keyboard interrupt as ctrl + c is not working when socket waits
if __name__ == '__main__':
    try:
        ascii_game_client_program()
    except KeyboardInterrupt:
        print('Interrupted')
