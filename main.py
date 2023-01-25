from flask import Flask, request, Response, render_template, make_response
from functions import cfg
from os import environ


app = Flask(__name__)
app.config["DEBUG"] = False


@app.route('/')
def home():
    return render_template('index.html', cfg=cfg)


@app.route('/help')
def about():
    return render_template('help.html')


@app.route('/api', methods=['POST', 'GET'])
def api():
    args = process_req(request)
    if len(args) == 1:
        return render_template("evaluation_report.html", enum=enumerate, round=round)


@app.route('/remove_first_page', methods=['POST', 'GET'])
def api():
    args = process_req(request)
    if len(args) == 1:
        return render_template("evaluation_report.html", enum=enumerate, round=round)


def process_req(req):
    query_parameters = req.args
    if len(query_parameters) == 0:
        query_parameters = req.form

    text = query_parameters.get('text')
    if "eval" in query_parameters:
        args = [text]
    elif "pv" in query_parameters:
        x = cfg["inputs"]["visualisation"]
        args = [text]
    else:
        x = cfg["inputs"]["generation"]
        if query_parameters.get('count'):
            cn = int(query_parameters.get('count'))
        alt = query_parameters.get('alt')
        args = [text, cn]

    if "log" in cfg and cfg["log"]:
        try:
            with open(cfg["log"], "a+", encoding="utf-8") as lf:
                lf.write(request.remote_addr + "\t" + "\t".join([str(x) for x in args]) + "\n")
        except:
            pass

    return args


if __name__ == "__main__":
    port = int(environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
