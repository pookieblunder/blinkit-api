from curl_cffi import requests

import hashlib
import os
import json
from db_config import url, Beauty_Cosmetics

# =========================
# DB
# =========================


SECTION = "Beauty & Cosmetics"

# =========================
# Cache Folder
# =========================
FOLDER = r"D:\blinkit\Beauty-Cosmetics"
os.makedirs(FOLDER, exist_ok=True)

# =========================
# Blinkit headers & cookies
# =========================



cookies = {
    'gr_1_deviceId': 'e7ae8231-3b4a-4aba-8210-653c8856d771',
    'city': '',
    '_gcl_au': '1.1.1193079599.1767937879',
    '_gid': 'GA1.2.310090624.1767937881',
    '_fbp': 'fb.1.1767937884119.190796487447140728',
    'gr_1_lat': '17.3924982',
    'gr_1_lon': '78.46796379999999',
    'gr_1_locality': 'Hyderabad',
    'gr_1_landmark': 'undefined',
    '__cf_bm': 'vJsSHadj6urBr7YecdZg1WHE_SBULCeCha2mI.HsnFo-1767953570-1.0.1.1-rYcvd2UJ.lXROBVeBvQnhVfpdQy.KWn9g3CoelF0w6v0uTlLVJADeICGR7qyiYYl.msYKiFB.xpnI01i2vd6d5vX2xCwH6tnmDBxSnc3ycQ',
    '__cfruid': 'f5780caca77a2d81768475477f4f2b9e0dcfea27-1767953570',
    '_cfuvid': 'PomwvMZewU7DLjQEMKfMbQcKPQgXZqE2xpY9N.LxYSg-1767953570448-0.0.1.1-604800000',
    '_ga_DDJ0134H6Z': 'GS2.2.s1767951452$o4$g1$t1767953846$j11$l0$h0',
    '_ga_JSMJG966C7': 'GS2.1.s1767951452$o4$g1$t1767953867$j60$l0$h0',
    '_ga': 'GA1.2.2074212143.1767937880',
    '_gat_UA-85989319-1': '1',
}

headers = {
    'accept': '*/*',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'access_token': 'null',
    'app_client': 'consumer_web',
    'app_version': '1010101010',
    'auth_key': 'c761ec3633c22afad934fb17a66385c1c06c5472b4898b866b7306186d0bb477',
    # Already added when you pass json=
    # 'content-type': 'application/json',
    'device_id': '1974ea9676ec33dc',
    'lat': '17.3924982',
    'lon': '78.46796379999999',
    'origin': 'https://blinkit.com',
    'platform': 'mobile_web',
    'priority': 'u=1, i',
    'referer': 'https://blinkit.com/cn/exotic-meat/cid/4/1201',
    'rn_bundle_version': '1009003012',
    'sec-ch-ua': '"Google Chrome";v="143", "Chromium";v="143", "Not A(Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'session_uuid': '77f11147-045e-48a2-9483-8dcbb0a42c14',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36',
    'web_app_version': '1008010016',
    'x-age-consent-granted': 'true',
    # 'cookie': 'gr_1_deviceId=e7ae8231-3b4a-4aba-8210-653c8856d771; city=; _gcl_au=1.1.1193079599.1767937879; _gid=GA1.2.310090624.1767937881; _fbp=fb.1.1767937884119.190796487447140728; gr_1_lat=17.3924982; gr_1_lon=78.46796379999999; gr_1_locality=Hyderabad; gr_1_landmark=undefined; __cf_bm=vJsSHadj6urBr7YecdZg1WHE_SBULCeCha2mI.HsnFo-1767953570-1.0.1.1-rYcvd2UJ.lXROBVeBvQnhVfpdQy.KWn9g3CoelF0w6v0uTlLVJADeICGR7qyiYYl.msYKiFB.xpnI01i2vd6d5vX2xCwH6tnmDBxSnc3ycQ; __cfruid=f5780caca77a2d81768475477f4f2b9e0dcfea27-1767953570; _cfuvid=PomwvMZewU7DLjQEMKfMbQcKPQgXZqE2xpY9N.LxYSg-1767953570448-0.0.1.1-604800000; _ga_DDJ0134H6Z=GS2.2.s1767951452$o4$g1$t1767953846$j11$l0$h0; _ga_JSMJG966C7=GS2.1.s1767951452$o4$g1$t1767953867$j60$l0$h0; _ga=GA1.2.2074212143.1767937880; _gat_UA-85989319-1=1',
}

params = {
    'l0_cat': '4',
    'l1_cat': '1201',
}

json_data = {}

# response = requests.post(
#     'https://blinkit.com/v1/layout/listing_widgets',
#     params=params,
#     cookies=cookies,
#     headers=headers,
#     json=json_data,
# )



# =========================
def extract_cids(url):
    parts = url.strip("/").split("/")
    return parts[-2], parts[-1]
def get_cached(url):
    key = hashlib.md5(url.encode()).hexdigest()
    path = os.path.join(FOLDER, key + ".json")

    if os.path.exists(path):
        with open(path, "r", encoding="utf8") as f:
            return json.load(f)

    r = requests.post(
        url,
        headers=headers,
        cookies=cookies,
        json={},
        impersonate="chrome120"   # 🚨 this is critical
    )

    if r.status_code != 200:
        print("❌ API failed", r.status_code)
        return None

    with open(path, "w", encoding="utf8") as f:
        f.write(r.text)

    return r.json()


def make_slug(name):
    name = name.lower().strip()
    name = name.replace("&", "and")
    name = name.replace(",", "")
    name = name.replace(".", "")
    name = name.replace("(", "")
    name = name.replace(")", "")
    name = name.replace("%", "")
    name = name.replace("/", "-")
    name = name.replace(" ", "-")

    # remove double dashes
    while "--" in name:
        name = name.replace("--", "-")

    return name.strip("-")


# =========================
# Fetch pending category URLs
# =========================
cats = url.find({
    "section": SECTION,
    "status": "pending"
})

for cat in cats:
    cat_url = cat["url"]
    cat_name = cat["name"]

    l0, l1 = extract_cids(cat_url)

    print(f"\n🚀 Scraping: {cat_name}")

    offset = 0

    while True:
        api = (
            "https://blinkit.com/v1/layout/listing_widgets"
            f"?l0_cat={l0}&l1_cat={l1}&offset={offset}"
        )

        jsn = get_cached(api)
        if not jsn:
            break

        items = jsn["response"]["snippets"]
        if not items:
            break

        for block in items:
            p = block["data"]

            name = p["name"]["text"]
            pid = p["identity"]["id"]
            img = p["image"]["url"]
            price = p["normal_price"]["text"]

            slug = make_slug(name)
            product_url = f"https://blinkit.com/prn/{slug}/prid/{pid}"

            doc = {
                "name": name,
                "pid": pid,
                "slug": slug,
                "product_url": product_url,
                "image": img,
                "price": price,
                "category": cat_name,
                "section": SECTION,
                "status": "pending"
            }

            Beauty_Cosmetics.update_one(
                {"pid": pid},
                {"$setOnInsert": doc},
                upsert=True
            )

            print("   🧾", name)

        # pagination
        # ---------- SAFE PAGINATION ----------
        try:
            page = jsn["response"]["snippets"][0]["data"]["layout_config"]["pagination"]
            if not page.get("next_url"):
                break
            offset += 20
        except:
            # No pagination means last page
            break


    # mark category done
    url.update_one(
        {"_id": cat["_id"]},
        {"$set": {"status": "done"}}
    )

    print(f"✅ Finished {cat_name}")
