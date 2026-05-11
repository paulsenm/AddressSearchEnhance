from flask import Flask, request, render_template

from handle_address import handle_address

app = Flask(__name__)



@app.route('/', methods=['GET','POST'])
def search_address():
    if request.method == 'GET':
        return render_template('index.html')
    address_string = request.form.get('address-input')
    complete_info = handle_address(address_string)
    print(complete_info)
    return render_template('index.html', complete_info = complete_info)


if __name__ == '__main__':
    app.run()