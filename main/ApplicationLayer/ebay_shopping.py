# try:
#     import ApplicationLayer.ebay_config as ebay_config
# except:
#     import ebay_config
from ebaysdk.shopping import Connection

import ebay_config
api = Connection(appid=ebay_config.Client_ID, config_file=None)
def findProductIdbyItem(ItemID):
    payload = {'IncludeSelector':'Details',
               'ItemID':ItemID}
    # response = api.execute('GetSingleItem', {'ItemID':ItemID})
    response = api.execute('GetSingleItem', payload)
    return response

response = findProductIdbyItem(372146447706)
print(response.dict())
