# TCP-Socket-Client-Server-Chat-Blackjack-Game

- Portfolio project for CS 372 - Introduction to Computer Networks.
- This project is allowed to be posted to a public GitHub repo after the class ends.
- The project implements a client/server chat program via TCP sockets.
- A multiplayer game of blackjack can also be played if the client sends the string 'play blackjack' to the server.  Game logic is hosted in a blackjack class on the server.
- First start the server with python socket_server.py.  Then the client can be started with python socket_client.py.
- At any time, the client/server can stop by sending 'q/' to the other, which will cause both programs to terminate.
- In all other cases, try/excepts handle unexpected closures of the connection by either party.  The server will continue to run and not crash regardless of what happens, and can continue to accept a client connection.

# Socket Logic Screenshots

- The client/server will always first send a 32 bit (4 byte) integer indiciating the length of the message it is going to send.  This is due to the fact that there is no EOF transmission field on a socket.
- Otherwise the client/server could hang forever on the recv() call as it waits for additional bytes
- After sending the message length. The program then sends the message itself over the socket.

![image](https://github.com/Mike11199/CS-372-Socket-Client-Server-Chat/assets/91037796/48d65eaf-b3b9-4c1e-a2bc-a22e052bff88)

- When receiving a message, the program first receives exactly 4 bytes of data telling it the message length.  Then opens the socket to receives that many bytes of data.

![image](https://github.com/Mike11199/CS-372-Socket-Client-Server-Chat/assets/91037796/eb05c2c3-2714-48b1-8826-5035a7f18184)




# Terminal Screenshots

- Server Start:

  <img src="https://github.com/Mike11199/CS-372-Socket-Client-Server-Chat/assets/91037796/f4690044-a50c-465e-816b-c9c81802c5f0" width="700" />

- Client Start:

  <img src="https://github.com/Mike11199/CS-372-Socket-Client-Server-Chat/assets/91037796/21d12683-117d-4494-ac52-c021ac4de1e6" width="700" />

- Game Start:
  
  <img src="https://github.com/Mike11199/CS-372-Socket-Client-Server-Chat/assets/91037796/4b36380c-9cf3-4fc3-9c89-a130b5bba997" width="700" />  

- Server Turn:

  <img src="https://github.com/Mike11199/CS-372-Socket-Client-Server-Chat/assets/91037796/2cea685a-ff99-4785-a5f0-0e23223f0d6c" width="700" />

- Client is notified of server's round results via socket:

  <img src="https://github.com/Mike11199/CS-372-Socket-Client-Server-Chat/assets/91037796/03e88278-cf65-4b1e-99e1-d9955e5ce1cb" width="700" />

- Round results by calculating dealer's hand versus players' hands.

  <img src="https://github.com/Mike11199/CS-372-Socket-Client-Server-Chat/assets/91037796/52dfec9b-90c5-4c1f-819c-4dc8acf63a89" width="700" />

  - Handled when a player gets blackjack:
 
  <img src="https://github.com/Mike11199/CS-372-Socket-Client-Server-Chat/assets/91037796/88fb401b-cebc-4cef-8bf4-403ae3b9b9c6" width="700" />

- Handled when a player busts - hand value over 21:
  
  <img src="https://github.com/Mike11199/CS-372-Socket-Client-Server-Chat/assets/91037796/266adace-0c64-4dd9-8d80-9575bc83eace" width="700" />

- Showed results of game to client/server then resume normal chat function over TCP sockets:

  <img src="https://github.com/Mike11199/CS-372-Socket-Client-Server-Chat/assets/91037796/015106fa-5ce5-4acd-991c-3d286d67e2ed" width="700" />


# Wireshark Packet Inspection 

- Using Wireshark to inspect localhost TCP packets between client and server socket programs.

![image](https://github.com/Mike11199/CS-372-Socket-Client-Server-Chat/assets/91037796/45ecf2e0-85bb-4dc9-9d98-8001df7624f8)

![image](https://github.com/Mike11199/CS-372-Socket-Client-Server-Chat/assets/91037796/cfa82018-8e9f-4edb-b810-2fe1f9e6f779)


