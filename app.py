from flask import Flask, request, jsonify

from crawler import naver_map_crawler

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'

@app.route('/crawl', methods=['POST'])
def crawl():
    data = request.json
    search_query = data.get('query')

    if not search_query:
        return jsonify({'error': 'No search query provided'}), 400

    result = naver_map_crawler(search_query)

    return jsonify({"message": result, "file": "output/results.xlsx"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
