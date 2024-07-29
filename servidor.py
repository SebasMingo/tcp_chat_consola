import socket
import threading

host = '127.0.0.1'
port = 55555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()
print(f"Server running on {host}:{port}")

clients = []
usernames = []

def broadcast(message, _client=None):
    for client in clients:
        if client != _client:
            try:
                client.send(message)
            except:
                remove_client(client)

def remove_client(client):
    if client in clients:
        index = clients.index(client)
        clients.remove(client)
        username = usernames[index]
        usernames.remove(username)
        print(f"{username} has disconnected.")
        broadcast(f"ChatBot: {username} has left the chat.".encode('utf-8'))
        client.close()

def handle_messages(client):
    while True:
        try:
            message = client.recv(1024)
            if message:
                broadcast(message, client)
            else:
                remove_client(client)
                break
        except:
            remove_client(client)
            break

def receive_connections():
    while True:
        try:
            client, address = server.accept()
            print(f"Connection from {address}")

            client.send("@username".encode("utf-8"))
            username = client.recv(1024).decode('utf-8')
            clients.append(client)
            usernames.append(username)

            print(f"{username} is now connected with {address}")
            broadcast(f"ChatBot: {username} has joined the chat.".encode("utf-8"), client)
            client.send("Connected to server".encode("utf-8"))

            thread = threading.Thread(target=handle_messages, args=(client,))
            thread.start()

        except Exception as e:
            print(f"Error accepting new connection: {e}")

receive_connections()
