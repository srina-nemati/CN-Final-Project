import socket


def send_calculation_request(operator, op1, op2=None):
    request = f"${operator}${op1}${op2}$"
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.connect(('localhost', 3000))
    server_socket.send(request.encode())

    response = server_socket.recv(1024).decode()
    response_parts = response.split('$')[1:-1]

    if len(response_parts) >= 3:
        calculation = response_parts[0]
        time = response_parts[1]
        result = response_parts[-1]

        if op2 is not None:
            print("\nCalculation:", op1, calculation, op2)
        else:
            print("\nCalculation:", calculation, op1)

        print("time: ", time)
        print("Result:", result)
    else:
        print("Invalid response from the server.")

    server_socket.close()


# Example usage:
send_calculation_request("Add", 10, 2)
send_calculation_request("Subtract", 10, 2)
send_calculation_request("Multiply", 10, 2)
send_calculation_request("Divide", 10, 2)
send_calculation_request("Sin", 30)
send_calculation_request("Cos", 30)
send_calculation_request("Tan", 30)
send_calculation_request("Cot", 30)
