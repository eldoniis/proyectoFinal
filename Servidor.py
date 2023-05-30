import socket
import threading


host = '127.0.0.1'
port = 8080

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind((host, port))
server.listen()
print(f"Server running on {host}:{port}")

clients = []
usernames = []


def broadcast(message, _client):
    for client in clients:
        if client != _client:
            client.send(message)


def handle_messages(client):
    while True:
        try:
            message = client.recv(1024)
            if message == b'img':
                receive_image(client)
            else:
                broadcast(message, client)
        except:
            index = clients.index(client)
            username = usernames[index]
            broadcast(f"ChatBot: {username} disconnected".encode('utf-8'), client)
            clients.remove(client)
            usernames.remove(username)
            client.close()
            break


def receive_connections():
    while True:
        client, address = server.accept()

        client.send("@username".encode("utf-8"))
        username = client.recv(1024).decode('utf-8')

        clients.append(client)
        usernames.append(username)

        print(f"{username} is connected with {str(address)}")

        message = f"ChatBot: {username} joined the chat!".encode("utf-8")
        broadcast(message, client)
        client.send("Connected to server".encode("utf-8"))

        thread = threading.Thread(target=handle_messages, args=(client,))
        thread.start()


def receive_image(client):
    file_name = "received_image.png"
    file = open(file_name, "wb")
    img_chunk = client.recv(2048)
    while img_chunk:
        file.write(img_chunk)
        img_chunk = client.recv(2048)
    file.close()

    broadcast(f"Image received from {usernames[clients.index(client)]}".encode("utf-8"), client)


receive_thread = threading.Thread(target=receive_connections)
receive_thread.start()
