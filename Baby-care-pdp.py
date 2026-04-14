import hashlib
import os
import json
import random
import time
from curl_cffi import requests
import pydash
from db_config import baby_care, baby_care_pdp


pdp_folder = r"D:\blinkit\Atta-Rice-Dal_spiderpage"

session = requests.Session(
    impersonate="chrome120"
)

DEVICES = [
    {"device_id": "d1a9c23f92a1", "lat": "17.3850", "lon": "78.4867"},
    {"device_id": "f81bbca99212", "lat": "28.6139", "lon": "77.2090"},
    {"device_id": "cc2e9918aa92", "lat": "12.9716", "lon": "77.5946"},
    {"device_id": "99ac2211b9aa", "lat": "19.0760", "lon": "72.8777"},
]

import requests

cookies = {
    'gr_1_deviceId': 'e7ae8231-3b4a-4aba-8210-653c8856d771',
    '_gcl_au': '1.1.1193079599.1767937879',
    '_fbp': 'fb.1.1767937884119.190796487447140728',
    'gr_1_lat': '17.3924982',
    'gr_1_lon': '78.46796379999999',
    'gr_1_locality': 'Hyderabad',
    'gr_1_landmark': 'undefined',
    '_gid': 'GA1.2.1438408380.1768193920',
    '_cfuvid': 'nn0cULB8lPTku9qMcDaRgccbLj1qurvTI5DSeb0uJcc-1768199094611-0.0.1.1-604800000',
    '__cf_bm': 'zBs4bsvC8szxp2P9tRCqFGPCBLrTtofzLc4aMbM_o4E-1768202067-1.0.1.1-TrI7vAEAN4_OaZshxdzjHlybJxb1GcDLQKXAqoXRTsOL.NuL55syhCKF7xQIRBx5GkTOxhb24d1.IGpwfEtas0oL5E1QBNlcC_pU4iNDcrI',
    '__cfruid': '5d7eb8ed8fd1e3a16de60f9b25c0d788575331f4-1768202067',
    '_ga_JSMJG966C7': 'GS2.1.s1768202064$o9$g1$t1768202675$j60$l0$h0',
    '_ga': 'GA1.2.2074212143.1767937880',
    '_gat_UA-85989319-1': '1',
    '_ga_DDJ0134H6Z': 'GS2.2.s1768202064$o9$g1$t1768202675$j60$l0$h0',
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


products = baby_care.find({"status": "pending"})

for product in products:
    product_url = product.get('product_url')
    if not product_url:
        continue

    hash_utf8 = product_url.encode('utf8')
    r_url_hash_id = str(int(hashlib.md5(hash_utf8).hexdigest(), 16) % (10 ** 10))
    file_path = f'PL_folder_html_pages_{r_url_hash_id}.html'
    path = os.path.join(pdp_folder, file_path)

    if os.path.isfile(path):
        print("Loading from disk:", path)
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
    else:
        print("Downloading:", product_url)

        pid = product_url.split("/prid/")[-1]
        api_url = f"https://blinkit.com/v1/layout/product/{pid}"
        print("Downloading:", api_url)

        for attempt in range(5):
            response = session.post(api_url, headers=get_headers(), cookies=cookies)

            if response.status_code == 200:
                break

            if response.status_code == 429:
                wait = random.uniform(15, 35)
                print(f"429 hit — sleeping {wait:.1f}s")
                time.sleep(wait)
            else:
                break

        if response.status_code != 200:
            print("Failed to download:", response.status_code)
            continue

        content = response.text
        with open(path, 'w', encoding='utf8') as f:
            f.write(content)

        jsn= json.loads(content)

        name = product.get('name')
        pid = product.get('pid')
        section = product.get('section')
        Baby_Weight = pydash.get(jsn, 'response.snippet_list_updater_data.attributes_to_add_for_expanding_vpd.payload.snippets_to_add[4].data.subtitle.text')
        Absorption_Hours = pydash.get(jsn,'response.snippets[0].data.overlay_data.expandable_data.expanded_state.vertical_item_list[4].subtitle.text')
        Material = pydash.get('response.snippet_list_updater_data.attributes_to_add_for_expanding_vpd.payload.snippets_to_add[5].data.subtitle.text')
        Skin_type = pydash
        Size = pydash.get('response.snippet_list_updater_data.attributes_to_add_for_expanding_vpd.payload.snippets_to_add[6].data.subtitle.text')
        Preferences = pydash.get('response.snippet_list_updater_data.attributes_to_add_for_expanding_vpd.payload.snippets_to_add[7].data.subtitle.text')
        Franchise = pydash.get('response.snippet_list_updater_data.attributes_to_add_for_expanding_vpd.payload.snippets_to_add[8].data.subtitle.text')
        Unit = pydash.get('response.page_level_components.sticky.footer_snippet_models[1].snippet.data.rfc_actions_v2.default[0].remove_from_cart.cart_item.unit')
        Key_features = pydash.get('response.snippet_list_updater_data.expandinfo0.payload.snippets_to_add[2].data.subtitle.text')
        Description = pydash.get('response.tracking.le_meta.custom_data.seo.attributes[0].value')
        Pac_size = pydash.get('response.snippet_list_updater_data.expandinfo0.payload.snippets_to_add[4].data.subtitle.text')
        Shelf_life = pydash.get('response.snippet_list_updater_data.expandinfo0.payload.snippets_to_add[5].data.subtitle.text')
        Country_of_origin = pydash.get('response.snippet_list_updater_data.expandinfo0.payload.snippets_to_add[6].data.subtitle.text')
        Return_policy = pydash.get('response.snippet_list_updater_data.expandinfo0.payload.snippets_to_add[8].data.subtitle.text')
        Manufacturer_name_add = pydash.get('response.snippet_list_updater_data.expandinfo0.payload.snippets_to_add[9].data.subtitle.text')
        Marketers_name = pydash.get('response.snippet_list_updater_data.expandinfo0.payload.snippets_to_add[10].data.subtitle.text')
        Disclaimer = pydash.get('response.snippet_list_updater_data.expandinfo0.payload.snippets_to_add[11].data.subtitle.text')
        seller = pydash.get('response.snippet_list_updater_data.expandinfo0.payload.snippets_to_add[12].data.subtitle.text')

        data = {
            "name": name,
            'pid': pid,
            'section': section,

        }

        try:
            baby_care_pdp.insert_one(data)

        except Exception as e:
            print("DB Error:", e)



        try:
            baby_care.update_one(
                {'_id': product['_id']},
                {'$set': {'status': 'Done'}}
            )

        except Exception as e:
            print('failed to update:', e)

        print("Finished", name)
