from flask import Flask, request, render_template, Response
from os import environ, path as px
from helper import cfg, get_return_type
from rq_handler import process_req
from services import services
from base64 import b64encode

try:
    from redisworks import q
except ImportError:
    q = None


app = Flask(__name__)
app.config["DEBUG"] = False


@app.route('/')
def home():
    return render_template('index.html', cfg=cfg)


@app.route('/help')
def about():
    return render_template('help.html')


@app.route('/api/<service>', methods=['POST', 'GET'])
def api(service):

    filename, args = process_req(request, service)

    if service not in services or service not in cfg["services"]:
        return ""

    f = services[service]
    return_type = get_return_type(service)

    if q and not return_type:
        job = q.enqueue(f, args)
        return "sent to redis que, id:" + str(job.get_id())
    else:
        text, out_file = f(args)

        if return_type == "text":
            return text

        if return_type == "file":
            return Response(out_file, mimetype="applictaion/pdf",
                            headers={'Content-Disposition': 'inline;filename=' + filename + '.pdf'})
        else:
            b64 = b64encode(out_file).decode("utf-8")
            return render_template('gui_response.html', file=b64, text=text)


if __name__ == "__main__":
    port = int(environ.get("PORT", 5001))
    app.run(host='0.0.0.0', port=port)
