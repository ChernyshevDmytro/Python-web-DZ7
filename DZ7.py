import socket
from time import sleep
import threading

def server_client(host, port, server_response, client_message, flag, counter):
    initial_counter = 0
    flag = flag
    client_message = client_message
    while  int(counter) >= initial_counter:
    
        try:       
            if flag == "server":                
                with socket.socket() as s:
                    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                    s.bind((host, port))
                    s.listen(1)
                    conn, addr = s.accept()
                    print(f"Connected by {addr}")
                    with conn:
                        while True:                    
                            data = conn.recv(1024)
                            if data:                            
                                print(f'From client number {initial_counter}: {data.decode()}')                               
                                client_message = data.decode()
                            if not data:
                                break
                            conn.send(server_response.encode())
                            flag = "client"
                            initial_counter+=1                           
                            sleep(1)                            

            if flag == "client":                
                with socket.socket() as so:
                    so.connect((host, port))
                    so.sendall(client_message.encode())                        
                    data_client = so.recv(1024)
                    if str(data_client.decode()) == str(server_response):
                        print(f'Server response: {data_client.decode()}')
                        so.close()                        
                        flag = 'server'
                        sleep(1) 
                                         
        except ConnectionRefusedError:
            sleep(0.5)

HOST = '127.0.0.1'
PORT = 64260
server_response = 'Ok'
client_message = 'Hi, it is a message from client'
counter = 10
flag = "server"


server = threading.Thread (target=server_client, args=(HOST, PORT, server_response, client_message, flag,  counter, ))
flag = "client"
client = threading.Thread (target=server_client, args=(HOST, PORT, server_response, client_message, flag,  counter, ))

server.start()
client.start()
server.join()
client.join()
print('Done!')                              