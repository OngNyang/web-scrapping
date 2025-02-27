from flask import Flask, request, jsonify

from crawler import naver_map_crawler

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'

@app.route('/crawl', methods=['GET'])  # ✅ GET 요청만 허용
def crawl():
    search_query = request.args.get('query')  # URL에서 query 파라미터 가져오기
    print("검색어: ")
    print(search_query)
    if not search_query:
        return jsonify({'error': 'No search query provided'}), 400  # 검색어 없으면 에러 반환

    result = naver_map_crawler(search_query)  # 크롤링 실행
    print("결과")
    print(result)

    return jsonify({"message": result, "file": "output/results.xlsx"})  # 결과 반환

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
