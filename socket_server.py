import time
import socket
import random
from socket import AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR


conn_client_socket, conn_client_addr = None, None

def ascii_game_server_program() -> None:
    """
    This function acts as a server program.

    It creates a new socket which binds to a specified host/port.  It then waits to accept incoming connections.

    Messages can then be sent and received from a connected client.  If the client disconnects or an exception occurs, it handles
    this and waits for a new client to connect.
    """
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

    # reference: https://docs.python.org/3/library/socket.html
    # reference textbook pg. 164
    # accept incoming connection, send back string, then close socket
    # reference: https://docs.python.org/3/howto/sockets.html
    global conn_client_socket
    global conn_client_addr

    while True:

        # connect to a client if not already connected
        try:
            if conn_client_socket is None or conn_client_addr is None:
                print("Server is now listening...")
                conn_client_socket, conn_client_addr = server_socket.accept()  # michael - can potentially hang here forever if not careful
                print(f"Connected to a client! Socket: {conn_client_socket}  Addr: {conn_client_addr} ")
        except Exception as e:
            print(f"Error creating new connection with client: {e}")
            continue

        # get message from client
        # handle exceptions by closing sockets and re-looping, which will hang at server_socket.accept() until a new socket connects
        try:
            print("Awaiting message from client...")
            msg_len = get_message_len(conn_client_socket)  # we always receive a 4 byte number for message length
            msg_from_client = get_message_str_from_client(conn_client_socket, msg_len)  # then we can use that number in next loop
            print(f"Message from client: {msg_from_client}")
            if msg_from_client == "play blackjack":
                print(f"Client requested to play blackjack!")
                play_blackjack()
        except Exception as e:
            print(f"Error: {e}")
            conn_client_socket, conn_client_addr = None, None
            continue

        # send response to client
        message = input("\nEnter Input > ")
        if message == '/q':
            send_disconnect_request_to_client(message)
            continue

        send_message_to_client(message, conn_client_socket)


def send_disconnect_request_to_client(message):
    print("Sending \q to end connection with server!")
    send_message_to_client(message, conn_client_socket)
    time.sleep(2) # give client 2 seconds to exit
    conn_client_socket.close()


def send_message_to_client(message: str, socket_conn: socket.socket) -> None:
    """
    This function sends a message to the client.  It first takes the message to be sent and calculates its size as a 32 bit integer.
    The integer is then sent to the client so that it knows how much data to expect from the incoming message.

    Then, the actual message is sent as a stream of bytes to the client.

    If there is some type of exception, the server raises an exception so that the server does not crash.
    """
    # https://realpython.com/python-sockets/
    message_to_bytes = encode_string(message)
    message_len = len(message_to_bytes)
    message_len_to_fixed_byte_size = message_len.to_bytes(4, byteorder='big')
    # print(f"Sending Bytes to Server (Hex 0x): {hex(int.from_bytes(message_len_to_fixed_byte_size, byteorder='big'))}")
    try:
        socket_conn.send(message_len_to_fixed_byte_size)
        socket_conn.send(message_to_bytes)
    except:
        print("Error sending message to client!")
        raise Exception


# Reference:
# https://enzircle.hashnode.dev/handling-message-boundaries-in-socket-programming#heading-method-3-message-length-header
def get_message_len(socket_conn: socket.socket) -> int:
    """
    This function should get the message length expected from the client.  The below recv() will hang until we receive data.

    We loop while we haven't received the expected number of bytes as we might not receive everything at once.  This function should always receive 4 bytes,
    for a 32 bit integer, telling us the length of the expected message to be received.

    If the client unexpectedly closes  recv() will return an empty bytes object b''.  This is handled by the function raising an exception to its parent,
    so that the server can loop back and hang on accept() to wait for a new socket client connection.
    """
    expected_num_bytes = 4
    data_buffer = b""
    while len(data_buffer) < expected_num_bytes:
        remaining_bytes = expected_num_bytes - len(data_buffer)
        message_from_client = socket_conn.recv(remaining_bytes)
        if message_from_client == b'':
            print("Client closed connection unexpectedly!")
            raise Exception
        data_buffer += message_from_client
    msg_len = int.from_bytes(data_buffer, byteorder="big")
    print(f"Message length is : {msg_len}")
    return msg_len


# Reference:
# https://enzircle.hashnode.dev/handling-message-boundaries-in-socket-programming#heading-method-3-message-length-header
def get_message_str_from_client(socket_conn: socket.socket, message_len_byte_expected: int) -> str:
    """
    This function should get a full message from the client.  The below recv() will hang until we receive data.

    We loop while we haven't received the expected number of bytes as we might not receive everything at once.  The length of the expected message is
    received earlier and passed into this function.

    If the client unexpectedly closes recv() will return an empty bytes object b''.  This is handled by the function raising an exception to its parent,
    so that the server can loop back and hang on accept() to wait for a new socket client connection.
    """
    data_buffer = b""
    while len(data_buffer) < message_len_byte_expected:
        remaining_bytes = message_len_byte_expected - len(data_buffer)
        message_from_client = socket_conn.recv(remaining_bytes)
        if message_from_client == b'':
            print("Client closed connection unexpectedly!")
            raise Exception
        data_buffer += message_from_client
    msg = decode_string(data_buffer)
    # print(f"Message from client: {msg}")
    if msg == '/q':
        print("Client closed connection!")
        socket_conn.close()
        raise Exception
    return msg


def decode_string(message: str) -> str:
    return message.decode('utf-8')

def encode_string(message: str) -> bytes:
    return message.encode('utf-8')


def play_blackjack():
    blackjack_game = Blackjack()
    # print(blackjack_game.get_deck())

    # play 3 rounds then decide winner so should have enough cards hopefully
    while blackjack_game.get_turn_count() < 3:
        blackjack_game.deal_first_cards_out()
        val = blackjack_game.play_server_turn()
        if val == -1:
            print("server disconnected")
            return
        send_message_to_client(f"Server turn results.  Server hand value: {blackjack_game.server_hand_value}.  Server cards: {blackjack_game.server_hand}. Press any key to continue.", conn_client_socket)
        msg_len = get_message_len(conn_client_socket)  # we always receive a 4 byte number for message length
        msg_from_client = get_message_str_from_client(conn_client_socket, msg_len)  # then we can use that number in next loop
        print("Awaiting client's turn...")
        val = blackjack_game.play_client_turn()
        if val == -1:
            print("client disconnected")
            return
        print("Awaiting dealer's turn...")
        blackjack_game.play_dealer_turn()
        blackjack_game.calculate_round_result()
        blackjack_game.increment_turn_count()

    blackjack_game.calculate_winner()


class Blackjack():

    def __init__(self):
        card_values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'jack', 'queen', 'king', 'ace']
        card_suits = ['spades', 'clubs', 'hearts', 'diamonds']
        self._dealer_deck = [(suite, val) for suite in card_suits for val in card_values]
        random.shuffle(self._dealer_deck)
        self.server_score = 0
        self.client_score = 0
        self._turn_count = 1
        self.client_hand = []
        self.server_hand = []
        self.dealer_hand = []
        self.client_hand_value = 0
        self.server_hand_value = 0
        self.dealer_hand_value = 0

    def get_deck(self):
        return self._dealer_deck

    def deal_card_out(self):
        return self._dealer_deck.pop(0)

    def get_turn_count(self):
        return self._turn_count

    def increment_turn_count(self):
        self._turn_count += 1

    def deal_first_cards_out(self):
        self.client_hand = []
        self.server_hand = []
        self.dealer_hand = []
        self.client_hand.append(self.deal_card_out())
        self.server_hand.append(self.deal_card_out())
        self.dealer_hand.append(self.deal_card_out())
        self.client_hand.append(self.deal_card_out())
        self.server_hand.append(self.deal_card_out())
        self.dealer_hand.append(self.deal_card_out())

    def calculate_hand_value(self, hand):
        hand_val = 0
        for card in hand:
            card_value = card[1]
            if card_value in [ 'jack', 'queen', 'king']:
                card_value = 10
            if card_value == 'ace':
                card_value = 11
            hand_val += int(card_value)

        # see if bust and if so see if any aces can be turned to 1s
        if hand_val > 21:
            for card in hand:
                card_value = card[1]
                if card_value == 'ace':
                    hand_val -= 10
        return hand_val

    def play_server_turn(self):
        server_choice = 0
        while server_choice != '2':
            self.server_hand_value = self.calculate_hand_value(self.server_hand)
            print(f"Server hand value: {self.server_hand_value}  Server Cards: {self.server_hand}")
            if self.server_hand_value > 21:
                print("Server busted!")
                return 0
            print("Server's Turn: Enter 1 to hit, 2 to stay.")
            server_choice = input("\nEnter Input > ")
            if server_choice == '/q':
                send_disconnect_request_to_client('/q')
                return -1
            if server_choice == '1':
                server_dealt_card = self.deal_card_out()
                self.server_hand.append(server_dealt_card)
        return 0

    def play_client_turn(self):
        client_choice = 0

        while client_choice != '2':
            self.client_hand_value = self.calculate_hand_value(self.client_hand)
            if self.client_hand_value > 21:
                print("Client busted!")
                send_message_to_client("Client busted! Press any key to continue.", conn_client_socket)
                msg_len = get_message_len(conn_client_socket)  # we always receive a 4 byte number for message length
                client_choice = get_message_str_from_client(conn_client_socket, msg_len)  # then we can use that number in next loop
                return 0
            send_message_to_client(f"Client's Turn: Enter 1 to hit, 2 to stay.  Client's cards: {self.client_hand}  Client hand value: {self.client_hand_value} ", conn_client_socket)
            print(f"Server awaiting client's turn: Client's cards: {self.client_hand} ")
            msg_len = get_message_len(conn_client_socket)  # we always receive a 4 byte number for message length
            client_choice = get_message_str_from_client(conn_client_socket, msg_len)  # then we can use that number in next loop
            if client_choice == '/q':
                send_disconnect_request_to_client('/q')
                return -1
            if client_choice == '1':
                client_dealt_card = self.deal_card_out()
                self.client_hand.append(client_dealt_card)
                print(f"Info for Server: Client got card: {client_dealt_card}.")
                send_message_to_client(f"Client got card: {client_dealt_card}. Press any key to continue.", conn_client_socket)
                msg_len = get_message_len(conn_client_socket)  # we always receive a 4 byte number for message length
                continue_str = get_message_str_from_client(conn_client_socket, msg_len)  # then we can use that number in next loop

        return 0

    def play_dealer_turn(self):

        self.dealer_hand_value = self.calculate_hand_value(self.dealer_hand)

        while self.dealer_hand_value < 17:
            if self.dealer_hand_value > 21:
                continue
            dealer_dealt_card = self.deal_card_out()
            self.dealer_hand.append(dealer_dealt_card)
            self.dealer_hand_value = self.calculate_hand_value(self.dealer_hand)

        print(f"Dealer's Hand Value: {self.dealer_hand_value}  Dealer's Cards: {self.dealer_hand}")
        send_message_to_client(f"Dealer's Hand Value: {self.dealer_hand_value} Dealer's Cards: {self.dealer_hand}.  Press any key to continue.", conn_client_socket)
        msg_len = get_message_len(conn_client_socket)  # we always receive a 4 byte number for message length
        msg_from_client = get_message_str_from_client(conn_client_socket, msg_len)  # then we can use that number in next loop


    def calculate_round_result(self):

        server_win = False
        client_win = False

        if self.dealer_hand_value > 21:
            if self.client_hand_value < 22:
                self.client_score += 100
                client_win = True
            if self.server_hand_value < 22:
                self.server_score += 100
                server_win = True
        else:
             if self.client_hand_value >= self.dealer_hand_value:
                self.client_score += 100
                client_win = True
             if self.server_hand_value >= self.dealer_hand_value:
                self.server_score += 100
                server_win = True

        print(f"Server Wins Round?: {server_win}  Client Wins Round?: {client_win}  Client Score: {self.client_score} Server Score: {self.server_score} ")
        send_message_to_client(f"Server Wins Round?: {server_win}  Client Wins Round?: {client_win}  Client Score: {self.client_score} Server Score: {self.server_score}.  Press any key to continue.", conn_client_socket)
        msg_len = get_message_len(conn_client_socket)  # we always receive a 4 byte number for message length
        msg_from_client = get_message_str_from_client(conn_client_socket, msg_len)  # then we can use that number in next loop

    def calculate_winner(self):

        if self.client_score == self.server_score:
            print(f"GAME OVER - Tie!  Client Score: {self.client_score} Server Score: {self.server_score}. Resuming normal chat function.")
            send_message_to_client(f"GAME OVER - Tie!  Client Score: {self.client_score} Server Score: {self.server_score}. Press any key to continue and resume normal chat function.", conn_client_socket)
        elif self.client_score > self.server_score:
            print(f"GAME OVER - Client Wins!  Client Score: {self.client_score} Server Score: {self.server_score}. Resuming normal chat function.")
            send_message_to_client(f"GAME OVER - Client Wins!  Client Score: {self.client_score} Server Score: {self.server_score}.  Press any key to continue and resume normal chat function.", conn_client_socket)
        else:
            print(f"GAME OVER - Server Wins!  Client Score: {self.client_score} Server Score: {self.server_score}. Resuming normal chat function.")
            send_message_to_client(f"GAME OVER - Server Wins!  Client Score: {self.client_score} Server Score: {self.server_score}.  Press any key to continue and resume normal chat function.", conn_client_socket)

        msg_len = get_message_len(conn_client_socket)  # we always receive a 4 byte number for message length
        msg_from_client = get_message_str_from_client(conn_client_socket, msg_len)  # then we can use that number in next loop





# https://stackoverflow.com/questions/21120947/catching-keyboardinterrupt-in-python-during-program-shutdown
# use try/except with keyboard interrupt as ctrl + c is not working when socket waits
if __name__ == '__main__':
    try:
        ascii_game_server_program()
    except KeyboardInterrupt:
        print('Interrupted')

