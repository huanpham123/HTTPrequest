from flask import Flask, request, render_template, jsonify
import requests

app = Flask(__name__)

DEFAULT_TIMEOUT = 20  # Tăng thời gian timeout lên 20 giây

@app.route('/send-request', methods=['POST'])
def send_request():
    url = request.form.get('url')
    method = request.form.get('method')
    headers = request.form.get('headers')
    data = request.form.get('data')
    timeout = int(request.form.get('timeout', DEFAULT_TIMEOUT))

    try:
        if method == "GET":
            response = requests.get(url, headers=headers, timeout=timeout)
        elif method == "POST":
            response = requests.post(url, headers=headers, json=data, timeout=timeout)
        elif method == "PUT":
            response = requests.put(url, headers=headers, json=data, timeout=timeout)
        elif method == "DELETE":
            response = requests.delete(url, headers=headers, timeout=timeout)

        return jsonify({
            'status_code': response.status_code,
            'headers': dict(response.headers),
            'content': response.text
        })

    except requests.exceptions.Timeout:
        return jsonify({'error': 'The request timed out after {} seconds'.format(timeout)}), 504
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
