import socket
import RSAE

def server_program():
    #Server's public and private keys

    p = int(input("Enter a prime number (eg, 17, 19, 23, etc): "))
    q = int(input("Enter another prime number (Not same one you entered above): "))

    public_key, private_key = RSAE.generate_key_pair(p, q)

    print("Your public key is ", public_key, " and your private key is ", private_key)

    #Client's public key
    client_puk = (0,0)
    sent_puk = False

    # get the hostname
    host = socket.gethostname()
    port = 5000  # initiate port no above 1024

    server_socket = socket.socket()  # get instance
    # look closely. The bind() function takes tuple as argument
    server_socket.bind((host, port))  # bind host address and port together

    # configure how many client the server can listen simultaneously
    server_socket.listen(2)
    conn, address = server_socket.accept()  # accept new connection
    print("Connection from: " + str(address))
    while True:
        # receive data stream. it won't accept data packet greater than 1024 bytes
        data = conn.recv(1024).decode()
        data = list(data.split(' '))
        data = [int(x) for x in data]
        if client_puk==(0,0):
            client_puk = (data[0],data[1])
        else:
            #the received message is decrypted using the server's private key
            print(f"cipher text: {data}")
            data = RSAE.decrypt(private_key, data)
        print("from connected user: " + str(data))
        if sent_puk:
            data = input(' -> ')
            #the sent message is encrypted using the client's public key
            data = RSAE.encrypt(client_puk, data)
            data = ' '.join(map(lambda x: str(x), data))
        else:
            data = f'{public_key[0]} {public_key[1]}'
            sent_puk = True

        conn.send(data.encode())  # send data to the client

    conn.close()  # close the connection


if __name__ == '__main__':
    server_program()