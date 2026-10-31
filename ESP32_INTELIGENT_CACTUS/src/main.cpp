#include <Arduino.h>
#include <esp_system.h>
#include <WiFi.h>
#include <ArduinoJson.h>

const char* WIFI_SSID = "PCDEDIEGO 7252";
const char* WIFI_PASSWORD = "5245R@3d";
const char* PC_IP = "192.168.137.1"; // IPv4 del ordenador
const int PUERTO = 5000;

WiFiClient cliente;

void initWifi() {
    WiFi.mode(WIFI_STA);
    WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
    Serial.print("Conectando al Wi-Fi del PC");
    while (WiFi.status() != WL_CONNECTED) {
        Serial.print(".");
        delay(500);
    }
    Serial.println("\nWi-Fi conectado.");
    Serial.print("IP del ESP32: ");
    Serial.println(WiFi.localIP());
}

bool conectarPC() {
    if (cliente.connected()) {
        return true;
    }
    cliente.stop();
    Serial.println("Conectando al receptor del PC...");
    if (!cliente.connect(PC_IP, PUERTO)) {
        Serial.println("No se pudo conectar. Reintentando...");
        return false;
    }
    Serial.println("Conectado al PC.");
    return true;
}

JsonDocument generarMedida() {
    // DATOS SIMULADOS: cambian un poco en cada envio.
    // random(a, b) genera un entero desde a hasta b - 1.
    // Dividir por 10.0 permite generar medidas con un decimal.
    JsonDocument datos;
    datos["ta"] = random(238, 249) / 10.0;  // 23.8 a 24.8 grados C
    datos["ts"] = random(213, 224) / 10.0;  // 21.3 a 22.3 grados C
    datos["ha"] = random(595, 616) / 10.0;  // 59.5 a 61.5 %
    datos["hs"] = random(342, 363) / 10.0;  // 34.2 a 36.2 %
    datos["luz"] = random(120000, 126001);  // Luz simulada en lux
    return datos;
}

void enviarMedida(const JsonDocument& datos) {
    String mensaje;
    serializeJson(datos, mensaje);
    cliente.println(mensaje); // El salto de linea separa los JSON en TCP.
    Serial.print("Enviado: ");
    Serial.println(mensaje);
}

void setup() {
    Serial.begin(115200);
    randomSeed(esp_random());
    initWifi();
}

void loop() {
    if (WiFi.status() != WL_CONNECTED) {
        cliente.stop();
        initWifi();
    }
    if (conectarPC()) {
        JsonDocument datos = generarMedida();
        enviarMedida(datos);
    }
    delay(2000); // Una medida cada dos segundos
}
