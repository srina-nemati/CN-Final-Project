import socket
import sys
import os

HOST = "localhost"
PORT = 3000
BUFFER_SIZE = 1024


def send_file_data(file_path, client_socket, addr):
    try:
        with open(file_path, 'rb') as file:
            data = file.read()  # Read the entire file data

            for part_number in range(0, len(data), BUFFER_SIZE - 4):
                offset = str(part_number).zfill(4).encode()  # Convert the part number to a 4-byte offset
                chunk = data[part_number: part_number + (BUFFER_SIZE - 4)]  # Extract a chunk of data

                client_socket.sendto(offset + chunk, addr)  # Send the data with offset to the client

        print('DONE: Sending File data')

    except:
        print('ERROR: function send_file_data')


def server_mode(directory):
    # Create a socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:
        # Bind the socket to a specific address and port
        server_socket.bind((HOST, PORT))

        print('Server Started...')

        while True:
            # Receive a message and client address
            file_name, addr = server_socket.recvfrom(BUFFER_SIZE)
            file_path = os.path.join(directory, file_name.decode())

            if not os.path.isfile(file_path):
                print('ERROR: Not Existing File')
                return

            send_file_data(file_path, server_socket, addr)
            break

    except:
        print('Error occurred while starting the server.')
    finally:
        # Close the server socket
        server_socket.close()


def receive_file_data(client_socket, offset):
    received_packets = {}  # Store the received packets

    for part_number in range(offset + 1):
        chunk, _ = client_socket.recvfrom(BUFFER_SIZE)

        if not chunk:
            break

        decoded_data = chunk.decode()
        part_number_str = decoded_data[:4]  # Extract the part number from the received data
        part_data = decoded_data[4:]  # Extract the actual data from the received data
        received_packets[int(part_number_str)] = part_data.encode()  # Store the received part data

        print("\nPart Data: ", part_data)
        print("\nPart No.: ", part_number_str, "\n")

    return received_packets, offset


def client_mode(file_name, saving_path):
    offset = 0

    # Create a socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:
        client_socket.sendto(file_name.encode(), (HOST, PORT))

        received_packets, offset = receive_file_data(client_socket, offset)

        # Save the received file data
        with open(saving_path, 'wb') as file:
            for i in range(0, offset + 1):
                if i not in received_packets:
                    raise Exception("ERROR: Part not found")

                file.write(received_packets[i])

        print('DONE: Receiving & Saving File data')
    except:
        print('ERROR: function client_mode.')
    finally:
        # Close the client socket
        client_socket.close()


def create_dir(directory):
    try:
        os.makedirs(directory)
    except OSError:
        print(f'ERROR: creating directory: {directory}')
        return
    else:
        print(f'DONE: Creating Directory: {directory}')


def main():
    if len(sys.argv) < 3:
        print_usage()
        return

    if sys.argv[1] == '-server':
        directory = sys.argv[2]

        if len(sys.argv) < 3:
            print('ERROR: Directory not specified.')
            return

        if not os.path.isdir(directory):
            create_dir(directory)

        server_mode(directory)

    elif sys.argv[1] == '-receive':
        if len(sys.argv) < 3:
            print('ERROR: Filename not specified.')
            return

        # File path to save the received file
        saving_path = r'E:\SBU\Term8\Shabakeh\HWs\pythonProject\recievedFile.txt'
        client_mode(sys.argv[2], saving_path)

    else:
        print('ERROR: Invalid mode.')


def print_usage():
    print('Usage: python p2pUDP.py <mode> <additional parameters>')
    print('Modes:')
    print('-server <directory>: Run in server mode, specifying the directory where files are located.')
    print('-receive <filename>: Run in client mode, specifying the filename to receive from the server.')


if __name__ == '__main__':
    main()
