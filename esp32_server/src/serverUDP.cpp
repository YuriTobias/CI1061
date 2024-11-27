#include <Arduino.h>
#include <WiFi.h>
#include <WiFiUdp.h>

const char* ssid = "NET_2GDDEAFE";
const char* password = "B3DDEAFE";

WiFiUDP udp;
unsigned int localPort = 8080;  // Local port to listen on

int packetCount = 0;

void setup() {
    Serial.begin(115200);
    WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED) {
        delay(1000);
        Serial.println("Conectando ao Wi-Fi...");
    }

    // Print IP address when connected
    Serial.println("Wi-Fi conectado!");
    Serial.print("Endereço IP: ");
    Serial.println(WiFi.localIP()); // Print the IP address

    udp.begin(localPort);  // Start the UDP listener on the specified port
}

void loop() {
    char incomingPacket[1500];  // Buffer for incoming data
    int packetSize = udp.parsePacket();  // Check if there's a packet available
    if (packetSize) {
        packetCount++;
        // Read the packet
        int len = udp.read(incomingPacket, 1500);
        if (len > 0) {
            incomingPacket[len] = 0;  // Null-terminate the string
        }

        Serial.printf("%lu: Recebido %d bytes de %s:%d, pacote nº %d, identificador %d\n", millis(), len, udp.remoteIP().toString().c_str(), udp.remotePort(), packetCount, udp.remotePort());
        // Send a response back to the sender
        //String response = "Recebido " + String(len) + " bytes. Pacotes recebidos: " + String(++packetCount);
        //udp.beginPacket(udp.remoteIP(), udp.remotePort());  // Send to the sender's IP and port
        //udp.write((const uint8_t*)response.c_str(), response.length());
        //udp.endPacket();
    }
}
