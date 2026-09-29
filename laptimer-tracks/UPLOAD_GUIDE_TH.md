
# คู่มือละเอียด - อัพโหลดฐานข้อมูลสนาม 2000+ แห่งขึ้น GitHub + ใช้กับ ESP32 LapTimer V2.2

## สิ่งที่คุณได้จากผมแล้ว (ในโฟลเดอร์ tracks/)
- tracks_world_2000.json (2000 สนาม - ชื่อครบ, รอเติมพิกัด)
- tracks_world_200.json (86 สนาม มีพิกัด S/F แม่นแล้ว)
- tracks_asia.json / tracks_asia_full.json / tracks_europe.json ฯลฯ
- buriram.json, bira.json, sepang.json ... (ไฟล์รายสนามพร้อม points วงรีจำลอง)

---

## ขั้นตอนที่ 1: สร้าง GitHub Repo

1. เข้า https://github.com/new
2. ตั้งชื่อ repo: `laptimer-tracks`
3. เลือก Public
4. ติ๊ก Add a README file
5. กด Create repository

## ขั้นตอนที่ 2: อัพโหลดไฟล์ (วิธีง่าย - ผ่านเว็บ)

1. เข้า repo ที่สร้าง -> กด Add file -> Upload files
2. ลากไฟล์ทั้งหมดจากโฟลเดอร์ tracks/ ที่โหลดจากผมไปวาง
   - tracks_world_2000.json
   - tracks_world_200.json
   - tracks_asia.json
   - tracks_asia_full.json
   - tracks_europe.json
   - tracks_north_america.json
   - tracks_south_america.json
   - tracks_oceania.json
   - tracks_africa.json
   - tracks_index.json
   - โฟลเดอร์ tracks/ ที่มีไฟล์รายสนาม 61 ไฟล์ (buriram.json ฯลฯ) -> ต้องสร้างโฟลเดอร์ tracks/ ใน GitHub ก่อน แล้วอัพเข้าไป
3. กด Commit changes

**วิธี Pro - ผ่าน git (ถ้ามี git ติดตั้ง):**
```bash
git clone https://github.com/YOURUSER/laptimer-tracks.git
cd laptimer-tracks
# copy ไฟล์ทั้งหมดจากผมมาวางในโฟลเดอร์นี้
git add .
git commit -m "Add 2000 tracks worldwide from racingcircuits.info + TrackAddict + Wikipedia"
git push
```

## ขั้นตอนที่ 3: เอาลิงก์ Raw สำหรับ ESP32

หลังอัพแล้ว ลิงก์จะเป็นแบบนี้:
```
https://raw.githubusercontent.com/YOURUSER/laptimer-tracks/main/tracks_asia.json
https://raw.githubusercontent.com/YOURUSER/laptimer-tracks/main/tracks_world_2000.json
https://raw.githubusercontent.com/YOURUSER/laptimer-tracks/main/tracks/buriram.json
```

เอาไปใส่ในโค้ด ESP32 ตรงนี้:
```cpp
const char* TRACK_INDEX_URL = "https://raw.githubusercontent.com/YOURUSER/laptimer-tracks/main/tracks_asia.json";
const char* TRACK_BASE_URL = "https://raw.githubusercontent.com/YOURUSER/laptimer-tracks/main/tracks/";
```

## ขั้นตอนที่ 4: เติมพิกัดและแผนที่จริงจาก OpenStreetMap (รันบนคอมคุณ)

ผมทำสคริปต์ `fetch_osm_tracks.py` ให้แล้ว (โหลดด้านล่าง)

วิธีรัน:
1. ติดตั้ง Python + pip install requests
2. รัน: `python fetch_osm_tracks.py --input tracks_world_2000.json --output tracks_world_2000_full.json`
3. สคริปต์จะไปถาม Overpass API และ Nominatim เพื่อเติม sfLat/sfLon และ points จริง
4. ได้ไฟล์ใหม่แล้วอัพขึ้น GitHub ทับไฟล์เดิม

## ขั้นตอนที่ 5: ดึงแผนที่จาก racingcircuits.info

racingcircuits.info ไม่มี API แต่มี SVG สวยๆ

วิธี:
1. เปิด https://www.racingcircuits.info/asia/thailand/buriram-united-international-circuit.html
2. คลิกขวา Save ไฟล์ SVG ของแทร็ก
3. รันสคริปต์ `svg_to_gps.py` ที่ผมให้ -> แปลง SVG path เป็น lat/lon โดยใช้จุด S/F เป็นจุดอ้างอิง
4. เอา points ที่ได้ไปใส่ใน buriram.json

## ขั้นตอนที่ 6: ใช้ใน ESP32 V2.2

1. ในหน้า WIFI ตั้ง SSID/PASS ให้เครื่องจำ (prefs.putString)
2. หน้า TRACK กด MENU -> เครื่องจะเรียก connectInternet() -> downloadToSD(TRACK_INDEX_URL)
3. เลือกสนามด้วย UP/DOWN -> downloadTrackById("buriram")
4. loadTrackFromSD("buriram") -> หน้า MAPS จะโชว์เส้นแทร็กจริง + เส้นสตาร์ทตารางขาวดำ + ลูกศรทิศทางทันที

## การอัพเดทสนามใหม่

แค่แก้ไฟล์ JSON บน GitHub แล้ว ESP32 จะโหลดใหม่เองครั้งหน้า ไม่ต้องแฟลชเฟิร์มแวร์ใหม่

---
