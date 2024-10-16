


import socket
import selectors
import types
import queue

sel = selectors.DefaultSelector()

# Player setup
player_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
player_socket.setblocking(False)
server_address = ('192.168.0.138', 5000)  # Replace with actual server IP
player_socket.connect_ex(server_address)

# Player states and data
clients_turn = True
assigned_color = ""  # 'white' or 'black'
inbound_moves = queue.Queue()  # Queue to store incoming moves
connection_code = ""  # Four-digit connection code
connected = False

# Register socket with the selector
events = selectors.EVENT_READ | selectors.EVENT_WRITE
data = types.SimpleNamespace(outb=b"", connection_code="", color="")
sel.register(player_socket, events, data=data)

print("Connected to the chess server.")


# Public functions

def send_outgoing_move(move):
    """Send a chess move to the server."""
    data.outb = f"MOVE:{move}".encode()
    sel.modify(player_socket, selectors.EVENT_WRITE, data=data)


def attempt_to_receive_move():
    """Check if there are inbound moves, return if available."""
    if not inbound_moves.empty():
        return inbound_moves.get()
    return None


def host_connection(code, color):
    """Host a game by sending the HOST command."""
    data.outb = f"HOST:{code}:{color}".encode()
    data.connection_code = code
    data.color = color
    sel.modify(player_socket, selectors.EVENT_WRITE, data=data)


def join_hosted_connection(code):
    """Join an existing hosted game by sending the CONNECT command."""
    data.outb = f"CONNECT:{code}".encode()
    sel.modify(player_socket, selectors.EVENT_WRITE, data=data)


# Private functions

def check_connection():
    """Check and handle server events."""
    events = sel.select(timeout=1)
    if events:
        for key, mask in events:
            service_connection(key, mask)


def service_connection(key, mask):
    global connected, assigned_color, clients_turn

    """Handle events (read/write) for the socket."""
    sock = key.fileobj
    data = key.data

    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(1024).decode()  # Read server response
        if recv_data.startswith("MOVE:"):
            move = recv_data.split("MOVE:")[1]
            inbound_moves.put(move)
            clients_turn = True
        elif recv_data.startswith("CONNECTED:"):
            print("Connected to opponent!")
            connected = True
            color = recv_data.split(":")[1]
            assigned_color = color
            print(f"Assigned color: {color}")
            if color == "black":
                clients_turn = False

        elif recv_data.startswith("CONNECT:"):
            print("No matching host found with that code.")

    if mask & selectors.EVENT_WRITE and data.outb:
        #if its a move set clients turn to false
        if data.outb.startswith(b"MOVE:"):
            clients_turn = False
        sent = sock.send(data.outb)  # Send data to server and return bytes sent
        data.outb = data.outb[sent:]  # Clear buffer after sending





#TESTING

'''
#player one
input_code = input("Enter a four digit connection code: ")
host_connection(input_code, "white")

while True:
    check_connection()
    move = attempt_to_receive_move()
    if move:
        print(f"Received move: {move}")
        send_outgoing_move("e4")
    if connected:
        print("Connected to opponent!")
        break
        
'''


#--------------------------------------------------------------



'''
#-------------------
#player two

input_code = input("Enter the 4 digit connection code of opponent: ")
join_hosted_connection(input_code)

while True:
    check_connection()
    move = attempt_to_receive_move()
    if move:
        print(f"Received move: {move}")
        send_outgoing_move("e5")
    if connected:
        print("Connected to opponent!")
        break

#--------------------------------------------------------------
#--------------------------------------------------------------
        
'''





