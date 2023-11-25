from socket import *
import signal
import sys

# Reference:  https://enzircle.hashnode.dev/handling-message-boundaries-in-socket-programming#heading-method-3-message-length-header

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
    #client_socket.send(encoded_string)
    #client_socket.send(b'END TRANSMISSION')

    # print data received from server
    # https://realpython.com/python-sockets/
    LENGTH_TEST = 6
    message_len = LENGTH_TEST.to_bytes(4, byteorder='big')
    client_socket.send(message_len)

    while True:
        data = client_socket.recv(5)  # can hang here
        if not data:
            break
        print('Received: ',data.decode())
    client_socket.close()


def decode_string(str):
    return str.decode('utf-8')

def encode_string(str):
    return str.encode('utf-8')

# Reference:
# https://enzircle.hashnode.dev/handling-message-boundaries-in-socket-programming#heading-method-3-message-length-header
def get_message_length(socket_connection) -> int:
    """
    This function should get the message length.  We don't use a loop (while data) as that will loop forever unless the socket closes.

    Instead, loop while we haven't received the expected bytes.  We should received 4 bytes, for a 32 bit integer, telling us the
    length of the expected message to be received.
    """
    data_buffer = b""
    expected_total_bytes = 4
    while len(data_buffer) < expected_total_bytes:
        remaining_bytes = expected_total_bytes - len(data_buffer)
        data_buffer += socket_connection.recv(remaining_bytes)
    msg_len = int.from_bytes(data_buffer, byteorder="big")
    print(f"Message length is : {msg_len}")
    return msg_len


# https://stackoverflow.com/questions/21120947/catching-keyboardinterrupt-in-python-during-program-shutdown
# use signals as ctrl + c is not working
if __name__ == '__main__':
    try:
        ascii_game_client_program()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(130)
        except SystemExit:
            os._exit(130)