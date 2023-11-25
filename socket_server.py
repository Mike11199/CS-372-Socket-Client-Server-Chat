import socket
from socket import AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR

conn_client_socket, conn_client_addr = None, None

def ascii_game_server_program():

    server_host = '127.0.0.1' # local host
    server_port = 65535  # limit as 2^16 port numbers
    print(f"Host: {server_host}")
    print(f"Port: {server_port}")

    # set up socket
    server_socket = socket.socket(AF_INET, SOCK_STREAM)

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
    # reference: https://docs.python.org/3/howto/sockets.html
    global conn_client_socket
    global conn_client_addr
    while True:

        # this section so we can reuse the same socket, but create a new one if we close it
        if conn_client_socket is None or conn_client_addr is None:
            conn_client_socket, conn_client_addr = server_socket.accept()  # michael - can potentially hang here forever if not careful
            print("Connected to a client!")
            print(conn_client_socket)
            print(conn_client_addr)

        # get message from client
        try:
            print("Awaiting message from client...")
            msg_len = get_message_len(conn_client_socket)  # we always receive a 4 byte number for message length
            msg_from_client = get_message_str_from_client(conn_client_socket, msg_len)  # then we can use that number in next loop
            print(f"Message from client: {msg_from_client}")
        except:
            print("Server is now listening...")
            continue

        # close if message is quit signal
        if msg_from_client == '\q':
            print("Client closed connection!")
            conn_client_socket.close()
        else:
            # or send response to client
            message = input("“Enter Input > ")
            if message == '\q':
                print("Sending \q to end connection with server!")
                send_message_to_client(message, conn_client_socket)
                conn_client_socket.close()
            send_message_to_client(message, conn_client_socket)




def send_message_to_client(message: str, socket_conn: socket.socket) -> None:
    # https://realpython.com/python-sockets/
    message_to_bytes = encode_string(message)
    message_len = len(message_to_bytes)
    message_len_to_fixed_byte_size = message_len.to_bytes(4, byteorder='big')
    print(f"Sending Bytes to Server (Hex 0x): {hex(int.from_bytes(message_len_to_fixed_byte_size, byteorder='big'))}")
    socket_conn.send(message_len_to_fixed_byte_size)
    socket_conn.send(message_to_bytes)


# Reference:
# https://enzircle.hashnode.dev/handling-message-boundaries-in-socket-programming#heading-method-3-message-length-header
def get_message_len(socket_conn: socket.socket) -> int:
    """
    This function should get the message length.  We don't use a loop (while data) as that will loop forever unless the socket closes.

    Instead, loop while we haven't received the expected bytes.  We should received 4 bytes, for a 32 bit integer, telling us the
    length of the expected message to be received.
    """
    global conn_client_socket
    global conn_client_addr

    expected_num_bytes = 4
    data_buffer = b""
    while len(data_buffer) < expected_num_bytes:
        remaining_bytes = expected_num_bytes - len(data_buffer)
        message_from_client = socket_conn.recv(remaining_bytes)
        if message_from_client == b'':
            print("Client closed connection unexpectedly!")
            conn_client_socket = None
            conn_client_addr = None
            raise Exception
        data_buffer += message_from_client
    msg_len = int.from_bytes(data_buffer, byteorder="big")
    print(f"Message length is : {msg_len}")
    return msg_len


# Reference:
# https://enzircle.hashnode.dev/handling-message-boundaries-in-socket-programming#heading-method-3-message-length-header
def get_message_str_from_client(socket_conn: socket.socket, message_len_byte_expected: int) -> str:
    """
    This function should get the message length.  We don't use a loop (while data) as that will loop forever unless the socket closes.

    Instead, loop while we haven't received the expected bytes.  We should received 4 bytes, for a 32 bit integer, telling us the
    length of the expected message to be received.
    """
    global conn_client_socket
    global conn_client_addr

    data_buffer = b""
    while len(data_buffer) < message_len_byte_expected:
        remaining_bytes = message_len_byte_expected - len(data_buffer)
        message_from_client = socket_conn.recv(remaining_bytes)
        if message_from_client == b'':
            print("Client closed connection unexpectedly!")
            conn_client_socket = None
            conn_client_addr = None
            raise Exception
        data_buffer += message_from_client
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
        ascii_game_server_program()
    except KeyboardInterrupt:
        print('Interrupted')

