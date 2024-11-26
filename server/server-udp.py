import socket
import time

ESP32_IP = "192.168.0.47"
PORT = 8080

def udp_test(data_size, repetitions):
    data = "A" * data_size
    total_time = 0
    print(f"Enviando pacotes de {data_size} bytes para {ESP32_IP}:{PORT}")

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client:
        print("Conectado ao servidor")
        for _ in range(repetitions):
            print(f"Enviando pacote {_ + 1} de {repetitions}")
            start_time = time.time()

            response = client.sendto(data.encode(), (ESP32_IP, PORT))
            if response:
                print("Pacote enviado com sucesso!")
            # Send the data as UDP (no need to connect)

            # Receive response (UDP is connectionless, so we just receive from the same address)
            response, _ = client.recvfrom(1024)
            print(f"Resposta: {response.decode().strip()}")
            total_time += (time.time() - start_time)
            print(f"Resposta: {response.decode().strip()}")

    avg_time = total_time / repetitions
    print(f"Tamanho do Pacote: {data_size} bytes | RTT Médio: {avg_time:.6f} segundos")

# Testa pacotes de diferentes tamanhos
for size in [256, 512]:
    udp_test(size, 5)
