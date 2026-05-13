import requests
import xml.etree.ElementTree as ET
import re
import html


from classes.juris_info import JurisInfo
from classes.contact import Contact

CITY_STRING = 'City'
COUNTY_STRING = 'County'
EPERMITTING_URL = 'aca-oregon.accela.com'

URL = 'https://www.oregon.gov/bcd/_vti_bin/Lists.asmx'

HEADERS = {
    'cookie':'BIGipServer~Oregon~OR-prd-SP-txdc.pool=rd1530o00000000000000000000ffffac1f2148o80; Path=/; Secure; HttpOnly;',
    'content-type':'text/xml;charset=UTF-8'
}

NAMESPACES = {
    'soap': 'http://schemas.xmlsoap.org/soap/envelope/',
    'sp': 'http://schemas.microsoft.com/sharepoint/soap/',
    'rs': 'urn:schemas-microsoft-com:rowset',
    'z': '#RowsetSchema'
}

def request_juris(location_name, city_or_county):
    request_body = f"<soap:Envelope xmlns:xsi='http://www.w3.org/2001/XMLSchema-instance' xmlns:xsd='http://www.w3.org/2001/XMLSchema' xmlns:soap='http://schemas.xmlsoap.org/soap/envelope/'><soap:Body><GetListItems xmlns='http://schemas.microsoft.com/sharepoint/soap/'><listName>lbdd-location</listName><viewName></viewName><query><Query>	<OrderBy> 	</OrderBy>	<Where> 	<Contains><FieldRef Name='{city_or_county}'/><Value Type='Text'>{location_name}</Value></Contains>	</Where>'	</Query></query><viewFields><ViewFields Properties='True' >  <FieldRef Name='Jurisdiction' />  <FieldRef Name='City' />  <FieldRef Name='Service_x0020_types' />  <FieldRef Name='Permits' />  <FieldRef Name='County' />  <FieldRef Name='Sorting' /> </ViewFields></viewFields><rowLimit>5000</rowLimit><queryOptions><QueryOptions><ViewAttributes Scope='Recursive' /></QueryOptions></queryOptions></GetListItems></soap:Body></soap:Envelope>"
    response = requests.post(URL, data = request_body, headers=HEADERS)

    xml_root = ET.fromstring(response.content)
    rows = xml_root.findall('.//z:row', namespaces=NAMESPACES)

    juris_permit_type_array = []
    for row in rows:
        juris_raw = row.attrib.get('ows_Jurisdiction')
        juris_clean = re.sub(r'^[^#]*#', '', juris_raw)
        #juris_clean = "".join(filter(str.isalpha, juris_raw))

        permit_types_raw = row.attrib.get('ows_Service_x0020_types')
        permit_types_clean = re.sub(r'[^a-zA-Z]', ' ', permit_types_raw)
        permit_types_clean = permit_types_clean.strip()
        permit_types_array = permit_types_clean.split()

        if city_or_county == COUNTY_STRING:
            if juris_raw == location_name:
                juris_info_block = JurisInfo(jurisdiction_name=juris_clean, permit_types=permit_types_array)
                juris_permit_type_array.append(juris_info_block)
        else:
            juris_info_block = JurisInfo(jurisdiction_name=juris_clean, permit_types=permit_types_array)
            juris_permit_type_array.append(juris_info_block)
        print(f'{juris_clean} handles{permit_types_clean}')
    
    return juris_permit_type_array   



def get_juris_contact(juris_block: JurisInfo):
    juris_name = juris_block.jurisdiction_name or ''
    request_body = f"<soap:Envelope xmlns:xsi='http://www.w3.org/2001/XMLSchema-instance' xmlns:xsd='http://www.w3.org/2001/XMLSchema' xmlns:soap='http://schemas.xmlsoap.org/soap/envelope/'><soap:Body><GetListItems xmlns='http://schemas.microsoft.com/sharepoint/soap/'><listName>lbdd-Jurisdictions</listName><viewName></viewName><query><Query>	<OrderBy> 	<FieldRef Name='Sorting' Ascending='TRUE'/>	</OrderBy>	<Where>	</Where>'	</Query></query><viewFields> <ViewFields Properties='True' >  <FieldRef Name='Title' />  <FieldRef Name='Contact_x0020_information' />  <FieldRef Name='Sorting' /> </ViewFields></viewFields><rowLimit>5000</rowLimit><queryOptions><QueryOptions><ViewAttributes Scope='Recursive' /></QueryOptions></queryOptions></GetListItems></soap:Body></soap:Envelope>"
    response = requests.post(URL, data = request_body, headers=HEADERS)

    xml_root = ET.fromstring(response.content)
    contacts = xml_root.findall('.//z:row', namespaces=NAMESPACES)

    contact_info = []
    for contact in contacts:
        juris_listed_name = contact.attrib.get('ows_Title') or ''
        if juris_name.upper() == juris_listed_name.upper():
            juris_contact_obj_old = {}
            contact_chunk_raw = contact.attrib.get('ows_Contact_x0020_information') or ''
            juris_contact_html = html.unescape(contact_chunk_raw)
            print(f'adding a contact with juris of: {juris_block}')
            juris_contact_block = Contact(
                juris_block=juris_block,
                contact_info=juris_contact_html,
                is_on_epermitting=EPERMITTING_URL in contact_info
            )

            contact_info.append(juris_contact_block)
    
    return contact_info

