from flask import *
from utils import *
from database import Database

dashboard = Blueprint('dashboard', __name__, template_folder='views', static_folder='assets', static_url_path='/assets')


@dashboard.route('/')
@login_required
def index():
    table = ""
    a = get_allFrequency()
    b = json.loads(a)
    allValue = {
        "frequencyRegistered": len(b),
        "peopleRegistered": 31,
        "frequencyAviable": 999-int(len(b))
    }
    for c in b:
            table += f"""
                <tr>
                    <td class="id">{c['id']}</td>
                    <td class="owner">{c['owner']}</td>
                    <td class="reallocable">{"Sì" if c['reallocable'] == 1 else "No"}</td>
                    <td class="occuped">{"Sì" if c['occuped'] else "No"}</td>
                    <td class="remove"><button value="{c['id']}" class="remove-item-btn" onclick="DeleteButton(this)">Elimina</button></td>
                </tr>
        """

    return render_template('dashboard.html', value=allValue, rows=table)
