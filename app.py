from flask import Flask, request, render_template

from handle_address import create_address, get_juris_permit_type_blocks
from soap_requests import get_juris_contact

app = Flask(__name__)



@app.route('/', methods=['GET','POST'])
def search_address():
    if request.method == 'GET':
        return render_template('index.html')
    address_string = request.form.get('address-input') or ""
    address_object = create_address(address_string)
    juris_permit_type_blocks = get_juris_permit_type_blocks(address_object)
    contact_blocks = []
    for juris_block in juris_permit_type_blocks:
        contact_block = get_juris_contact(juris_block=juris_block)
        contact_blocks.extend(contact_block)
        print(contact_block)

    
    return render_template('index.html', contact_blocks = contact_blocks)


if __name__ == '__main__':
    app.run()