#include <Arduino.h>
#include <WiFi.h>
#include <ArduinoJson.h>

const char* WIFI_SSID = "PCDEDIEGO 7252";
const char* WIFI_PASSWORD = "5245R@3d";
const char* PC_IP = "192.168.137.1"; // IPv4 del ordenador
const int PUERTO = 5000;

WiFiClient cliente;

void setup() {
    Serial.begin(115200);
    WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
    Serial.println("Conectando al Wi-Fi...");
    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
    }
    Serial.println("Wi-Fi conectado");
}

void loop() {
    if (!cliente.connected()) {
        cliente.stop();
        Serial.println("Conectando al PC...");
        if (!cliente.connect(PC_IP, PUERTO)) {
            delay(1000);
            return;
        }
    }

    // Ejemplo con tres sensores analogicos en GPIO 32, 33 y 34.
    // Son lecturas sin convertir a unidades. Cambia estas tres lineas
    // por las lecturas de tus sensores cuando sepamos cuales son.
    JsonDocument datos;
    datos["sensor1"] = analogRead(32);
    datos["sensor2"] = analogRead(33);
    datos["sensor3"] = analogRead(34);

    String mensaje;
    serializeJson(datos, mensaje);
    cliente.println(mensaje); // Un JSON por linea
    Serial.println(mensaje);
    delay(1000);
}
