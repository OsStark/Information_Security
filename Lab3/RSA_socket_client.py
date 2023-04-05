import socket
import RSAE

def client_program():
    #Client's public and private keys

    p = int(input("Enter a prime number (eg, 17, 19, 23, etc): "))
    q = int(input("Enter another prime number (Not same one you entered above): "))

    public_key, private_key = RSAE.generate_key_pair(p, q)

    print("Your public key is ", public_key, " and your private key is ", private_key)
    
    #Server's public key
    server_puk = (0,0)

    host = socket.gethostname()  # as both code is running on same pc
    port = 5000  # socket server port number

    client_socket = socket.socket()  # instantiate
    client_socket.connect((host, port))  # connect to the server

    message = f'{public_key[0]} {public_key[1]}'  # take input

    while True:
        #the sent message is encrypted using the server's public key
        if server_puk != (0,0):
            message = RSAE.encrypt(server_puk, message)
            message = ' '.join(map(lambda x: str(x), message))
        client_socket.send(message.encode())  # send message
        data = client_socket.recv(1024).decode()  # receive response
        data = list(data.split(' '))
        data = [int(x) for x in data]
        if server_puk == (0,0):
            server_puk = (data[0],data[1])
        else:
            #the received message is decrypted using the client's private key
            print(f"cipher text: {data}")
            data = RSAE.decrypt(private_key, data)
        print('Received from server: ' + str(data))  # show in terminal

        message = input(" -> ")  # again take input

    client_socket.close()  # close the connection


if __name__ == '__main__':
    client_program()