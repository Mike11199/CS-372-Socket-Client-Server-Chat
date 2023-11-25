from socket import *
import sys



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
    # reference: https://docs.python.org/3/howto/sockets.html
    conn_client_socket, conn_client_addr = None, None
    while True:

        # this section so we can reuse the same socket, but create a new one if we close it
        if conn_client_socket is None or conn_client_addr is None:
            conn_client_socket, conn_client_addr = server_socket.accept()  # michael - can potentially hang here forever if not careful
            print(conn_client_socket)
            print(conn_client_addr)

        msg_len = get_message_len(conn_client_socket)  # we always receive a 4 byte number for message length
        msg_from_client = get_message_str_from_client(conn_client_socket, msg_len)  # then we can use that number in next loop
        print(msg_from_client)
        # conn_client_socket.close()


# Reference:
# https://enzircle.hashnode.dev/handling-message-boundaries-in-socket-programming#heading-method-3-message-length-header
def get_message_len(socket_connection) -> int:
    """
    This function should get the message length.  We don't use a loop (while data) as that will loop forever unless the socket closes.

    Instead, loop while we haven't received the expected bytes.  We should received 4 bytes, for a 32 bit integer, telling us the
    length of the expected message to be received.
    """
    expected_num_bytes = 4
    data_buffer = b""
    while len(data_buffer) < expected_num_bytes:
        remaining_bytes = expected_num_bytes - len(data_buffer)
        data_buffer += socket_connection.recv(remaining_bytes)
    msg_len = int.from_bytes(data_buffer, byteorder="big")
    print(f"Message length is : {msg_len}")
    return msg_len

# Reference:
# https://enzircle.hashnode.dev/handling-message-boundaries-in-socket-programming#heading-method-3-message-length-header
def get_message_str_from_client(socket_connection, message_len_byte_expected) -> int:
    """
    This function should get the message length.  We don't use a loop (while data) as that will loop forever unless the socket closes.

    Instead, loop while we haven't received the expected bytes.  We should received 4 bytes, for a 32 bit integer, telling us the
    length of the expected message to be received.
    """
    data_buffer = b""
    while len(data_buffer) < message_len_byte_expected:
        remaining_bytes = message_len_byte_expected - len(data_buffer)
        data_buffer += socket_connection.recv(remaining_bytes)
    msg = decode_string(data_buffer)
    print(f"Message is : {msg}")
    return msg


def decode_string(str):
    return str.decode('utf-8')

def encode_string(str):
    return str.encode('utf-8')



# https://stackoverflow.com/questions/21120947/catching-keyboardinterrupt-in-python-during-program-shutdown
# use try/except with keyboard interrupt as ctrl + c is not working when socket waits
if __name__ == '__main__':
    try:
        ascii_game_server_program()
    except KeyboardInterrupt:
        print('Interrupted')
        sys.exit(130)
