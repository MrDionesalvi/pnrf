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
                    <td class="reallocable">{"Sì" if int(c['reallocable']) == 1 else "No"}</td>
                    <td class="occuped">{"Sì" if int(c['occuped']) == 1 else "No"}</td>
                    <td class="butons">
                        <button value="{c['id']}" class="remove-item-btn button is-danger is-small" onclick="DeleteButton(this)">Elimina</button>
                        <button value="{c['id']}" class="change-item-btn button is-warning is-small" onclick="ChangeButton(this)">Ri-Alloca</button>
                    </td>
                </tr>
        """

    return render_template('dashboard.html', value=allValue, rows=table)
