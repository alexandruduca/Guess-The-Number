import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("127.0.0.1", 2103))


def multi_player():
    guessed = False
    while not guessed:
        number = input("Introduceti un numar: ")
        s.send(str.encode(number))
        response = s.recv(100).decode("UTF-8")
        print(response)
        if response == "numarul este corect":
            guessed = True


replay = True
while replay:
    multi_player()
    score = s.recv(100).decode("UTF-8")
    print("Scorul dumneavoastra este: " + score)
    response = input("Daca doriti sa mai jucati, scrieti 'da', altfel 'nu': ")
    while not (response.lower() == "da" or response.lower() == "nu"):
        response = input("Comanda invalida. Incercati din nou: ")
    s.send(str.encode(response))
    if response.lower() == "nu":
        max_score = s.recv(100).decode("UTF-8")
        print("Scorul maxim al acestei sesiuni este: " + max_score)
        replay = False

s.close()
