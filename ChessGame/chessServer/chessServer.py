
import socket
import selectors
import types

sel = selectors.DefaultSelector()

# Dictionary to store client data (socket, color, opponent) key is connection code
client_data = {}

# Server setup
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setblocking(False)
server_socket.bind(('0.0.0.0', 5000))  # Bind to all network interfaces
server_socket.listen()
sel.register(server_socket, selectors.EVENT_READ, data=None)

print("Server is waiting for players to connect...")


def accept_connection(sock):
    """Accept incoming client connections."""
    conn, addr = sock.accept()
    print(f"Accepted connection from {addr}")
    conn.setblocking(False)
    data = types.SimpleNamespace(outb=b"", connection_code="", color="", opponent=None)
    sel.register(conn, selectors.EVENT_READ | selectors.EVENT_WRITE, data=data)
    print("Connection registered")

def service_connection(key, mask):
    """Handle client connections for reading and writing."""
    sock = key.fileobj
    data = key.data

    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(1024).decode()
        if recv_data:
            handle_message(sock, recv_data, data)
            print("Data received.")
        else:
            print("Closing connection.")
            sel.unregister(sock)
            sock.close()

    if mask & selectors.EVENT_WRITE and data.outb:
        print(f"Data sent: {data.outb}")
        sent = sock.send(data.outb)
        data.outb = data.outb[sent:]  # Clear buffer after sending
        





def handle_message(sock, message, data):
    """Handle messages sent by clients (MOVE, HOST, CONNECT)."""
    if message.startswith("HOST:"):
        _, code, color = message.split(":")
        data.connection_code = code
        data.color = color
        client_data[code] = sock
        print(f"Hosting game with code {code}, color {color}")
        #send something back to client for testing


    elif message.startswith("CONNECT:"):
        print("Connecting players...")
        _, code = message.split(":")
        if code in client_data:
            opponent_sock = client_data[code]
            opponent_data = sel.get_key(opponent_sock).data
            data.opponent = opponent_sock
            opponent_data.opponent = sock
            data.connection_code = code
            if opponent_data.color == "white":
                data.color = "black"
            else:
                data.color = "white"

            # Notify both players

            data.outb = f"CONNECTED:{data.color}".encode()
            opponent_data.outb = f"CONNECTED:{opponent_data.color}".encode()
            print(f"Connected players with code {code}")
        else:
            data.outb = "CONNECT:No matching host found.".encode()
            print(f"No matching host found for code {code}")

    elif message.startswith("MOVE:"):
        move = message.split("MOVE:")[1]
        if data.opponent:
            opponent_data = sel.get_key(data.opponent).data
            opponent_data.outb = f"MOVE:{move}".encode()
            print(f"Relaying move to opponent: {move}")
        else:
            print("No opponent to relay move to.")


# Main loop for server
def run_server():
    while True:
        events = sel.select(timeout=None)
        for key, mask in events:
            if key.data is None:
                accept_connection(key.fileobj)
            else:
                service_connection(key, mask)


# Start the server
run_server()

