
# multiconn-client.py

import sys
import socket
import selectors
import types

sel = selectors.DefaultSelector()
messages = [b"Message 1 from client.", b"Message 2 from client."]

def start_connections(host, port, num_conns):
    server_addr = (host, port)
    for i in range(0, num_conns):
        connid = i + 1
        print(f"Starting connection {connid} to {server_addr}")
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setblocking(False)
        sock.connect_ex(server_addr)
        events = selectors.EVENT_READ | selectors.EVENT_WRITE
        data = types.SimpleNamespace(
            connid=connid,
            msg_total=sum(len(m) for m in messages),
            recv_total=0,
            messages=messages.copy(),
            outb=b"",
        )
        sel.register(sock, events, data=data)



def service_connection(key, mask):
    sock = key.fileobj
    data = key.data
    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(1024)  # Should be ready to read
        if recv_data:
            data.outb += recv_data
            print(f"Received {recv_data!r} from connection {data.connid}")
            data.recv_total += len(recv_data)
        else:
            print(f"Closing connection {data.connid}")
        if not recv_data or data.recv_total == data.msg_total:
            print(f"Closing connection {data.connid}")
            sel.unregister(sock)
            sock.close()
    if mask & selectors.EVENT_WRITE:
        if not data.outb and data.messages:
            data.outb = data.messages.pop(0)
        if data.outb:
            print(f"Echoing {data.outb!r} to {data.addr}")
            print(f"Sending {data.outb!r} to connection {data.connid}")
            sent = sock.send(data.outb)  # Should be ready to write
            data.outb = data.outb[sent:]





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

def service_connection(key, mask):
    sock = key.fileobj
    data = key.data

    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(1024)  # Non-blocking read
        if recv_data:
            handle_server_response(recv_data.decode('utf-8'))
        else:
            print("Server closed the connection.")
            sel.unregister(sock)
            sock.close()

    if mask & selectors.EVENT_WRITE and data.outb:
        print(f"Sending {data.outb!r}")
        sent = sock.send(data.outb)  # Non-blocking write
        data.outb = data.outb[sent:]

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
        print(f"Move received: {response}")

def send_move(move):
    global clients_turn
    data = sel.get_key(player_socket).data
    data.outb = move.encode('utf-8')  # Set the move to be sent
    clients_turn = False
    print(f"Move '{move}' is queued to be sent.")

# Main event loop for handling the non-blocking I/O
try:
    while True:
        events = sel.select(timeout=None)
        for key, mask in events:
            service_connection(key, mask)
finally:
    sel.close()


'''
