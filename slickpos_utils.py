import json, os
from core.models import SlickposProducts

headers = {
  'Authorization': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1aWQiOiI3MzcwZDc4Ni1lN2Y1LTQzNmYtYjYwOC0wYTc2NDRmZGI4ZTciLCJyb2wiOiJ1c2VyIiwiYXVkIjoidzRGNDV2cDVicGxldEFGZE5pWnhVRUV6cWFTemZ3SzAiLCJpYXQiOjE2MTI5NzQ5MDcsImlzcyI6InNsaWNrcG9zIn0.i7rTScUlAmZPK_jcoD-wQsP5OitUBFsEjjiRoQmcYaw'
}

import requests

get_a_receipt = requests.get('https://api.slickpos.com/api/sales?accountId=7370d786-e7f5-436f-b608-0a7644fdb8e7&createdAt=1607177955780&localReceiptNumber=GH-ZPR-2031-100628', headers=headers)

get_receipt_by_date = requests.get('https://api.slickpos.com/api/sales/daily?accountId=7370d786-e7f5-436f-b608-0a7644fdb8e7&registerId=489f4846-10a1-4b42-8d05-569221d8d227&receiptDate=20210218', headers=headers)

setup = requests.get('https://api.slickpos.com/api/setup?id=7370d786-e7f5-436f-b608-0a7644fdb8e7', headers=headers)

customer = requests.get('https://api.slickpos.com/api/customer/list?accountId=7370d786-e7f5-436f-b608-0a7644fdb8e7', headers=headers)

products = requests.get('https://api.slickpos.com/api/product/list?accountId=7370d786-e7f5-436f-b608-0a7644fdb8e7', headers=headers)

orders = requests.put('https://api.slickpos.com/api/setup/showIncomingTab', headers=headers)

# print(products.text)
print('hai')

# world_json = os.path.join(os.getcwd(), 'products.json')
# with open(world_json) as f:
#   pos_products = json.load(f)
# for product in pos_products:
#     country_data = SlickposProducts.objects.create(
#     slickpos_id = product['id'],
#     name = product['name'],
#     category_id = product['categoryId'],
#     taxgroup_id = product['taxGroupId'],
#     marked_price = product['markedPrice'],
#     register_id = product['registerId'],
#     variant_group_id = product['variantGroupIds'],
#     addon_group_id = product['addonGroupId'],
#     order_id = product['order']
# )