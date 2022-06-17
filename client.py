import socket
from time import sleep


def client(HOST, PORT, server_response, client_message):        
    client_message = client_message   

    with socket.socket() as so:
        while True:
            try:
                so.connect((HOST, PORT))
                so.sendall(client_message.encode())                        
                data_client = so.recv(1024)
                if str(data_client.decode()) == str(server_response):
                    print(f'Server response: {data_client.decode()}')                                             
                sleep(1)               
                break
            
            except ConnectionRefusedError:
                sleep(0.5)
        so.close()  
               
    with socket.socket() as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen(1)
        conn, addr = s.accept()
        print(f"Connected by {addr}")
        with conn: 
            while True:                   
                data = conn.recv(1024)
                if data.decode() != str(server_response):                            
                    print(f'From client: {data.decode()}')                               
                    client_message = data.decode()
                if not data:
                    break
                conn.send(server_response.encode()) 
                                   
                s.close()                       
                sleep(1)
                break

HOST = '127.0.0.1'
PORT = 64260
server_response = 'Ok'
client_message = 'Hi, it is a message from client2'

client(HOST, PORT, server_response, client_message)