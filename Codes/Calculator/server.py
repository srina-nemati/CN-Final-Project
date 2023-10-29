import math
import socket
from timeit import default_timer as timer
import datetime


def perform_calculation(operator, op1, op2):
    if operator == "Add":
        result = op1 + op2
    elif operator == "Subtract":
        result = op1 - op2
    elif operator == "Multiply":
        result = op1 * op2
    elif operator == "Divide":
        result = op1 / op2
    elif operator == "Sin":
        result = math.sin(op1)
    elif operator == "Cos":
        result = math.cos(op1)
    elif operator == "Tan":
        result = math.tan(op1)
    elif operator == "Cot":
        result = 1 / math.tan(op1)
    else:
        result = None
    return result


def handle_client_connection(client_socket):
    request = client_socket.recv(1024).decode()
    operator, op1, op2 = request.split('$')[1:-1]
    op1 = float(op1)
    if op2 == 'None':
        op2 = None
    else:
        op2 = float(op2)

    start_timer = timer()
    result = perform_calculation(operator, op1, op2)
    close_timer = timer()
    calc_time = str(datetime.timedelta(seconds=close_timer - start_timer))
    response = f"${operator}${calc_time}${result}$"
    client_socket.send(response.encode())
    client_socket.close()


def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 3000))
    server_socket.listen(1)
    print("Server is listening on port 3000...")

    while True:
        client_socket, _ = server_socket.accept()
        handle_client_connection(client_socket)


start_server()
