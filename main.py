from flask import Flask, request, render_template
from os import environ
from helper import cfg
from rq_handler import process_req, process_req2, task_in_background
import redis
from rq import Queue


app = Flask(__name__)
app.config["DEBUG"] = False
#r = redis.Redis()
#q = Queue(connection=r)


@app.route('/')
def home():
    return render_template('index.html', cfg=cfg)


@app.route('/help')
def about():
    return render_template('help.html')


@app.route('/api', methods=['POST', 'GET'])
def api():
    #q.enqueue(process_req)
    return process_req2()



@app.route('/remove_first_pages', methods=['POST', 'GET'])
def remove_first_pages():
    process_req(request, target="remove_first_pages")
    #q.enqueue(process_req, args=request, kwargs={"target": "remove_first_pages"})


if __name__ == "__main__":
    port = int(environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
