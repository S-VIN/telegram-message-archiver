from flask import Flask
from flask import request
import json
import sqlite3

app = Flask(__name__)


def get_last_message():
    connect = sqlite3.connect('messages.db')
    t = connect.execute("SELECT author, message FROM messages ORDER BY id DESC LIMIT 1")
    result = ''
    for row in t:
        result += row[0]
        result += ' '
        result += row[1]
    return result


@app.route('/post', methods=['POST'])
def main():
    ## Создаем ответ
    response = {
        'session': request.json['session'],
        'version': request.json['version'],
        'response': {
            'end_session': False
        }
    }
    ## Заполняем необходимую информацию
    handle_dialog(response, request.json)
    return json.dumps(response)


def handle_dialog(res,req):
    ## Проверяем, есть ли содержимое
    # res['response']['text'] = req['request']['original_utterance']
    res['response']['text'] = get_last_message()



if __name__ == '__main__':
    app.run()