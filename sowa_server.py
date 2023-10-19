from flask import Flask, render_template
from flask_restful import Api

import os.path
import logging

logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.INFO)


def root_dir():
    return os.path.abspath(os.path.dirname(__file__))


def get_file(filename):
    try:
        src = os.path.join(root_dir(), filename)
        print('---- Load file - ' + str(src))
        return open(src).read()
    except IOError as exc:
        return str(exc)


app = Flask(__name__)
api = Api(app)


@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')


@app.route('/save_bad_words', methods=['POST'])
def save_bad_words():
    return render_template('index.html')

# @app.route('/', methods=['GET'])
# def home():
#     content = get_file('templates/index.html')
#     return Response(content, mimetype="text/html")


# @app.route('/resources/templates/css/bootstrap.min.css', methods=['GET'])
# @app.route('/resources/templates/js/jquery.min.js', methods=['GET'])
# @app.route('/resources/templates/js/bootstrap.min.js', methods=['GET'])
# @app.route('/resources/bad_words.txt', methods=['GET'])
# def resources_txt():
#     print('---- Resources path - ' + str(request.path))
#     content = get_file(request.path[1:].replace("/", "\\"))
#     return Response(content, mimetype="text/html")
#
#
# @app.route('/resources/templates/image/sbIch.jpg', methods=['GET'])
# def resources_image():
#     print('---- Resources path - ' + str(request.path))
#     content = get_file(request.path[1:].replace("/", "\\"))
#     return Response(content, mimetype="image/jpeg", content_type="image/jpeg")


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
