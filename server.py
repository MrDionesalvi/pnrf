from flask import *
from datetime import timedelta

from api.api import api
import time



app = Flask(__name__, template_folder='views', static_folder='assets', static_url_path='/assets')
app.secret_key = 'E6pdioneCazzBigEnorm121S9FKWgPGiGN6jx6s8yk2X3TT'


app.register_blueprint(api, url_prefix='/api')

@app.before_request
def make_session_permanent():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(hours=5)

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route('/sitemap.xml', methods=['GET', 'POST'])
def sitemap():
    return send_from_directory(app.static_folder, 'sitemap.xml')

@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('index.html'), 404




def start_site():
    try:
        app.debug = True
        app.run(host='0.0.0.0', port=53056, threaded=True)
    except Exception as e:
        print(e)
        time.sleep(2)
        start_site()

if __name__ == '__main__':
    start_site()