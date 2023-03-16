from flask import Flask, request, render_template, Response
from os import environ
from helper import cfg
from rq_handler import process_req
from redisworks import q


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
        text, out_file = function(args)
        if out_file:
            return Response(out_file, mimetype="applictaion/pdf",
                            headers={'Content-Disposition': 'attachment;filename=result.pdf'})
        else:
            return text


if __name__ == "__main__":
    port = int(environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
