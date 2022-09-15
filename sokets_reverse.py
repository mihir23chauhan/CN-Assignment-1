import socket
import os
from tkinter.tix import Tree


def transpose(text, s):
    return text[::-1]


port = 9999
en_key = 0
de_key = (-1) * en_key

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("Socket Created, Ready to connect.")

s.bind(('localhost', port))

s.listen(3)

while True:
    print("Waiting for command from clint...")

    # Connecting to the current clint at that momment address.
    c, addr = s.accept()
    """Look into Clint.py and document for architaure layer understing."""
    # follow same procesure as done in clint.py for sending the message.
    welcome_mes = 'Welcome to server'
    welcome_mes = transpose(welcome_mes, en_key)
    c.send(bytes(welcome_mes, 'utf-8'))

    """LayerN-2:- receiving command into bytes format and decoding it."""
    name = c.recv(1024).decode()

    """LayerN-1:- decryting the recieved recieved message"""
    name = transpose(name, de_key)

    print("Connected with addr:- ", addr, "Command from clint:-", name)

    if (name == 'cwd'):
        data = os.getcwd()  # layerN
        data = transpose(data, en_key)  # layerN-1
        c.send(bytes(data, 'utf-8'))  # layerN-2

    if (name == 'ls'):
        # arr = os.listdir()
        # c.send(bytes(str(len(arr)), 'utf-8'))
        # print(arr)
        # for x in arr:
        #     c.send(bytes(x, 'utf-8'))
        #     print(x)

        arr = os.listdir()
        arr = str(arr)
        arr = transpose(arr, en_key)
        c.send(bytes(arr, 'utf-8'))

    if (name[:2] == 'cd'):
        path = name[3:]

        try:
            os.chdir(path)
            current_directory = os.getcwd()
            print("Directory changed to:-", current_directory)
            status = "OK"
            status = transpose(status, en_key)
            c.send(bytes(status, 'utf-8'))
        except:
            print("Something wrong with given.")
            status = "NOK"
            status = transpose(status, en_key)
            c.send(bytes(status, 'utf-8'))

    if (name[:3] == 'upd'):
        data = c.recv(1024).decode()
        data = transpose(data, de_key)
        if (data == "NOK"):
            print("File transfer failed.")
        else:
            file_name = name[4:]
            file = open(file_name, "w")

            file.write(data)
            file.close()
            status = "OK"
            status = transpose(status, en_key)
            c.send(bytes(status, 'utf-8'))

    if (name[:3] == 'dwd'):

        # file = open(name[4:], "r")
        # data = file.read()
        # print(data)
        # print("2938u239u2839")
        # data = encrypt(data, 2)
        # print(data)
        # c.send(bytes(data, 'utf-8'))
        # file.close()
        if (name[4:] in os.listdir()):
            file = open(name[4:], "r")
            data = file.read()
            data = transpose(data, en_key)
            c.send(bytes(data, 'utf-8'))
            file.close()
        else:
            data = "NOK"
            data = transpose(data, en_key)
            c.send(bytes(data, 'utf-8'))

    c.close()
