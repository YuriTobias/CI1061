import os
import socket

SEG_SIZE = 4096

def tcp_server(host, port):
    os.makedirs("received_files", exist_ok=True)  # Ensure the directory exists

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((host, port))
        server_socket.listen(1)
        print(f"TCP Server listening on {host}:{port}")

        conn, addr = server_socket.accept()
        with conn:
            print(f"Connected by {addr}")
            # Receive the padded file name
            file_name = conn.recv(SEG_SIZE).decode()
            file_path = os.path.join("received_files", file_name)
            print(f"Receiving file '{file_name}'...")

            with open(file_path, 'wb') as f:
                while True:
                    data = conn.recv(SEG_SIZE)
                    if not data:  # End of file
                        break
                    f.write(data)

            print(f"File '{file_name}' received and saved at '{file_path}'.")
            # while True:
            #     data = conn.recv(1024)
            #     if not data:
            #         break
            #     print(f"Received: {data.decode()}")

def udp_server(host, port):
    os.makedirs("received_files", exist_ok=True)  # Ensure the directory exists

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_socket:
        server_socket.bind((host, port))
        print(f"UDP Server listening on {host}:{port}")

        # Receive the padded file name
        file_name, addr = server_socket.recvfrom(SEG_SIZE)
        file_name = file_name.decode()
        file_path = os.path.join("received_files", file_name)
        print(f"Receiving file '{file_name}'...")

        print(f"Receiving file '{file_name}' from {addr}...")
        with open(file_path, 'wb') as f:
            while True:
                data, addr = server_socket.recvfrom(SEG_SIZE)
                if data == b"EOF":  # End of File marker
                    break
                f.write(data)

        print(f"File '{file_name}' received and saved at '{file_path}'.")
        
        # while True:
        #     data, addr = server_socket.recvfrom(SEG_SIZE)
        #     print(f"Received from {addr}: {data.decode()}")

def main():
    # List of server types
    server_types = ["TCP", "UDP"]

    # Ask the user to choose a server type
    print("Choose the type of server:")
    for i, server_type in enumerate(server_types, start=1):
        print(f"{i}. {server_type}")

    choice = int(input("Enter your choice (1 or 2): "))
    if choice not in [1, 2]:
        print("Invalid choice. Exiting.")
        return

    # Get host and port from the user
    host = input("Enter the host (e.g., 127.0.0.1): ").strip()
    port = int(input("Enter the port (e.g., 12345): "))

    # Run the chosen server
    if choice == 1:
        print("Starting TCP server...")
        tcp_server(host, port)
    elif choice == 2:
        print("Starting UDP server...")
        udp_server(host, port)

if __name__ == "__main__":
    main()
