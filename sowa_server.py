from flask import Flask, render_template, redirect, request
from flask_restful import Api

import os.path
import logging


handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s'))

log = logging.getLogger('sowa_server')
log.setLevel(logging.INFO)
log.addHandler(handler)

log_flask = logging.getLogger('werkzeug')
log_flask.disabled = True


def root_dir():
    return os.path.abspath(os.path.dirname(__file__))


def get_file(filename):
    try:
        src = os.path.join(root_dir(), filename)
        print('---- Load file - ' + str(src))
        return open(src).read()
    except IOError as exc:
        return str(exc)


def save_file(filename, content):
    log.info("Сохраняем изменения в файл '{}':\n{}".format(filename, content))
    with open(filename, 'w', encoding='utf-8', newline='') as f:
        f.write(content)


app = Flask(__name__)
api = Api(app)


@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')


@app.route('/save_bad_words', methods=['POST'])
def save_bad_words():
    save_file('./static/bad_words.txt', request.form['badWords'])
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
