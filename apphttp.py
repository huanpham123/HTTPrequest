from flask import Flask, request, render_template, jsonify
import requests

app = Flask(__name__)

# Thời gian chờ mặc định cho các yêu cầu HTTP (tính bằng giây)
DEFAULT_TIMEOUT = 10  # thời gian chờ là 10 giây

@app.route('/')
def index():
    return render_template('http.html')

@app.route('/send-request', methods=['POST'])
def send_request():
    url = request.form.get('url')
    method = request.form.get('method')
    headers = request.form.get('headers')
    data = request.form.get('data')
    timeout = request.form.get('timeout', DEFAULT_TIMEOUT)  # Lấy thời gian chờ từ form (mặc định 10 giây)

    # Chuyển đổi headers thành dictionary nếu có
    headers_dict = {}
    if headers:
        for line in headers.splitlines():
            key_value = line.split(": ", 1)
            if len(key_value) == 2:
                headers_dict[key_value[0].strip()] = key_value[1].strip()

    try:
        # Gửi yêu cầu HTTP với thời gian chờ và phương thức đã chọn
        if method == "GET":
            response = requests.get(url, headers=headers_dict, timeout=int(timeout))
        elif method == "POST":
            response = requests.post(url, headers=headers_dict, json=data, timeout=int(timeout))
        elif method == "PUT":
            response = requests.put(url, headers=headers_dict, json=data, timeout=int(timeout))
        elif method == "DELETE":
            response = requests.delete(url, headers=headers_dict, timeout=int(timeout))

        return jsonify({
            'status_code': response.status_code,
            'headers': dict(response.headers),
            'content': response.text
        })

    except requests.exceptions.Timeout:
        return jsonify({'error': 'The request timed out after {} seconds'.format(timeout)}), 504
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
