import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("127.0.0.1", 2103))


def single_player():
    guessed = False
    while not guessed:
        number = input("Introduceti un numar: ")
        s.send(str.encode(number))
        response = s.recv(100).decode("UTF-8")
        print(response)
        if response == "numarul este corect":
            guessed = True


def multi_player():
    print("Numarul ales de mine este: " + game_mode)
    guessed = False
    while not guessed:
        response = s.recv(100).decode("UTF-8")
        print(response)
        if response == "numarul a fost ghicit":
            guessed = True


game_mode = input("Introduceti un numar in intervalul [0, 50](daca doriti sa jucati contra unui adversar) sau scrieti "
                  "'nu': ")
while not ((game_mode.isnumeric() and 0 <= int(game_mode) <= 50) or game_mode.lower() == "nu"):
    game_mode = input("Input invalid. Incercati din nou: ")

s.send(str.encode(game_mode))
print()

if game_mode.lower() == "nu":
    replay_single_player = True
    while replay_single_player:
        single_player()
        score = s.recv(100).decode("UTF-8")
        print("Scorul dumneavoastra este: " + score)
        response = input("Daca doriti sa mai jucati, scrieti 'da', altfel 'nu': ")
        while not (response.lower() == "da" or response.lower() == "nu"):
            response = input("Comanda invalida. Incercati din nou: ")
        s.send(str.encode(response))
        if response.lower() == "nu":
            max_score = s.recv(100).decode("UTF-8")
            print("Scorul maxim al acestei sesiuni este: " + max_score)
            replay_single_player = False
else:
    replay_multi_player = True
    print("Asteptam sa se conecteze adversarul!")
    flag = s.recv(100).decode("UTF-8")
    if flag.lower() == "ok":
        print("Clientul 2 s-a conectat. Jocul poate incepe!")
        while replay_multi_player:
            multi_player()
            score = s.recv(100).decode("UTF-8")
            print("Scorul acestui meci este: " + score)
            restart = s.recv(100).decode("UTF-8")
            if restart.lower() == "nu":
                max_score = s.recv(100).decode("UTF-8")
                print("Scorul maxim al acestei sesiuni este: " + max_score)
                replay_multi_player = False
            else:
                game_mode = input("Adversarul vrea sa joace o noua partida. Introduceti un nou numar: ")
                s.send(str.encode(game_mode))

s.close()
