# from zeep import Client

# #https://www.oregon.gov/bcd/_vti_bin/Lists.asmx
# client = Client('https://www.oregon.gov/bcd/_vti_bin/Lists.asmx?WSDL')
# #result = client.service.GetListItems('lbdd-location')

# f = open('soap_req.xml','rt',encoding='GB2312')
# s=f.read()
# response=client.service.DEMO1(s)


# print(f'result: {response}')

import requests
import xml.etree.ElementTree as ET
import re


namespaces = {
    'soap': 'http://schemas.xmlsoap.org/soap/envelope/',
    'a': 'http://www.etis.fskab.se/v1.0/ETISws',
    "sp": "http://schemas.microsoft.com/sharepoint/soap/",
    "rs": "urn:schemas-microsoft-com:rowset",
    "z": "#RowsetSchema"
}

URL = 'https://www.oregon.gov/bcd/_vti_bin/Lists.asmx'
HEADERS = {
    'cookie':'BIGipServer~Oregon~OR-prd-SP-txdc.pool=rd1530o00000000000000000000ffffac1f2148o80; Path=/; Secure; HttpOnly;',
    'content-type':'text/xml;charset=UTF-8'
}

body = ''

def make_request_string(place_name, city_county):
    body_string = f"<soap:Envelope xmlns:xsi='http://www.w3.org/2001/XMLSchema-instance' xmlns:xsd='http://www.w3.org/2001/XMLSchema' xmlns:soap='http://schemas.xmlsoap.org/soap/envelope/'><soap:Body><GetListItems xmlns='http://schemas.microsoft.com/sharepoint/soap/'><listName>lbdd-location</listName><viewName></viewName><query><Query>	<OrderBy> 	</OrderBy>	<Where> 	<Contains><FieldRef Name='{city_county}'/><Value Type='Text'>{place_name}</Value></Contains>	</Where>'	</Query></query><viewFields><ViewFields Properties='True' >  <FieldRef Name='Jurisdiction' />  <FieldRef Name='City' />  <FieldRef Name='Service_x0020_types' />  <FieldRef Name='Permits' />  <FieldRef Name='County' />  <FieldRef Name='Sorting' /> </ViewFields></viewFields><rowLimit>5000</rowLimit><queryOptions><QueryOptions><ViewAttributes Scope='Recursive' /></QueryOptions></queryOptions></GetListItems></soap:Body></soap:Envelope>"
    return body_string

test_body = make_request_string('Woodburn', 'City')
response = requests.post(URL, data = test_body, headers=HEADERS)

root = ET.fromstring(response.content)
rows = root.findall('.//z:row', namespaces)
print(f'found {len(rows)} rows')

juris_permit_array = []
for row in rows:
    juris_raw = row.attrib.get('ows_Jurisdiction')
    juris_clean = "".join(filter(str.isalpha, juris_raw))
    permit_types_raw = row.attrib.get('ows_Service_x0020_types')
    permit_types_clean = re.sub(r'[^a-zA-Z]', ' ', permit_types_raw)
    print(f'{juris_clean} handles{permit_types_clean}')


#print(response.content)
#xml_from_response = ET.ElementTree(ET.fromstring(response.content))
# tree = ET.ElementTree(ET.fromstring(response.content))
# print(tree)
# list_items = tree.findall('./soap:Envelope'
#                           '/soap:Body'
#                           '/a:GetListItemsResponse'
#                           '/a:GetListItemsResult'
#                           '/a:listitems'
#                           '/z:row'
#                           '/a:ows_Jurisdiction',
#                           namespaces)
# list_items = tree.findall('*/ows_Jurisdiction')
# for thing in list_items:
#     print(thing.text)
# print(f'list items: {list_items}')
# tree_string = ET.parse(tree)
# print(f'tree: {tree_string}')
# root = tree.getroot()
# list_items = tree_string.find('./soap:Envelope/', namespaces=namespaces)
# print(f'juris blocks: {list_items}')

# included_jurisdictions = []
