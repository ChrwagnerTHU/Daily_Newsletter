import json
import finance_request

symbols = {"AIR"}
requester = finance_request.requester("J1AF3SZ0S4184JGT", 'stock_info.json')

data = requester.getDataDaily()

with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)
