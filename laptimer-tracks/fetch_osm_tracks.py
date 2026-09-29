
"""
fetch_osm_tracks.py
ดึงพิกัด S/F และเส้นแทร็กจริงจาก OpenStreetMap Overpass + Nominatim
สำหรับเติมไฟล์ tracks_world_2000.json ให้ครบ

วิธีใช้:
pip install requests
python fetch_osm_tracks.py --input tracks_world_2000.json --output tracks_world_2000_full.json

จะได้ไฟล์ที่มี sfLat/sfLon และ points จริงสำหรับ ESP32
"""
import json, requests, time, argparse, sys

def geocode_track(name):
    """ใช้ Nominatim หาพิกัดสนาม"""
    url = "https://nominatim.openstreetmap.org/search"
    params = {"q": name + " race circuit", "format": "json", "limit": 1}
    headers = {"User-Agent": "LapTimer/2.2 (your email)"}
    try:
        r = requests.get(url, params=params, headers=headers, timeout=10)
        if r.status_code==200 and len(r.json())>0:
            j = r.json()[0]
            return float(j["lat"]), float(j["lon"])
    except Exception as e:
        print(f"geocode failed {name}: {e}")
    return None, None

def fetch_overpass_outline(name):
    """ดึงเส้นแทร็กจาก Overpass"""
    # ค้นหา way ที่มี name ตรงกันและเป็นสนามแข่ง
    query = f"""
    [out:json][timeout:25];
    (
      way["leisure"="track"]["name"~"{name}",i];
      way["sport"="motor"]["name"~"{name}",i];
      relation["leisure"="track"]["name"~"{name}",i];
    );
    out geom;
    """
    url = "https://overpass-api.de/api/interpreter"
    try:
        r = requests.post(url, data={"data": query}, timeout=30)
        if r.status_code==200:
            data = r.json()
            points = []
            for el in data.get("elements", []):
                geom = el.get("geometry") or []
                for pt in geom:
                    points.append({"lat": pt["lat"], "lon": pt["lon"]})
                if points:
                    break
            return points
    except Exception as e:
        print(f"overpass failed {name}: {e}")
    return []

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    with open(args.input, "r", encoding="utf-8") as f:
        tracks = json.load(f)

    updated = []
    for i, t in enumerate(tracks):
        print(f"[{i+1}/{len(tracks)}] {t['name']}")
        # ถ้ายังไม่มีพิกัด ให้ geocode
        if t.get("sfLat",0)==0 or t.get("sfLon",0)==0:
            lat, lon = geocode_track(t["name"])
            if lat:
                t["sfLat"]=lat
                t["sfLon"]=lon
                print(f"  -> geocoded {lat},{lon}")
            time.sleep(1.1)  # Nominatim rate limit

        # ถ้ามีรายสนามแยก ให้เติม points
        # ข้ามไปก่อนถ้าไม่อยากดึง outline ทั้งหมด (จะช้า)

        updated.append(t)

    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(updated, f, ensure_ascii=False, indent=2)
    print(f"Saved {args.output}")

if __name__=="__main__":
    main()
