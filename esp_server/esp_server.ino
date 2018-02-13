#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include <ESP8266WebServer.h>
#include <ESP8266mDNS.h>
#include <ESP8266HTTPClient.h>
#include <ArduinoJson.h>

MDNSResponder mdns;

// Replace with your network credentials
const char* ssid = "EUAPP16D";
const char* password = "wolfgang";
const char* server_ip = "10.0.1.59:8000";
ESP8266WebServer server(80);

String webPage = "";


void setup(void) {
  // preparing GPIOs
  pinMode(LED_BUILTIN, OUTPUT);

  delay(1000);
  Serial.begin(115200);
  WiFi.begin(ssid, password);
  Serial.println("");

  // Wait for connection
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.print("Connected to ");
  Serial.println(ssid);
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());
  Serial.print("Sending data about board to main server");

  StaticJsonBuffer<300> JSONbuffer;   //Declaring static JSON buffer
  JsonObject& JSONencoder = JSONbuffer.createObject();
  JSONencoder["ip"] = WiFi.localIP().toString();
  JSONencoder["username"] = "ocasek";
  char JSONmessageBuffer[300];
  JSONencoder.prettyPrintTo(JSONmessageBuffer, sizeof(JSONmessageBuffer));

  Serial.println(JSONmessageBuffer);

  HTTPClient http;
  http.begin("http://" + String(server_ip) + "/api/lightInfo");
  http.addHeader("Content-Type", "application/json");

  int httpCode = http.POST(JSONmessageBuffer); //Send the request
  String payload = http.getString(); //Get the response payload
  Serial.println(httpCode); //Print HTTP return code
  Serial.println(payload); //Print request response payload
  http.end();



  if (mdns.begin("esp8266", WiFi.localIP())) {
    Serial.println("MDNS responder started");
  }
  server.on("/On", []() {
    server.send(200, "text/html", "Succes");
    digitalWrite(LED_BUILTIN, LOW);
    delay(1000);
  });
  server.on("/Off", []() {
    server.send(200, "text/html", "Succes");
    digitalWrite(LED_BUILTIN, HIGH);
    delay(1000);
  });
  server.begin();
  Serial.println("HTTP server started");
}

void loop(void) {
  server.handleClient();
}
