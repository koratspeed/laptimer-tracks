
// ใส่ใน LapTimer V2.2 ของคุณ - วางหลัง connectInternet()

#include <ArduinoJson.h>
#include <WiFiClientSecure.h>

const char* TRACK_INDEX_URL = "https://raw.githubusercontent.com/YOURUSER/laptimer-tracks/main/tracks_index.json";
const char* TRACK_BASE_URL = "https://raw.githubusercontent.com/YOURUSER/laptimer-tracks/main/tracks/";

bool downloadToSD(String url, String sdPath) {
  WiFiClientSecure client; client.setInsecure();
  HTTPClient http;
  if(!http.begin(client, url)) return false;
  int code = http.GET();
  if(code!=200){ http.end(); return false; }
  if(SD.exists(sdPath)) SD.remove(sdPath);
  File f = SD.open(sdPath, FILE_WRITE);
  if(!f){ http.end(); return false; }
  WiFiClient* stream = http.getStreamPtr();
  uint8_t buf[512];
  while(http.connected()){
    size_t avail = stream->available();
    if(avail){
      size_t toRead = min(avail, sizeof(buf));
      int c = stream->readBytes(buf, toRead);
      f.write(buf, c);
    } else delay(1);
    if(avail==0 && !http.connected()) break;
  }
  f.close(); http.end();
  return true;
}

bool downloadTrackList(){
  if(!wifiStaConnected && !connectInternet()) return false;
  SD.mkdir("/tracks");
  return downloadToSD(TRACK_INDEX_URL, "/tracks/index.json");
}

bool downloadTrackById(String id){
  String url = String(TRACK_BASE_URL) + id + ".json";
  String path = "/tracks/" + id + ".json";
  return downloadToSD(url, path);
}

bool loadTrackFromSD(String id){
  String path = "/tracks/" + id + ".json";
  if(!SD.exists(path)) return false;
  File f = SD.open(path);
  DynamicJsonDocument doc(16384);
  DeserializationError err = deserializeJson(doc, f);
  f.close();
  if(err) return false;
  track.valid = true;
  strncpy(track.name, doc["name"] | "NO NAME", sizeof(track.name)-1);
  track.sfLat = doc["sfLat"] | 0.0f;
  track.sfLon = doc["sfLon"] | 0.0f;
  mapPointCount = 0;
  JsonArray pts = doc["points"].as<JsonArray>();
  for(JsonObject p : pts){
    if(mapPointCount >= MAX_MAP_POINTS) break;
    mapPoints[mapPointCount].lat = p["lat"];
    mapPoints[mapPointCount].lon = p["lon"];
    mapPointCount++;
  }
  if(mapPointCount>0){
    mapLoaded = true;
    mapMinLat = mapMaxLat = mapPoints[0].lat;
    mapMinLon = mapMaxLon = mapPoints[0].lon;
    for(int i=1;i<mapPointCount;i++){
      mapMinLat = min(mapMinLat, mapPoints[i].lat);
      mapMaxLat = max(mapMaxLat, mapPoints[i].lat);
      mapMinLon = min(mapMinLon, mapPoints[i].lon);
      mapMaxLon = max(mapMaxLon, mapPoints[i].lon);
    }
  }
  return true;
}
