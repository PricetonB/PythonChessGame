

import socket
import selectors
import types

sel = selectors.DefaultSelector()

# Player setup
player_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
player_socket.setblocking(False)  # Set the socket to non-blocking mode
server_address = ('192.168.0.138', 5000)  # Replace with actual server IP
player_socket.connect_ex(server_address)  # Non-blocking connection attempt
clients_turn = True
assigned_color = ""
print("Connected to the chess server.")

# Register the socket to monitor it for read and write events
events = selectors.EVENT_READ | selectors.EVENT_WRITE
data = types.SimpleNamespace(outb=b"")
sel.register(player_socket, events, data=data)

def service_connection_for_outbound(key, mask):
    sock = key.fileobj
    data = key.data

    if mask & selectors.EVENT_WRITE and data.outb:
        print(f"Sending {data.outb!r}")
        sent = sock.send(data.outb)  # Non-blocking write
        data.outb = data.outb[sent:]


def service_connection_for_inbound(key, mask):
    sock = key.fileobj
    data = key.data

    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(1024)  # Non-blocking read
        if recv_data:
            print(f"Received {recv_data!r} in service_connection_for_inbound returning to handle_server_response.")
            return handle_server_response(recv_data.decode('utf-8'))
        else:
            print("Server closed the connection.")
            sel.unregister(sock)
            sock.close()

def handle_server_response(response):
    global clients_turn, assigned_color
    # Handle the response from the server
    if response in ("white", "black"):
        # This handles the color assignment
        assigned_color = response
        clients_turn = (response == "white")
        print(f"You are playing as {assigned_color}.")
    else:
        # Handle moves
        clients_turn = True
        print(f"Move received: {response} in handle server rsponse. returning move to main.")
        return response

def send_move(move):
    global clients_turn
    data = sel.get_key(player_socket).data
    data.outb = move.encode('utf-8')  # Set the move to be sent
    clients_turn = False
    print(f"Move '{move}' is queued to be sent.")
    service_connection_for_outbound(sel.get_key(player_socket), selectors.EVENT_WRITE)

# Main event loop for handling the non-blocking I/O

def check_server_response():
    events = sel.select(timeout=1)
    if events:
        for key, mask in events:
            move = service_connection_for_inbound(key, mask)
            if move and move != "white" and move != "black":
                print(f"Returning move: {move} from check_server_response.")
                return move








'''
# multiconn-client.py

import sys
import socket
import selectors
import types


# Player setup
player_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('192.168.0.138', 5000)  # Replace 'server_ip_address' with the actual IP of the server
player_socket.connect(server_address)
clients_turn = True
assigned_color = ""
print("Connected to the chess server.") 











def get_color():
    global clients_turn
    global assigned_color
    color = player_socket.recv(1024).decode('utf-8')
    if color == "white":
        assigned_color = "white"
        clients_turn = True
        print("You are playing as white.")
    else:
        assigned_color = "black"
        clients_turn = False
        print("You are playing as black.")


def send_move(move):
    global clients_turn
    player_socket.send(move.encode('utf-8'))
    clients_turn = False
    print("Move sent.")


def receive_move():
    global clients_turn
    clients_turn = True
    move = player_socket.recv(1024).decode('utf-8')
    print("Move received.")
    return move






'''
