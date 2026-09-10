import sys
import time
import json
import random
import ssl
import urllib.request
import urllib.parse
from datetime import datetime, timezone

GATEWAY_URL = "http://localhost:3000/api/telemetry"

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# Comprehensive coverage across ALL 8 North Eastern States (Eight Sisters)
STATIONS = [
    {
        "station_id": "NER-SIKK-01",
        "name": "Ranipool NH-10 Geotech Array",
        "lat": 27.3389, "lon": 88.6065,
        "state": "Sikkim",
        "base_tilt": 1.20
    },
    {
        "station_id": "NER-MEGH-02",
        "name": "East Khasi Hills Mawkdok Station",
        "lat": 25.5788, "lon": 91.8933,
        "state": "Meghalaya",
        "base_tilt": 0.45
    },
    {
        "station_id": "NER-ASSA-03",
        "name": "Dima Hasao Jatinga Hill Station",
        "lat": 25.1837, "lon": 93.0298,
        "state": "Assam",
        "base_tilt": 1.15
    },
    {
        "station_id": "NER-ARUN-04",
        "name": "West Kameng Tawang Alpine Pass",
        "lat": 27.5861, "lon": 91.8653,
        "state": "Arunachal Pradesh",
        "base_tilt": 0.95
    },
    {
        "station_id": "NER-MIZO-05",
        "name": "Chite Veng Escarpment Array",
        "lat": 23.7271, "lon": 92.7176,
        "state": "Mizoram",
        "base_tilt": 0.30
    },
    {
        "station_id": "NER-NAGA-06",
        "name": "Kohima South Bypass Corridor",
        "lat": 25.6751, "lon": 94.1086,
        "state": "Nagaland",
        "base_tilt": 0.85
    },
    {
        "station_id": "NER-MANI-07",
        "name": "Noney Tupul River Corridor",
        "lat": 24.8167, "lon": 93.6833,
        "state": "Manipur",
        "base_tilt": 1.30
    },
    {
        "station_id": "NER-TRIP-08",
        "name": "Jampui Hills North Ridge",
        "lat": 23.9500, "lon": 92.2667,
        "state": "Tripura",
        "base_tilt": 0.35
    }
]

def get_live_weather(lat, lon):
    query = urllib.parse.urlencode({
        "latitude": lat,
        "longitude": lon,
        "current": "temperature_2m,precipitation,rain",
        "timezone": "Asia/Kolkata"
    })
    url = f"https://api.open-meteo.com/v1/forecast?{query}"

    try:
        req = urllib.request.Request(url, headers={"User-Agent": "ner-landslide-iot/1.0"})
        with urllib.request.urlopen(req, timeout=3, context=ctx) as res:
            if res.status == 200:
                payload = json.loads(res.read().decode('utf-8'))
                cur = payload.get("current", {})
                rain = cur.get("precipitation", 0.0) or cur.get("rain", 0.0) or 0.0
                temp = cur.get("temperature_2m", 22.0)
                return float(rain), float(temp)
    except Exception:
        # Fallback to realistic monsoon baseline if offline
        return round(random.uniform(5.0, 32.0), 2), 22.5

    return 0.0, 22.0

def generate_readings():
    readings = []
    for s in STATIONS:
        rain_mm, temp_c = get_live_weather(s["lat"], s["lon"])

        moisture = min(98.0, 50.0 + (rain_mm * 1.5) + random.uniform(-2.0, 3.0))
        pore_pressure = max(5.0, (moisture * 0.4) + random.uniform(1.0, 4.0))
        tilt = s["base_tilt"] + (rain_mm * 0.04) + random.uniform(0.01, 0.12)

        readings.append({
            "station_id": s["station_id"],
            "station_name": s["name"],
            "state": s["state"],
            "latitude": s["lat"],
            "longitude": s["lon"],
            "rainfall_mm_h": round(rain_mm, 2),
            "temperature_c": round(temp_c, 1),
            "soil_moisture_percent": round(moisture, 2),
            "pore_water_pressure_kpa": round(pore_pressure, 2),
            "slope_tilt_degrees": round(tilt, 2),
            "recorded_at": datetime.now(timezone.utc).isoformat()
        })
    return readings

def push_batch(batch):
    sent = 0
    for r in batch:
        try:
            req = urllib.request.Request(
                GATEWAY_URL,
                data=json.dumps(r).encode('utf-8'),
                headers={"Content-Type": "application/json"}
            )
            with urllib.request.urlopen(req, timeout=2) as res:
                if res.status in (200, 201):
                    sent += 1
        except Exception:
            pass
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Pushed {sent}/{len(batch)} station streams across 8 NER states")

def main():
    once = "--once" in sys.argv
    print(f"[simulator] Monitoring all 8 North Eastern States (Sikkim, Assam, Meghalaya, Arunachal, Mizoram, Nagaland, Manipur, Tripura)")

    while True:
        data = generate_readings()
        for r in data:
            print(f"  {r['state']}: {r['station_name']} -> rain={r['rainfall_mm_h']}mm/h, soil={r['soil_moisture_percent']}%, tilt={r['slope_tilt_degrees']}deg")

        push_batch(data)

        if once:
            break

        time.sleep(15)

if __name__ == "__main__":
    main()
