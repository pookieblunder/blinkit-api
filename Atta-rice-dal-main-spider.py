import hashlib
import os
import json
import random
import time
from curl_cffi import requests
import pydash
from db_config import Atta_Rice_Dal, Atta_Rice_Dal_pdp


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


products = Atta_Rice_Dal.find({"status": "pending"})

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
        Price_of_1kg = pydash.get(jsn, 'response.snippets[4].data.horizontal_item_list[0].data.subtitle.text')
        Price_of_500g = pydash.get(jsn,'response.snippets[4].data.horizontal_item_list[1].data.subtitle.text')
        Discount_on_1kg = pydash.get(jsn,'response.page_level_components.sticky.footer_snippet_models[1].snippet.data.offer_tag.title.text')
        Discount_on_500g = pydash.get(jsn,'response.page_level_components.sticky.footer_snippet_models[1].snippet.data.offer_tag.title.text')
        key_features = pydash.get(jsn, 'response.tracking.le_meta.custom_data.seo.attributes[1].value')
        Protein_Per_100_g = pydash.get(jsn, 'response.tracking.le_meta.custom_data.seo.attributes[1].value')
        Total_Carbohydrates_Per_100_g = pydash.get(jsn, 'response.snippet_list_updater_data.expandnutritional_information0.payload.snippets_to_add[2].data.subtitle.text')
        Total_Sugar_Per_100_g = pydash.get(jsn, 'response.snippet_list_updater_data.expandnutritional_information0.payload.snippets_to_add[2].data.subtitle.text')
        Added_Sugars_Per_100_g = pydash.get(jsn,'response.snippet_list_updater_data.expandnutritional_information0.payload.snippets_to_add[4].data.subtitle.text')
        Total_fat_per_g = pydash.get(jsn, 'response.snippet_list_updater_data.expandnutritional_information0.payload.snippets_to_add[5].data.subtitle.text')
        Saturated_fat_per_100_g = pydash.get(jsn, "response.snippet_list_updater_data.expandnutritional_information0.payload.snippets_to_add[6].data.subtitle.text")
        ingredients = pydash.get(jsn, 'response.snippet_list_updater_data.expandinfo0.payload.snippets_to_add[2].data.subtitle.text')
        Description = pydash.get(jsn, 'response.tracking.le_meta.custom_data.seo.attributes[0].value')
        FSSAI_License = pydash.get(jsn, 'response.snippet_list_updater_data.expandinfo0.payload.snippets_to_add[5].data.subtitle.text')
        Shelf_Life = pydash.get(jsn, 'response.snippets[0].data.overlay_data.expandable_data.expanded_state.vertical_item_list[1].subtitle.text')
        Disclaimer = pydash.get(jsn,'response.snippet_list_updater_data.expandinfo0.payload.snippets_to_add[7].data.subtitle.text')
        Country_of_origin= pydash.get(jsn,"response.snippet_list_updater_data.expandinfo0.payload.snippets_to_add[9].data.subtitle.text")
        Manufacturer_name = pydash.get(jsn,'response.snippet_list_updater_data.expandinfo0.payload.snippets_to_add[10].data.subtitle.text')
        Marketers_name_and_address = pydash.get(jsn,'response.snippet_list_updater_data.expandinfo0.payload.snippets_to_add[11].data.subtitle.text')
        Return_policy = pydash.get(jsn, 'response.snippet_list_updater_data.attributes_to_add_for_expanding_vpd.payload.snippets_to_add[0].data.horizontal_item_list[0].data.click_action.open_bottom_sheet.data.response.snippets[2].data.subtitle.text')
        Seller = pydash.get(jsn, 'response.snippet_list_updater_data.expandinfo0.payload.snippets_to_add[13].data.subtitle.text')
        Seller_FASSAI = pydash.get(jsn,'response.snippet_list_updater_data.expandinfo0.payload.snippets_to_add[14].data.subtitle.text')

        data = {
            "name": name,
            'pid': pid,
            'Price_of_1Kg':  Price_of_1kg,
            'Price_of_500g' : Price_of_500g,
            'Discount_on_1kg': Discount_on_1kg,
            'Discount_on_500g' : Discount_on_500g,
            'key_features' : key_features,
            'Protein_Per_100_g': Protein_Per_100_g,
            'Total_Carbohydrates_Per_100_g' : Total_Carbohydrates_Per_100_g,
            'Total_Sugar_Per_100_g' : Total_Sugar_Per_100_g,
            'Added_Sugars_Per_100_g': Added_Sugars_Per_100_g,
            'Total_fat_per_g' : Total_fat_per_g,
            'Saturated_fat_per_100_g':  Saturated_fat_per_100_g,
            'ingredients' : ingredients,
            'Description' : Description,
            'FSSAI_License' : FSSAI_License,
            'Shelf_Life' : Shelf_Life,
            'Disclaimer' : Disclaimer,
            'Country_of_origin' : Country_of_origin,
            'Manufacturer_name' : Manufacturer_name,
            'Marketers_name_and_address' : Marketers_name_and_address,
            'Return_policy' : Return_policy,
            'Seller' : Seller,
            'Seller_FASAI' : Seller_FASSAI
        }

        try:
            Atta_Rice_Dal_pdp.insert_one(data)

        except Exception as e:
            print("DB Error:", e)



        try:
            Atta_Rice_Dal.update_one(
                {'_id': product['_id']},
                {'$set': {'status': 'Done'}}
            )

        except Exception as e:
            print('failed to update:', e)

        print("Finished", name)
