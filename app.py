import detector
from flask import Flask, redirect, url_for, request, jsonify
app = Flask(__name__)


@app.route('/detectDiagram', methods=['POST'])
def post_detectAndApplyResutls():
    # print(request.json)
    # return jsonify({'sucess': True})

    if('authectication' == request.json['code']):
        res = detector.detectDiagram(request.json['imageString'])
        # return res
        return jsonify({'sucess': True, 'data': res})


if __name__ == "__main__":
    app.run(debug=True)
