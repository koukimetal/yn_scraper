from flask import Flask, request, make_response
import datetime
import time
from jinja2 import Environment, PackageLoader

from webapp.scraper import extract_news

app = Flask(__name__)
env = Environment(autoescape=True, loader=PackageLoader('webapp', 'templates'))


@app.route('/', methods=['GET'])
def show_news():
    visited = request.cookies.get('visited')

    if visited is None:
        news = extract_news()
        expire_date = datetime.datetime.now()
        expire_date = expire_date + datetime.timedelta(minutes=5)

        template = env.get_template('news.html')
        resp = make_response(template.render(news=news))
        # Only unixtime works for some reason
        resp.set_cookie('visited', 'visited', expires=int(time.mktime(expire_date.timetuple())))

        return resp
    else:
        template = env.get_template('sorry.html')
        return template.render()


# This is for debugger
def port_check(hostname, port):
    import socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        result = sock.connect_ex((hostname, port))
    except socket.gaierror:
        sock.close()
        return False
    sock.close()
    return result == 0


if __name__ == '__main__':
    # This is for debugger
    debug_port = 5678
    if port_check('debug_host', debug_port):
        import pydevd
        pydevd.settrace('debug_host', port=debug_port, stdoutToServer=True, stderrToServer=True)

    app.run(host='0.0.0.0')
