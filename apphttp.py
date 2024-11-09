from flask import Flask, request, render_template, jsonify
import requests
import time

app = Flask(__name__)

DEFAULT_TIMEOUT = 10  # Thời gian chờ mặc định

@app.route('/')
def index():
    return render_template('http.html')

@app.route('/send-request', methods=['POST'])
def send_request():
    url = request.form.get('url')
    method = request.form.get('method')
    headers = request.form.get('headers')
    data = request.form.get('data')
    timeout = request.form.get('timeout', DEFAULT_TIMEOUT)

    # Chuyển headers thành dictionary
    headers_dict = {}
    if headers:
        for line in headers.splitlines():
            key_value = line.split(": ", 1)
            if len(key_value) == 2:
                headers_dict[key_value[0].strip()] = key_value[1].strip()

    start_time = time.time()

    try:
        if method == "GET":
            response = requests.get(url, headers=headers_dict, timeout=int(timeout))
        elif method == "POST":
            response = requests.post(url, headers=headers_dict, json=data, timeout=int(timeout))
        elif method == "PUT":
            response = requests.put(url, headers=headers_dict, json=data, timeout=int(timeout))
        elif method == "DELETE":
            response = requests.delete(url, headers=headers_dict, timeout=int(timeout))

        end_time = time.time()
        elapsed_time = end_time - start_time

        return jsonify({
            'status_code': response.status_code,
            'headers': dict(response.headers),
            'content': response.text,
            'elapsed_time': f"{elapsed_time:.2f} seconds"
        })

    except requests.exceptions.Timeout:
        return jsonify({'error': f'The request timed out after {timeout} seconds'}), 504
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
