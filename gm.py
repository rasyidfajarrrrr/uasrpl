"""
group_monitor - Simple web app to manage groups and show participants on monitors.
"""

from flask import Flask, redirect, render_template, abort, request, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_httpauth import HTTPBasicAuth

from faker import Faker


# create Faker instance for name generation and set locale
fake = Faker(locale='de_DE')

# initialize HTTP server
app = Flask(__name__)
auth = HTTPBasicAuth()


# global list containing all participants for all groups
GROUP_COUNT = 6
groups = [('', '', '') for _ in range(GROUP_COUNT)]


@app.route('/', methods=['GET'])
def start():
    global groups
    fake_names = True if 'fake' in request.args else False
    notification = ''
    if 'success' in request.args:
        notification = 'Einträge wurden gespeichert!'
    if 'cleared' in request.args:
        notification = 'Einträge wurden gelöscht!'
    return render_template('index.html', heading='Gruppen-Monitor',
                           content=build_group_form(groups, fake_names=fake_names), notification=notification)


def build_group_form(group_list, fake_names=False):
    content = '<h1 class="title"><a href="/">Gruppen-Monitor</a></h1><form action="/groups" method="POST">'
    for i, g in enumerate(group_list):
        content += f"""<div class="group-block">
            <h2 class="subtitle"><a href="{url_for('monitor', no=i)}" class="button is-primary">Gruppe {i + 1}</a></h2>
            <div class="field-group">
            <div class="field is-inline-block-desktop ml-4">
            <label class="label" for="group{i}-name1">Name 1</label>
            <div class="control"><input class="input is-primary is-one-quarter" type="text" name="group{i}-name1" id="group{i}-name1" size="40" value="{fake.name() if fake_names else g[0]}"/></div>
            </div>
            <div class="field is-inline-block-desktop ml-4">
            <label class="label" for="group{i}-name2">Name 2</label>
            <div class="control"><input class="input is-primary is-one-quarter" type="text" name="group{i}-name2" id="group{i}-name2" size="40" value="{fake.name() if fake_names else g[1]}"/></div>
            </div>
            <div class="field is-inline-block-desktop ml-4">
            <label class="label" for="group{i}-name3">Name 3</label>
            <div class="control"><input class="input is-primary is-one-quarter" type="text" name="group{i}-name3" id="group{i}-name3" size="40" value="{fake.name() if fake_names else g[2]}"/></div>
            </div>
        </div>
        """
    content += '<div class="buttons is-right"><input class="button is-primary" type="submit" value="Speichern..."></div></form>'
    return content


@app.route('/monitor/<int:no>')
def monitor(no):
    global groups
    try:
        content = f"""<section class="hero is-primary is-medium mt-6">
            <div class="hero-body">
                <p class="title is-size-1">
                    Gruppenmitglieder Gruppe {no + 1}
                </p>
                <p class="subtitle">
                    {''.join(['<div class="box nametag">{}</div>'.format(n) for n in groups[no] if n])}
                </p>
            </div>
            </section>
        """
        return render_template('index.html', heading=f'Gruppe Nr. {no + 1}', content=content, notification='', refresh=True)
    except IndexError:
        return render_template('index.html', heading=f'Fehlerhafte Gruppennummer',
                               content=f'Gruppe {no} gibt es nicht!', notification='')


@auth.verify_password
def verify_password(username, password):
    if check_password_hash(generate_password_hash('1234'), password):
        return username
    return None


@app.route('/groups', methods=['GET', 'POST'])
@auth.login_required
def add():
    global groups
    if request.method == 'GET':
        group_block_html = """<div class="card"><div class="card-content">
            <div class="media"><div class="media-content">
                <p class="title is-4">{}</p>
            </div></div>
                <div class="content">{}</div>
            </div></div>"""
        content = '<h1 class="title">Gruppen</h1>' + \
                  '\n'.join([group_block_html.format(i + 1, ', '.join([n for n in g]))
                             for i, g in enumerate(groups)])
        return render_template('index.html', notification='', content=content)
    elif request.method == 'POST':
        groups.clear()
        for i in range(GROUP_COUNT):
            groups.append((request.form.get(f'group{i}-name1'), request.form.get(
                f'group{i}-name2'), request.form.get(f'group{i}-name3')))
        return redirect(url_for('start', success=True))
    else:
        return abort(404)


@app.route('/groups/clear')
def clear():
    global groups
    groups = [('', '', '') for _ in range(GROUP_COUNT)]
    return redirect(url_for('start', cleared=True))


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
