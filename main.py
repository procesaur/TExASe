from flask import Flask, request, render_template
from os import environ
from helper import cfg
from rq_handler import process_req
from redisworks import redis_q as q


app = Flask(__name__)
app.config["DEBUG"] = False


def count_and_save_words(i):
    return i


@app.route('/')
def home():
    return render_template('index.html', cfg=cfg)


@app.route('/help')
def about():
    return render_template('help.html')


@app.route('/api', methods=['POST', 'GET'])
def api():
    function, args = process_req(request)
    if q:
        job = q.enqueue(function, args)
        return "sent to redis que, id:" + str(job.get_id())
    else:
        return function(args)


@app.route('/remove_first_pages', methods=['POST', 'GET'])
def remove_first_pages():
    function, args = process_req(request)
    if q:
        job = q.enqueue(function, args)
        return "sent to redis que, id:" + str(job.get_id())
    else:
        return function(args)


if __name__ == "__main__":
    port = int(environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
