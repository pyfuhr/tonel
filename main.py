from flask import Flask, request
import logging
import json, os

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)

sessionStorage = {}
rabbit = []


@app.route('/post', methods=['POST'])
def main():
    logging.info('Request: %r', request.json)

    response = {
        'session': request.json['session'],
        'version': request.json['version'],
        'response': {
            'end_session': False
        }
    }

    handle_dialog(request.json, response)

    logging.info('Response: %r', request.json)

    return json.dumps(response)


@app.route('/')
def appp():
    return 'Work'


def handle_dialog(req, res):
    
    global rabbit
    
    user_id = req['session']['user_id']

    if req['session']['new']:
        sessionStorage[user_id] = {
            'suggests': [
                "Не хочу.",
                "Не буду.",
                "Отстань!",
            ]
        }
    if not (user_id in rabbit):
        res['response']['text'] = 'Привет! Купи слона!'
        res['response']['buttons'] = get_suggests(user_id)
        return
    else:
        res['response']['text'] = 'Привет! Купи кролика!'
        res['response']['buttons'] = get_suggests_rabbit(user_id)

    if not (user_id in rabbit):
        logging.info('111')
        for i in ['ладно', 'куплю', 'покупаю', 'хорошо']:
            if i in req['request']['original_utterance'].lower():
                res['response']['text'] = 'Слона можно найти на Яндекс.Маркете!'
                rabbit.append(user_id)
                logging.info('User ID: ' + srt(user_id))
    else:
        logging.info('000')
        for i in ['ладно', 'куплю', 'покупаю', 'хорошо']:
            if i in req['request']['original_utterance'].lower():
                res['response']['text'] = 'Кролика можно найти на Яндекс.Маркете!'
                res['response']['end_session'] = True
                try:
                    del rabbit[rabbit.index(user_id)]
                except:
                    pass
                
    if not (user_id in rabbit):
        res['response']['text'] = 'Все говорят "%s", а ты купи слона!' % (
            req['request']['original_utterance']
        )
        res['response']['buttons'] = get_suggests(user_id)
    else:
        res['response']['text'] = 'Все говорят "%s", а ты купи кролика!' % (
            req['request']['original_utterance']
        )
        res['response']['buttons'] = get_suggests_rabbit(user_id)


def get_suggests(user_id):
    session = sessionStorage[user_id]

    suggests = [
        {'title': suggest, 'hide': True}
        for suggest in session['suggests'][:2]
    ]

    session['suggests'] = session['suggests'][1:]
    sessionStorage[user_id] = session

    if len(suggests) < 2:
        suggests.append({
            "title": "Ладно",
            "url": "https://market.yandex.ru/search?text=слон",
            "hide": True
        })

    return suggests


def get_suggests_rabbit(user_id):
    session = sessionStorage[user_id]

    suggests = [
        {'title': suggest, 'hide': True}
        for suggest in session['suggests'][:2]
    ]

    session['suggests'] = session['suggests'][1:]
    sessionStorage[user_id] = session

    if len(suggests) < 2:
        suggests.append({
            "title": "Ладно",
            "url": "https://market.yandex.ru/search?text=слон",
            "hide": True
        })

    return suggests


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
