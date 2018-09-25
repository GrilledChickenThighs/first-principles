try:
    import ApplicationLayer.ebay_config as ebay_config
except:
    import ebay_config
import datetime
from ebaysdk.exception import ConnectionError
from ebaysdk.finding import Connection
import pandas as pd
import sys
# query = '9780345803788'
api = Connection(appid=ebay_config.Client_ID, config_file=None)
# ISBN, UPC, EAN, or ReferenceID (ePID)
 # EAN values are typically 13 digits in length, but some use only eight digits.
 # ISBN values can be 10 characters (ISBN-10) or 13 characters (ISBN-13) in length, and they identify books.
 # MPN value is not based on an international standard, but is defined by the seller/manufacturer of the product. Technically, there is no maximum length for an MPN, but eBay actually enforces a 65-character limit for MPN values.
 # Reference: EPID is a commonly-used acronymn for an eBay Catalog product ID.
 # UPC values are 12 digits in length. UPC values identify a wide variety of products, and are typically used in the US and Canada.

# len('0025192072024')
# len('0025192072024')
# query=input('Please Enter UPC, ISBN, MPN, EAN or ProductId(ePID). The following format is accepted\nISBN:0123456789\n')
# query
# value, id = sanitizeInput(query)
# response = findCompletedItems(value, id)
# df = pd.DataFrame(response)
# parseResponse(response)
# df = toDataframe(parseResponse(response))
# dfg = df.groupby(by='conditionType', sort=False)
# dfg.describe()
# dfglt = df.groupby(by='listingType')
# dfglt.describe()

def sanitizeInput(input):
    idtype, value = input.split(':')
    idtype = idtype.lower().strip()
    value = value.strip()
    # # TODO: Split hyphens

    if 'upc' in idtype:
        return value, 'UPC'
        if len(value) == 12 and value.isdigit():
            return value, 'UPC'
        else:
            raise Exception('UPC value must be 12 digits in length')

    if 'ean' in idtype:
        if len(value) == 8 or len(value) == 13 and value.isdigit():
            return value, 'EAN'
        else:
            raise Exception('EAN value must be 13 or 8 digits in length')

    if 'isbn' in idtype:
        if len(value) ==  10 or len(value) == 13 and value.isdigit():
            return value, 'ISBN'
        else:
            # print('ISBN value must be 10 or 13 digits in length')
            raise Exception('ISBN value must be 10 or 13 digits in length')

    if 'mpn' in idtype:
        if len(value) < 65:
            return value, 'MPN'
        else:
            raise Exception('MPN value must be less than 65 characters in length')

    if 'productid' in idtype or 'pid' in idtype:
        if value.isdigit():
            return value, 'ReferenceID'
        else:
            raise Exception('ReferenceID must be digits')
    else:
        raise Exception('Input not recognized. Try again.')

def findCompletedItems(productId, idtype):
    print('fci')
    # Type accepts ISBN, EAN, MPN, RefercneID(ePID),and UPC
    payload = {'outputSelector':'SellerInfo',
               'productId': {
                   '#text':productId, '@attrs':{'type': idtype}},
               'paginationInput':{
                   'entriesPerPage':'100',
                   'pageNumber':1
               }}
    response = api.execute('findCompletedItems', payload)

    assert (response.reply.ack == 'Success'), response.reply # # TODO: Handler function that searchs for subsitute and then inputs back into function to run again. IE error 41 bad product ID. Search pid on web or other ebay api and run function again with different id or keywords
    assert (response.reply.searchResult._count != '0' ), ('No search Results')
    results = response.dict()['searchResult']['item']
    pages = response.dict()['paginationOutput']['totalPages']
    # Check to see if there are more results. Max 100 per page
    for page in range(2,int(pages)+1):
        payload = {'productId': {'#text':productId, '@attrs':{'type': idtype}},
                    'paginationInput':{
                        'entriesPerPage': '100',
                        'pageNumber':page
                        },
                    'outputSelector':'SellerInfo'}
        response = api.execute('findCompletedItems', payload)
        results += response.dict()['searchResult']['item'] # Concatenate page results
    return results

def parseResponse(results):
    print('PR')

    my_items = []
    itemslist = results
    # rdict = response.dict()
    # assert(rdict['ack'] == 'Success')
    # assert(rdict['searchResult'] != 0 )
    # itemslist = rdict['searchResult']['item']
    for i, item in enumerate(itemslist):
        my_dict = dict()
        shippingType = itemslist[i]['shippingInfo']['shippingType']

        if shippingType == 'Calculated':
            continue
        if 'productId' in itemslist[i]:
            my_dict['productId'] = itemslist[i]['productId']['value']
        else:
            my_dict['productId'] = None

        my_dict['itemId'] = itemslist[i]['itemId']
        my_dict['title'] = itemslist[i]['title']
        my_dict['shippingPrice'] = itemslist[i]['shippingInfo']['shippingServiceCost']['value']
        my_dict['handlingTime'] = itemslist[i]['shippingInfo']['handlingTime']
        my_dict['price'] = itemslist[i]['sellingStatus']['currentPrice']['value']
        my_dict['startTime'] = itemslist[i]['listingInfo']['startTime']
        my_dict['endTime'] = itemslist[i]['listingInfo']['endTime']
        my_dict['listingType'] = itemslist[i]['listingInfo']['listingType']
        my_dict['conditionId'] = itemslist[i]['condition']['conditionId']
        my_dict['conditionType'] = itemslist[i]['condition']['conditionDisplayName']
        my_items.append(my_dict)
    return my_items

def toDataframe(items):
    print('TD')

    df = pd.DataFrame(items)
    df = df.convert_objects(convert_numeric=True)
    df['endTime'] = pd.to_datetime(df['endTime'])
    df['startTime'] = pd.to_datetime(df['startTime'])
    df['totalPrice'] = df['price'] + df['shippingPrice']
    return df

def produceDataset(query):
    value, idtype = sanitizeInput(query)
    response = findCompletedItems(value, idtype)
    items = parseResponse(response)

    return toDataframe(items)
