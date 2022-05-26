import socket
from random import randint

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("127.0.0.1", 2103))
s.listen(2)
(connection_client1, address_client1) = s.accept()
print("Connected address_client1:", address_client1)


def single_player():
    number_to_guess = randint(0, 50)
    print(number_to_guess)
    steps = 0
    result = 10
    while result:
        number_client = connection_client1.recv(100).decode("UTF-8")
        result = compare_numbers(number_to_guess, int(number_client))
        steps = steps + 1
    return steps


def compare_numbers(number_server, number_client):
    if number_server == number_client:
        connection_client1.send(b"numarul este corect")
        return 0
    elif number_client < number_server:
        connection_client1.send(b"numarul este mai mare")
        return 1
    connection_client1.send(b"numarul este mai mic")
    return 2


def multi_player(number_client1):
    steps = 0
    result = 10
    while result:
        number_client2 = connection_client2.recv(100).decode("UTF-8")
        result = compare_numbers_clients(int(number_client1), int(number_client2))
        steps = steps + 1
    return steps


def compare_numbers_clients(number_client1, number_client2):
    if number_client1 == number_client2:
        connection_client1.send(b"numarul a fost ghicit")
        connection_client2.send(b"numarul este corect")
        return 0
    elif number_client2 < number_client1:
        connection_client1.send(b"numarul meu este mai mare")
        connection_client2.send(b"numarul este mai mare")
        return 1
    connection_client1.send(b"numarul meu este mai mic")
    connection_client2.send(b"numarul este mai mic")
    return 2


max_score = 50

game_mode = connection_client1.recv(100).decode("UTF-8")

if game_mode.lower() == "nu":
    while True:
        score = single_player()
        if score < max_score:
            max_score = score
        connection_client1.send(str.encode(str(score)))
        response = connection_client1.recv(100).decode("UTF-8")
        if response.lower() == "nu":
            connection_client1.send(str.encode(str(max_score)))
            break
else:
    (connection_client2, address_client2) = s.accept()
    print("Connected connection_client2:", address_client2)
    connection_client1.send(b"ok")
    while True:
        score = multi_player(int(game_mode))
        if score < max_score:
            max_score = score
        connection_client1.send(str.encode(str(score)))
        connection_client2.send(str.encode(str(score)))
        response_client2 = connection_client2.recv(100).decode("UTF-8")
        connection_client1.send(str.encode(response_client2))
        if response_client2.lower() == "nu":
            connection_client1.send(str.encode(str(max_score)))
            connection_client2.send(str.encode(str(max_score)))
            connection_client2.close()
            break
        else:
            game_mode = connection_client1.recv(100).decode("UTF-8")

connection_client1.close()
print("Server closed")
