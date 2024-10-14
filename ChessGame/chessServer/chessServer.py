import socket

# Server setup
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('0.0.0.0', 5000))  # Bind to all available interfaces on port 5000
server_socket.listen(2)  # Allow two connections (for the two players)

print("Server is waiting for players to connect...")

# Accept connections from two clients
player1_socket, player1_address = server_socket.accept()
print(f"Player 1 connected from {player1_address}")

player2_socket, player2_address = server_socket.accept()
print(f"Player 2 connected from {player2_address}")


def send_colors():
    player1_socket.send("white".encode("utf-8"))
    player2_socket.send("black".encode("utf-8"))
    print("colors sent")


# Function to relay moves between players
def relay_moves():
    while True:
        # Receive a move from Player 1
        move = player1_socket.recv(1024).decode('utf-8')
        if not move:
            break
        print(f"Player 1 move: {move}")
        # Send the move to Player 2
        player2_socket.send(move.encode('utf-8'))
        print("data sent to player 2")

        # Receive a move from Player 2
        move = player2_socket.recv(1024).decode('utf-8')
        if not move:
            break
        print(f"Player 2 move: {move}")
        # Send the move to Player 1
        player1_socket.send(move.encode('utf-8'))
        print("data sent to player 1")


send_colors()
relay_moves()

# Close connections
player1_socket.close()
player2_socket.close()
server_socket.close()