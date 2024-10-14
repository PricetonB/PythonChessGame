
import socket

# Player setup
player_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('192.168.0.138', 5000)  # Replace 'server_ip_address' with the actual IP of the server
player_socket.connect(server_address)
turn = "white"
assigned_color = ""
print("Connected to the chess server.") 




def get_color():
    global turn
    global assigned_color
    color = player_socket.recv(1024).decode('utf-8')
    if color == "white":
        assigned_color = "white"
        turn = "white"
        print("You are playing as white.")
    else:
        assigned_color = "black"
        turn = "black"
        print("You are playing as black.")


def send_move(move):
    global turn
    player_socket.send(move.encode('utf-8'))
    turn = "black"
    print("Move sent.")


def receive_move():
    global turn
    turn = "white"
    move = player_socket.recv(1024).decode('utf-8')
    print("Move received.")
    return move



