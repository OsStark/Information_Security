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

def client_program():

    #the client chooses p, q and its private key
    p = int(input(f"Enter a prime number: "))
    q = int(input(f"Enter a primitive root of {p}: "))
    private_key = int(input(f"Choose a private key (smaller than {p}): "))
    public_key = pow(q,private_key)%p #the client calculates its public key
    
    secret = -1

    host = socket.gethostname()  # as both code is running on same pc
    port = 5000  # socket server port number

    client_socket = socket.socket()  # instantiate
    client_socket.connect((host, port))  # connect to the server

    message = f'{p} {q} {public_key}'  #the first message by the client has p, q and its public key

    while True:
        if secret != -1:
            #encryption using the secret key
            message = encrypt(message, secret)
        client_socket.send(message.encode())  # send message
        data = client_socket.recv(1024).decode()  # receive response
        if secret == -1:
            server_puk = int(data) #the first message by the server is its public key
            secret = pow(server_puk, private_key)%p #the client calculates the secret key
            print(f"secret: {secret}")
        else:
            #decryption using the secret key
            print("cipher text: " + data)
            data = encrypt(data, -secret)
        print('Received from server: ' + str(data))  # show in terminal

        message = input(" -> ")  # again take input

    client_socket.close()  # close the connection


if __name__ == '__main__':
    client_program()