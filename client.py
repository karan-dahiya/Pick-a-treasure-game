from socket import socket, AF_INET, SOCK_STREAM
import struct
import sys

HOST = 'localhost'
PORT = 12345

def handle_communication(sock, player_name):
    """Handles communication between the server and client."""
    while True:
        try:
            row = int(input("Row? (0-9): "))
            col = int(input("Column? (0-9): "))

            if row < 0 or row >= 10 or col < 0 or col >= 10:
                print("Only Integers (0-9)")
                continue

            coords = (row << 4) | col
            sock.sendall(bytes([coords]))

            score_data = sock.recv(4)
            if len(score_data) == 4:
                score, = struct.unpack('!H', score_data[:2])
                print(f'Player name: {player_name}, Total Score: {score}')
            else:
                print("No update from server")

        except ValueError:
            print("Only Integers (0-9)")
            break

def client():
    """Client connects to the server.""" # Ask for player name
    with socket(AF_INET, SOCK_STREAM) as sock:
        try:
            sock.connect((HOST, PORT))
            # Receive player name from the client
            name_length_data = sock.recv(2)
            name_length = struct.unpack('!H', name_length_data)[0]
            player_name = sock.recv(name_length).decode('utf-8')


            # Enter the communication loop now that the name has been accepted
            handle_communication(sock, player_name)

        except ConnectionRefusedError:
            print("Connection refused: The server is full.")
            sys.exit()

client()
