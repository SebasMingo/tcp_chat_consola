import socket
import threading
import time

username = input("Enter your username: ")

host = '127.0.0.1'
port = 55555

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def connect_to_server():
    try:
        client.connect((host, port))
        print("Connected to the server.")
    except ConnectionRefusedError:
        print("Connection refused, please make sure the server is running.")
        exit()

def receive_messages():
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message == "@username":
                client.send(username.encode("utf-8"))
            else:
                print(message)
        except ConnectionResetError:
            print("Connection lost, reconnecting...")
            reconnect_to_server()
            break
        except Exception as e:
            print(f"An error occurred: {e}")
            client.close()
            break

def write_messages():
    while True:
        try:
            message = f"{username}: {input('')}"
            client.send(message.encode('utf-8'))
        except Exception as e:
            print(f"An error occurred while sending the message: {e}")
            client.close()
            break

def reconnect_to_server():
    while True:
        try:
            time.sleep(5)  # Esperar 5 segundos antes de intentar reconectar
            connect_to_server()
            # Volver a empezar los hilos de lectura y escritura
            receive_thread = threading.Thread(target=receive_messages)
            receive_thread.start()

            write_thread = threading.Thread(target=write_messages)
            write_thread.start()
            break
        except Exception as e:
            print(f"Reconnection attempt failed: {e}")
            continue

connect_to_server()

receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

write_thread = threading.Thread(target=write_messages)
write_thread.start()
