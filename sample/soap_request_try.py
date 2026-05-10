# from zeep import Client

# #https://www.oregon.gov/bcd/_vti_bin/Lists.asmx
# client = Client('https://www.oregon.gov/bcd/_vti_bin/Lists.asmx?WSDL')
# #result = client.service.GetListItems('lbdd-location')

# f = open('soap_req.xml','rt',encoding='GB2312')
# s=f.read()
# response=client.service.DEMO1(s)


# print(f'result: {response}')

import requests

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

print(response.content)