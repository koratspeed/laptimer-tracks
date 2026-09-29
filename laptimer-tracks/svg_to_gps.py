
"""
svg_to_gps.py
แปลง SVG path จาก racingcircuits.info เป็น lat/lon สำหรับ ESP32

1. เปิดหน้า racingcircuits.info -> Save SVG
2. เปิด SVG หา <path d="M x y ...">
3. รัน: python svg_to_gps.py --svg buriram.svg --lat 14.9628444 --lon 103.0849972 --output buriram_points.json

จะได้ points ที่เอาไปใส่ใน buriram.json ได้เลย
"""
import argparse, json, re, math

def parse_svg_path(d):
    # ดึงตัวเลขจาก path
    nums = list(map(float, re.findall(r"[-+]?\d*\.?\d+", d)))
    points = []
    for i in range(0, len(nums), 2):
        if i+1 < len(nums):
            points.append((nums[i], nums[i+1]))
    return points

def svg_to_gps(points, center_lat, center_lon, scale=0.00005):
    # แปลงพิกัด SVG (pixel) เป็น lat/lon โดยใช้ center เป็นจุด S/F
    # scale: 1 pixel = 0.00005 deg (~5.5m) ปรับได้
    gps = []
    if not points:
        return gps
    # หาจุดกลาง SVG
    min_x = min(p[0] for p in points)
    max_x = max(p[0] for p in points)
    min_y = min(p[1] for p in points)
    max_y = max(p[1] for p in points)
    cx = (min_x+max_x)/2
    cy = (min_y+max_y)/2

    for x,y in points:
        dlat = (cy - y) * scale  # Y กลับด้าน
        dlon = (x - cx) * scale / math.cos(math.radians(center_lat))
        gps.append({"lat": center_lat + dlat, "lon": center_lon + dlon})
    return gps

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--svg", required=True, help="path to SVG file")
    parser.add_argument("--lat", type=float, required=True, help="sfLat")
    parser.add_argument("--lon", type=float, required=True, help="sfLon")
    parser.add_argument("--output", required=True)
    parser.add_argument("--scale", type=float, default=0.00005)
    args = parser.parse_args()

    with open(args.svg, "r", encoding="utf-8") as f:
        content = f.read()
    m = re.search(r'd="([^"]+)"', content)
    if not m:
        print("ไม่เจอ path d=")
        return
    points = parse_svg_path(m.group(1))
    gps_points = svg_to_gps(points, args.lat, args.lon, args.scale)

    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(gps_points, f, indent=2)
    print(f"Saved {len(gps_points)} points to {args.output}")

if __name__=="__main__":
    main()
