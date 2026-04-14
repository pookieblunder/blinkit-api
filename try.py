import requests

cookies = {
    '_fbp': 'fb.1.1767937884119.190796487447140728',
    'gr_1_lat': '17.3924982',
    'gr_1_lon': '78.46796379999999',
    'gr_1_locality': 'Hyderabad',
    'gr_1_landmark': 'undefined',
    'gr_1_deviceId': '54fb06bd-2bc2-4353-9a0a-89cdcf6ce4f4',
    '_gcl_au': '1.1.1561759622.1775729167',
    'city': 'Shanghai',
    '__cf_bm': 'bGdZ__oRIdgSkPn_IvzmZXZUR1SJ6lNmqZ_cdjYMbyE-1776076387-1.0.1.1-xcPKHAQVSuZRjEIHjvFPWDd.JjcqoDvcEkFMZGXQVC2GLaCkqpso2QKCFFE6kDadx041p1fmLQfjy7lkr8Y80SjV3KfpLTLKl6oE78.5VmM',
    '_cfuvid': '2k9TMleanJcs4xmRnYa8yshVN1fIR6EcuQBlpSJ8XKQ-1776076387134-0.0.1.1-604800000',
    '_gid': 'GA1.2.1071137803.1776076391',
    '_gat_UA-85989319-1': '1',
    '_ga_JSMJG966C7': 'GS2.1.s1776076390$o18$g1$t1776076572$j8$l0$h0',
    '_ga': 'GA1.2.2074212143.1767937880',
    '_ga_DDJ0134H6Z': 'GS2.2.s1776076392$o15$g1$t1776076572$j9$l0$h0',
}

headers = {
    'accept': '*/*',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'access_token': 'null',
    'app_client': 'consumer_web',
    'app_version': '1010101010',
    'auth_key': 'c761ec3633c22afad934fb17a66385c1c06c5472b4898b866b7306186d0bb477',
    # 'content-length': '0',
    'content-type': 'application/json',
    'device_id': '1974ea9676ec33dc',
    'lat': '17.3924982',
    'lon': '78.46796379999999',
    'origin': 'https://blinkit.com',
    'priority': 'u=1, i',
    'referer': 'https://blinkit.com/s/?q=chocolate',
    'rn_bundle_version': '1009003012',
    'sec-ch-ua': '"Chromium";v="146", "Not-A.Brand";v="24", "Google Chrome";v="146"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'session_uuid': '95a726fc-f077-45af-816b-153ff47b8552',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36',
    'web_app_version': '1008010016',
    # 'cookie': '_fbp=fb.1.1767937884119.190796487447140728; gr_1_lat=17.3924982; gr_1_lon=78.46796379999999; gr_1_locality=Hyderabad; gr_1_landmark=undefined; gr_1_deviceId=54fb06bd-2bc2-4353-9a0a-89cdcf6ce4f4; _gcl_au=1.1.1561759622.1775729167; city=Shanghai; __cf_bm=bGdZ__oRIdgSkPn_IvzmZXZUR1SJ6lNmqZ_cdjYMbyE-1776076387-1.0.1.1-xcPKHAQVSuZRjEIHjvFPWDd.JjcqoDvcEkFMZGXQVC2GLaCkqpso2QKCFFE6kDadx041p1fmLQfjy7lkr8Y80SjV3KfpLTLKl6oE78.5VmM; _cfuvid=2k9TMleanJcs4xmRnYa8yshVN1fIR6EcuQBlpSJ8XKQ-1776076387134-0.0.1.1-604800000; _gid=GA1.2.1071137803.1776076391; _gat_UA-85989319-1=1; _ga_JSMJG966C7=GS2.1.s1776076390$o18$g1$t1776076572$j8$l0$h0; _ga=GA1.2.2074212143.1767937880; _ga_DDJ0134H6Z=GS2.2.s1776076392$o15$g1$t1776076572$j9$l0$h0',
}

params = {
    'offset': '12',
    'limit': '12',
    'actual_query': 'chocolate',
    'last_snippet_type': 'product_card_snippet_type_2',
    'last_widget_type': 'listing_container',
    'page_index': '1',
    'q': 'chocolate',
    'search_count': '859',
    'search_method': 'basic',
    'search_type': 'type_to_search',
    'total_entities_processed': '1',
    'total_pagination_items': '859',
}

response = requests.post('https://blinkit.com/v1/layout/search', params=params, cookies=cookies, headers=headers)

print(response.status_code)
print('')