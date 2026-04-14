# import json
# import random
# import time
# from curl_cffi import requests
# import pydash
# from db_config import Atta_Rice_Dal
#
#
# session = requests.Session(impersonate="chrome120")
#
# DEVICES = [
#     {"device_id": "d1a9c23f92a1", "lat": "17.3850", "lon": "78.4867"},
#     {"device_id": "f81bbca99212", "lat": "28.6139", "lon": "77.2090"},
#     {"device_id": "cc2e9918aa92", "lat": "12.9716", "lon": "77.5946"},
#     {"device_id": "99ac2211b9aa", "lat": "19.0760", "lon": "72.8777"},
# ]
#
# cookies = {
#     'gr_1_deviceId': 'e7ae8231-3b4a-4aba-8210-653c8856d771',
#     '_gcl_au': '1.1.1193079599.1767937879',
#     '_fbp': 'fb.1.1767937884119.190796487447140728',
#     'gr_1_lat': '17.3924982',
#     'gr_1_lon': '78.46796379999999',
#     'gr_1_locality': 'Hyderabad',
#     'gr_1_landmark': 'undefined',
#     '_gid': 'GA1.2.1438408380.1768193920',
#     '__cf_bm': 'u4bDNt.OxlxXIz4kiLgdjEyt.xC8nCxcs090pwjUJME-1768199094-1.0.1.1-hjBBKLUFl17QliOUkHO5P7cKBzCHPZmXlLCRa_C3mxnQ6u6lqZXhG369uUbJAkUjTjGvZQKqZ8rowxXF_da_QrgR7qAHsbMBK3xoyKeNYjs',
#     '__cfruid': '561e08e2000533dba8a8d677c11ed0884ad834b0-1768199094',
#     '_cfuvid': 'nn0cULB8lPTku9qMcDaRgccbLj1qurvTI5DSeb0uJcc-1768199094611-0.0.1.1-604800000',
#     '_ga_JSMJG966C7': 'GS2.1.s1768197718$o8$g1$t1768199094$j59$l0$h0',
#     '_ga': 'GA1.2.2074212143.1767937880',
#     '_gat_UA-85989319-1': '1',
#     '_ga_DDJ0134H6Z': 'GS2.2.s1768197718$o8$g1$t1768199094$j60$l0$h0',
# }
#
#
#
# def get_headers():
#     d = random.choice(DEVICES)
#
#     return {
#         "accept": "application/json",
#         "content-type": "application/json",
#         "app_client": "consumer_web",
#         "app_version": "1010101011",
#
#         "device_id": d["device_id"],
#         "lat": d["lat"],
#         "lon": d["lon"],
#
#         "origin": "https://blinkit.com",
#         "referer": "https://blinkit.com/",
#
#         "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/143.0.0.0",
#         "x-age-consent-granted": "false",
#     }
#
# def fetch_search_page(keyword, offset=0):
#     url = "https://blinkit.com/v1/layout/search"
#
#     params = {
#         "offset": str(offset),
#         "limit": "24",
#         "q": keyword,
#         "search_type": "auto_suggest",
#         "search_method": "basic"
#     }
#
#     headers = get_headers()
#
#     for attempt in range(5):
#         try:
#             response = session.post(
#                 url,
#                 params=params,
#                 headers=headers,
#                 cookies=cookies
#             )
#
#             print(f"Status Code: {response.status_code}")
#
#             if response.status_code == 200:
#                 return response.json()
#
#             elif response.status_code in [403, 401]:
#                 print(" BLOCKED (403/401) → Refresh cookies/auth_key")
#                 return None
#
#             elif response.status_code == 429:
#                 wait = random.uniform(10, 25)
#                 print(f" Rate limited → sleeping {wait:.1f}s")
#                 time.sleep(wait)
#
#             else:
#                 print( "Error:", response.status_code)
#                 return None
#
#         except Exception as e:
#             print("Request error:", e)
#             time.sleep(3)
#
#     return None
#
#
# def extract_products(jsn):
#     results = []
#
#     if not jsn:
#         return results
#
#     snippets = pydash.get(jsn, "response.snippets", [])
#
#     if not snippets:
#         print("No snippets → API structure changed")
#         return results
#
#     for snip in snippets:
#
#         if snip.get("widget_type") not in ["product_card_snippet_type_2","product_card_type_unbounded_v2", "product_card_horizontal_snippet"]:
#             continue
#
#         data = snip.get("data", {})
#
#         # Product ID
#         pid = data.get("product_id") or pydash.get(data, "identity.id")
#         if not pid:
#             continue
#
#
#         name = (
#             pydash.get(data, "display_name.text")
#             or pydash.get(data, "name.text")
#         )
#
#
#         price = (pydash.get(data, "pricing_info.price.text")           # BEST
#             or pydash.get(data, "normal_price.text")              # fallback
#             or pydash.get(data, "tracking.common_attributes.price"))
#
#         mrp = (
#             pydash.get(data, "pricing_info.mrp.text")             # BEST
#             or pydash.get(data, "mrp.text")                       # fallback
#             or pydash.get(data, "tracking.common_attributes.mrp")
#         )
#
#
#         if isinstance(price, str):
#             price = price.replace("₹", "").strip()
#
#         if isinstance(mrp, str):
#             mrp = mrp.replace("₹", "").strip()
#
#         results.append({
#             "pid": str(pid),
#             "name": name,
#             "price": price,
#             "mrp": mrp,
#             "product_url": f"https://blinkit.com/prn/x/prid/{pid}",
#             "status": "done" if price else "pending"
#         })
#
#     return results
#
#
# def save_to_db(products):
#     for p in products:
#         try:
#             Atta_Rice_Dal.update_one(
#                 {"pid": p["pid"]},
#                 {"$setOnInsert": p},
#                 upsert=True
#             )
#         except Exception as e:
#             print("DB error:", e)
#
# def run():
#     keywords = ["atta", "rice", "dal"]
#
#     for keyword in keywords:
#         print(f"\n Fetching keyword: {keyword}")
#
#         jsn = fetch_search_page(keyword)
#
#         if not jsn:
#             print("No response")
#             continue
#
#         products = extract_products(jsn)
#
#         print(f"Found {len(products)} products")
#
#         if not products:
#             print("No products extracted")
#             print(json.dumps(jsn, indent=2)[:1000])
#             continue
#
#         save_to_db(products)
#
#         sleep_time = random.uniform(2, 5)
#         print(f"Sleeping {sleep_time:.1f}s\n")
#         time.sleep(sleep_time)
#
# if __name__ == "__main__":
#     run()


from flask import Flask, request, jsonify
import json
import random
import time
from curl_cffi import requests
import pydash

app = Flask(__name__)

session = requests.Session(impersonate="chrome120")

DEVICES = [
    {"device_id": "d1a9c23f92a1", "lat": "17.3850", "lon": "78.4867"},
    {"device_id": "f81bbca99212", "lat": "28.6139", "lon": "77.2090"},
    {"device_id": "cc2e9918aa92", "lat": "12.9716", "lon": "77.5946"},
    {"device_id": "99ac2211b9aa", "lat": "19.0760", "lon": "72.8777"},
]

cookies = {
    'gr_1_deviceId': 'e7ae8231-3b4a-4aba-8210-653c8856d771',
    '_gcl_au': '1.1.1193079599.1767937879',
    '_fbp': 'fb.1.1767937884119.190796487447140728',
    'gr_1_lat': '17.3924982',
    'gr_1_lon': '78.46796379999999',
    'gr_1_locality': 'Hyderabad',
    'gr_1_landmark': 'undefined',
    '_gid': 'GA1.2.1438408380.1768193920',
    '__cf_bm': 'u4bDNt.OxlxXIz4kiLgdjEyt.xC8nCxcs090pwjUJME-1768199094-1.0.1.1-hjBBKLUFl17QliOUkHO5P7cKBzCHPZmXlLCRa_C3mxnQ6u6lqZXhG369uUbJAkUjTjGvZQKqZ8rowxXF_da_QrgR7qAHsbMBK3xoyKeNYjs',
    '__cfruid': '561e08e2000533dba8a8d677c11ed0884ad834b0-1768199094',
    '_cfuvid': 'nn0cULB8lPTku9qMcDaRgccbLj1qurvTI5DSeb0uJcc-1768199094611-0.0.1.1-604800000',
    '_ga_JSMJG966C7': 'GS2.1.s1768197718$o8$g1$t1768199094$j59$l0$h0',
    '_ga': 'GA1.2.2074212143.1767937880',
    '_gat_UA-85989319-1': '1',
    '_ga_DDJ0134H6Z': 'GS2.2.s1768197718$o8$g1$t1768199094$j60$l0$h0',
}

def get_headers():
    d = random.choice(DEVICES)
    return {
            "accept": "application/json",
            "content-type": "application/json",
            "app_client": "consumer_web",
            "app_version": "1010101011",

            "device_id": d["device_id"],
            "lat": d["lat"],
            "lon": d["lon"],

            "origin": "https://blinkit.com",
            "referer": "https://blinkit.com/",

            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/143.0.0.0",
            "x-age-consent-granted": "false",
        }

def fetch_search_page(keyword, offset=0):
    url = "https://blinkit.com/v1/layout/search"

    params = {
        "offset": str(offset),
        "limit": "24",
        "q": keyword,
        "search_type": "auto_suggest",
        "search_method": "basic"
    }

    try:
        response = session.post(
            url,
            params=params,
            headers=get_headers(),
            cookies=cookies
        )

        if response.status_code == 200:
            return response.json()
        else:
            return None

    except Exception as e:
        print("Error:", e)
        return None


def extract_products(jsn):
    results = []

    snippets = pydash.get(jsn, "response.snippets", [])

    for snip in snippets:
        if snip.get("widget_type") not in [
            "product_card_snippet_type_2",
            "product_card_type_unbounded_v2",
            "product_card_horizontal_snippet"
        ]:
            continue

        data = snip.get("data", {})

        pid = data.get("product_id") or pydash.get(data, "identity.id")
        if not pid:
            continue

        name = (
            pydash.get(data, "display_name.text")
            or pydash.get(data, "name.text")
        )

        price = (
            pydash.get(data, "pricing_info.price.text")
            or pydash.get(data, "normal_price.text")
        )

        results.append({
            "pid": pid,
            "name": name,
            "price": price,
            "product_url": f"https://blinkit.com/prn/x/prid/{pid}"
        })

    return results


@app.route("/")
def home():
    return {
        "status": "ok",
        "message": "Blinkit API is running"
    }


# 🔥 API Endpoint
@app.route("/search", methods=["GET"])
def search():
    keyword = request.args.get("q")

    if not keyword:
        return jsonify({"error": "Missing 'q' parameter"}), 400

    jsn = fetch_search_page(keyword)

    if not jsn:
        return jsonify({"error": "Failed to fetch data"}), 500

    products = extract_products(jsn)

    return jsonify({
        "keyword": keyword,
        "count": len(products),
        "products": products
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)