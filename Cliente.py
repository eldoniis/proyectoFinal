import os
import socket
import threading

username = input("Enter your username: ")

host = '127.0.0.1'
port = 8080

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host, port))


def receive_messages():
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message == "@username":
                client.send(username.encode("utf-8"))
            elif message == "img":
                receive_image()
            else:
                print(message)

        except Exception as e:
            print("An error occurred:", e)
            client.close()
            break


def write_messages():
    while True:
        entrada = input('')
        if entrada == 'img':
            image_path = "image.png"
            if os.path.exists(image_path):
                send_image(image_path)
            else:
                print("File not found.")
        else:
            message = f"{username}: {entrada}"
            client.send(message.encode('utf-8'))


def send_image(image_path):
    client.send("img".encode("utf-8"))
    with open(image_path, "rb") as file:
        img_data = file.read(2048)
        while img_data:
            client.send(img_data)
            img_data = file.read(2048)


def receive_image():
    file_name = client.recv(1024).decode("utf-8")
    file = open(file_name, "wb")
    img_chunk = client.recv(2048)
    while img_chunk:
        file.write(img_chunk)
        img_chunk = client.recv(2048)
    file.close()
    print(f"Image {file_name} received.")


receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

write_thread = threading.Thread(target=write_messages)
write_thread.start()
