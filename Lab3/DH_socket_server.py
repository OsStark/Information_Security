import socket

#after the secret key is shard messages are encrypted using caeser cipher
def encrypt(text,s):
   result = ""
   # transverse the plain text
   for i in range(len(text)):
      char = text[i]
      # Encrypt uppercase characters in plain text
      
      if (char == " "):
        result += " "
      elif (char.isupper()):
         result += chr((ord(char) + s-65) % 26 + 65)
      # Encrypt lowercase characters in plain text
      else:
         result += chr((ord(char) + s - 97) % 26 + 97)
   return result

def server_program():

    secret = -1
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
        if secret==-1: #the first message from the client has p, q and the client's public key
            data = list(data.split(' '))
            data = [int(x) for x in data]
            p = data[0]
            q = data[1]
            client_puk = data[2]
        else:
            #decryption using the secret key
            print("cipher text: " + data)
            data = encrypt(data, -secret)
        print("from connected user: " + str(data))
        if sent_puk:
            data = input(' -> ')
            #encryption using the secret key
            data = encrypt(data, secret)
        else:
            private_key = int(input(f"Choose a private key (smaller than {p}): ")) #the server chooses its own private key
            public_key = pow(q,private_key)%p #the server calculates its public key
            secret = pow(client_puk, private_key)%p #the server calculates the secret key
            print(f"secret: {secret}")
            data = f'{public_key}' #the first message from the server is its public key
            sent_puk = True

        conn.send(data.encode())  # send data to the client

    conn.close()  # close the connection


if __name__ == '__main__':
    server_program()