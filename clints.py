from cgi import print_environ
import os
import socket
#from cmath import exp


def encrypt(text, s):  # Ceaser cipher
    result = ""

    for i in range(len(text)):
        char = text[i]

        if (char.isupper()):
            result += chr((ord(char) + s-65) % 26 + 65)

        elif (char.islower()):
            result += chr((ord(char) + s - 97) % 26 + 97)

        else:
            result += char

    return result


port = 9990
en_key = 2
de_key = (-1) * en_key

while True:

    c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    c.connect(('localhost', port))
    welcome_mes = c.recv(1024).decode()
    welcome_mes = encrypt(welcome_mes, de_key)
    print(welcome_mes)

    """
    LayerN: File Service
    -> taking every input from the user would be layerN. 
    """
    name = input(">>>")  # take the input from the user

    """ 
    Layer N-1 : Cryto layer:-
    1.  encrypt the every message that clint is sending to server
        encrypt the message before converting it into bytes format

    2.  decrpt the every message recereved from the server after converted 
         the message into string format from the bytes format. 

    """
    name = encrypt(name, en_key)

    """
    This would eb laye archicture as the cryto layer depend on what 
        ever message we are getting from the above layer.
    """

    c.send(bytes(name, 'utf-8'))
    """
    Layer N-2: Networking
    sending every message woudld be Networkinf layer. 
    """

    """
    1. While sending the message LayerN, LayerN-1 and LayerN-2 format will be follewed. 
    2. While receiveing the message LayerN-2, LayerN-1 and LayerN format will be followed. 

    """
    name = encrypt(name, de_key)
    if (name == 'cwd'):
        data = c.recv(1024).decode()  # LayerN-2
        data = encrypt(data, de_key)  # LayerN-1
        current_folder = data  # layerN
        print(current_folder)

    if (name == 'ls'):
        # a = int(c.recv(1024).decode())
        # print(a)
        # arr = []
        # for i in range(a):
        #     d = c.recv(1024).decode()
        #     arr.append(d)
        # print(arr)

        arr = c.recv(1024).decode()  # LayerN-2
        arr = encrypt(arr, de_key)  # LayerN-1
        arr = eval(arr)  # LayerN, here converting the strig back into array.
        print(arr)

    if (name[:2] == 'cd'):
        status = c.recv(1024).decode()
        status = encrypt(status, de_key)
        print(status)

    if (name[:3] == 'upd'):
        if (name[4:] in os.listdir()):
            file = open(name[4:], "r")
            data = file.read()
            data = encrypt(data, en_key)
            c.send(bytes(data, 'utf-8'))
            file.close()
            status = c.recv(1024).decode()
            status = encrypt(status, de_key)
            print(status)
        else:
            data = "NOK"
            data = encrypt(data, en_key)
            c.send(bytes(data, 'utf-8'))
            data = encrypt(data, de_key)
            print(data)

    if (name[:3] == 'dwd'):
        data = c.recv(1024).decode()
        data = encrypt(data, de_key)
        if (data != "NOK"):
            file_name = name[4:]
            file = open(file_name, "w")
            file.write(data)
            file.close()
            print("OK")
        else:
            print("NOK")

    print("")
