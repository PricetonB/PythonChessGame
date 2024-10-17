
#clients turn needs set at connection and not touched ungain unless pygame

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

    


def attempt_to_receive_move():
    """Check if there are inbound moves, return if available."""
    if not inbound_moves.empty():
        move = inbound_moves.get()
        return move
        
    return None


def host_connection(code, color):

    """Host a game by sending the HOST command."""
    data.outb = f"HOST:{code}:{color}".encode()
    data.connection_code = code
    data.color = color





def join_hosted_connection(code):
    """Join an existing hosted game by sending the CONNECT command."""
    data.outb = f"CONNECT:{code}".encode()
    data.connection_code = code



# Private functions

def check_connection():
    """Check and handle server events."""
    events = sel.select(timeout=1)
    if events:
        for key, mask in events:
            service_connection(key, mask)


def service_connection(key, mask):
    global connected, assigned_color, clients_turn, connection_code

    """Handle events (read/write) for the socket."""
    sock = key.fileobj
    data = key.data

    if mask & selectors.EVENT_READ:
        #if data is empty string print empty string sent
        if not data.outb:
            print("empty string sent to us")
        recv_data = sock.recv(1024).decode()  # Read server response

        if recv_data.startswith("MOVE:"):
            move = recv_data.split("MOVE:")[1]
            inbound_moves.put(move)


        elif recv_data.startswith("CONNECTED:"):
            print("Connected to opponent!")
            color = recv_data.split(":")[1]
            assigned_color = color
            connection_code = data.connection_code
            if color == "black":
                clients_turn = False
            else:
                clients_turn = True
            connected = True




        elif recv_data.startswith("CONNECT:"):
            print("No matching host found with that code.")

    if mask & selectors.EVENT_WRITE and data.outb:

        #if its a move set clients turn to false
        if data.outb.startswith(b"MOVE:"):
            print(f"Sending move: {data.outb}")

        sent = sock.send(data.outb)  # Send data to server and return bytes sent  
        data.outb = data.outb[sent:]  # Clear buffer after sending





#TESTING


#player one
input_code = input("Enter a four digit connection code: ")
host_connection(input_code, "white")



while True:
    check_connection()

    if connected:
        if clients_turn:
            print("Your turn!")
            input_move = input("Enter a move like A2A4: ")
            send_outgoing_move(input_move)
            clients_turn = False



        else:

            move = attempt_to_receive_move()
            if move:
                clients_turn = True
                print(f"Received move: {move}")










        



#--------------------------------------------------------------



'''
#-------------------
#player two

input_code = input("Enter the 4 digit connection code of opponent: ")
join_hosted_connection(input_code)

while True:
    check_connection()

    if connected:
        if clients_turn:
            print("Your turn!")
            input_move = input("Enter a move like A2A4: ")
            send_outgoing_move(input_move)
            clients_turn = False



        else:

            move = attempt_to_receive_move()
            if move:
                clients_turn = True
                print(f"Received move: {move}")

#--------------------------------------------------------------
#--------------------------------------------------------------
        
'''


















'''
import socket
import selectors
import types



# 



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
data = types.SimpleNamespace(outb=b"") #feel free to add parameters here as needed
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

