import os
from tqdm import tqdm
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

            if message != "img":
                if message == "@username":
                    client.send(username.encode("utf-8"))
                else:
                    print(message)
            else:
                fileName = client.recv(1024).decode()
                print(fileName)
                fileSize = client.recv(1024).decode()
                print(fileSize)

                file = open(fileName, "wb")
                file_bytes = b""

                done = False

                progress = tqdm.tqdm(unit="B", unit_scale=True, unit_divisor=1000,
                                     total=int(fileSize))

                while not done:
                    data = client.recv(1024)
                    if file_bytes[-5:] == b"<END>":
                        done = True
                    else:
                        file_bytes += data 
                    progress.update(1024)

                file.write(file_bytes)
                file.close()
                                             
                
            
        except:
            print("An error Ocurred")
            client.close
            break

def write_messages():
    while True:
        entrada = input('')
        if entrada == 'img':
            file = open("image.png","rb")
            fileSize = os.path.getsize("image.png")

            client.send(entrada.encode('utf-8'))
            client.send(str(fileSize).encode())

            data = file.read()
            client.sendall(data)
            client.send(b"<END>")

            file.close()
        else:
            message = f"{username}: {entrada}"
            client.send(message.encode('utf-8'))

receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

write_thread = threading.Thread(target=write_messages)
write_thread.start()
