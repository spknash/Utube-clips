from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import processURL as pu


app = Flask(__name__)
CORS(app)


    

@app.route('/submit', methods=['POST'])
def submit():
    data = request.get_json()
    print(data)
    url = data.get('url')
    if url:
        # Process the URL here and return the result
        vid_details = pu.get_video_details(url)
        comments = pu.get_comments(url)
        #print("Received URL:", url)
        #print("details: ", vid_details)
        return jsonify({'submittedUrl': url})
    return jsonify({'error': 'Invalid URL'}), 400
if __name__ == '__main__':
    app.run(debug=True)

