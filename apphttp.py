from flask import Flask, request, render_template, jsonify
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('http.html')

@app.route('/send-request', methods=['POST'])
def send_request():
    url = request.form.get('url')
    method = request.form.get('method')
    headers = request.form.get('headers')
    data = request.form.get('data')

    headers_dict = {}
    if headers:
        # Chuyển đổi headers từ chuỗi sang từ điển
        for line in headers.splitlines():
            key, value = line.split(": ", 1)
            headers_dict[key] = value

    try:
        # Gửi yêu cầu HTTP với phương thức đã chọn
        if method == "GET":
            response = requests.get(url, headers=headers_dict)
        elif method == "POST":
            response = requests.post(url, headers=headers_dict, json=data)  # Thay đổi thành json nếu cần
        elif method == "PUT":
            response = requests.put(url, headers=headers_dict, json=data)  # Thay đổi thành json nếu cần
        elif method == "DELETE":
            response = requests.delete(url, headers=headers_dict)

        return jsonify({
            'status_code': response.status_code,
            'headers': dict(response.headers),
            'content': response.text
        })

    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
