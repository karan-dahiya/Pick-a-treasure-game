from Player import Player
from Board import Board
from asyncio import run, start_server, StreamReader, StreamWriter
import struct

BUF_SIZE = 1024
HOST = '0.0.0.0'
PORT = 12345
MAX_CONNECT = 2

active_connect = 0  # Count of active player connections

async def handle_client(reader : StreamReader, writer : StreamWriter) -> None:
    """
    Handle a client connection.

    Give player a name. Set up game board.
    Read data from client and check for treasures.

    """
    global active_connect

    if active_connect >= MAX_CONNECT:
        print(" * * * New connection refused * * * ")
        return

    active_connect += 1

    player_name = "One"
    if active_connect > 1: player_name = "Two"

    # Send player name to client
    name_encoded = player_name.encode('utf-8')
    name_length = struct.pack('!H', len(name_encoded))
    writer.write(name_length)
    writer.write(name_encoded)
    await writer.drain()

    print(f"Player: {player_name} joined the game.")

    # player and game board
    player = Player(player_name)
    game_board = Board(10, 3)
    print(game_board)

    try:
        while True:
            data = await reader.read(BUF_SIZE)
            if not data:
                break

            try:
                # Process the received data
                s = data[0]
                row = (s >> 4) & 0x0F
                col = s & 0x0F

                treasure_value = game_board.pick(row, col)

                if treasure_value is not None:
                    player.add_score(treasure_value)
                    print(f"{player_name} found treasure worth {treasure_value}!")
                else:
                    print(f"{player_name}: No treasure there.")

                print(game_board)

                t = struct.pack('!HH', player.get_score(), 0)
                writer.write(t)
                await writer.drain()
            except Exception as e:
                print(f"Error for {player_name}: {e}")

    finally:
        active_connect -= 1  # Decrease active connection count
        writer.close()
        print(f"Connection closed for {player_name}")


async def main()-> None:
    """
    Main function to set up the server.

    Start the server, wait for clients to connect.
    Create a thread for each client.
    """
    print("Game Loading...")
    game_board = Board(10, 3)
    print(game_board)
    print(f"Host: {HOST}, Port: {PORT}")

    global active_connect

    server = await start_server(handle_client, HOST, PORT)
    await server.serve_forever()
    print(f'Serving on {HOST}:{PORT}')

run(main())
