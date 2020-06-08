import detector
from flask import Flask, redirect, url_for, request, jsonify
app = Flask(__name__)


@app.route('/detectDiagram', methods=['POST'])
def post_detectAndApplyResutls():
    if('authectication' == request.json['code']):
        detector.detectDiagram()
        return jsonify({'sucess': True})


if __name__ == "__main__":
    app.run(debug=True)
