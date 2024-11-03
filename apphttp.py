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
            key_value = line.split(": ", 1)
            if len(key_value) == 2:
                headers_dict[key_value[0].strip()] = key_value[1].strip()

    try:
        # Gửi yêu cầu HTTP với phương thức đã chọn
        if method == "GET":
            response = requests.get(url, headers=headers_dict)
        elif method == "POST":
            response = requests.post(url, headers=headers_dict, json=data)  # Gửi dữ liệu dưới dạng JSON
        elif method == "PUT":
            response = requests.put(url, headers=headers_dict, json=data)  # Gửi dữ liệu dưới dạng JSON
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
