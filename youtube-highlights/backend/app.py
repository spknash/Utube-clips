from flask import Flask, request
from flask_cors import CORS
import sys
import jsonify

app = Flask(__name__)
CORS(app)

def process_url(url):
    print("the url is: ", file=sys.stderr)
    print(url, file=sys.stderr)

@app.route('/submit', methods=['POST'])
def submit():
    url = request.form.get('url')
    if url:
        # Process the URL here and return the result
        process_url(url)
        return jsonify({'submittedUrl': url})
    return jsonify({'error': 'Invalid URL'}), 400
if __name__ == '__main__':
    app.run(debug=True)