import urllib.request
import json
import csv

# === Step 1. 下載 HTML ===
url_ch = "https://resources-wehelp-taiwan-b986132eca78c0b5eeb736fc03240c2ff8b7116.gitlab.io/hotels-ch"
url_en = "https://resources-wehelp-taiwan-b986132eca78c0b5eeb736fc03240c2ff8b7116.gitlab.io/hotels-en"

def fetch_json(url):
    with urllib.request.urlopen(url) as response:
        data = json.load(response)
    return data["list"]

# 抓取json
hotels_ch = fetch_json(url_ch)
hotels_en = fetch_json(url_en)


# === Step 3. 合併中英文資料 ===
en_map = {h["_id"]: h for h in hotels_en}
merged = []

for h in hotels_ch:
    en = en_map.get(h["_id"], {})
    merged.append({
        "id": h["_id"],
        "name_ch": h["旅宿名稱"],
        "name_en": en.get("hotel name", ""),
        "district": h["地址"][3:6], # 抓取 地址的第3~6位元
        "address_ch": h["地址"],
        "address_en": en.get("address", ""),
        "phone":h["電話或手機號碼"],
        "rooms_en": int(en.get("total number of rooms", 0)),
        "rooms_ch":int(h["房間數"])
    })

# === Step 4. 輸出 hotels.csv ===
with open("hotels.csv", "w", encoding="utf-8", newline="") as f:
    writer = csv.writer(f)
    for h in merged:
        writer.writerow([
             h["name_ch"], h["name_en"],
             h["address_ch"], h["address_en"], h["phone"], h["rooms_ch"]
        ])

# === Step 5. 依行政區分組並輸出 districts.csv ===
district_summary = {}
for h in merged:
    dist = h["district"]
    if dist not in district_summary:
        district_summary[dist] = {"count": 0, "rooms": 0}
    district_summary[dist]["count"] += 1
    district_summary[dist]["rooms"] += h["rooms_en"] + h["rooms_ch"]

with open("districts.csv", "w", encoding="utf-8", newline="") as f:
    writer = csv.writer(f)
    for dist, data in district_summary.items():
        writer.writerow([dist, data["count"], data["rooms"]])


