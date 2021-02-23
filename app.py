import json
from bson import json_util

from flask import Flask, render_template, request, url_for, session, flash, redirect, jsonify

from openwnms.domain.models import Device
from openwnms.domain.services import LoginService
from settings import DEBUG


app = Flask(__name__)
app.config.from_object("config.Config")
app.secret_key = 'openwnms'


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/authenticate', methods=['POST',])
def authenticate():

    username = request.form['username']
    password = request.form['password']

    authenticated = LoginService.authenticate(username, password)

    if authenticated:
        session['user_logged'] = username
        flash(username + ' logado com sucesso!')
        next_page = request.form['next']
        print('Next: ' + next_page)
        return redirect(next_page)
    else:
        flash('Não logado tente denovo!')
        return redirect(url_for('login'))


@app.route('/logout')
def logout():
    session['user_logged'] = None
    flash('Nenhum utilizador logado')
    return redirect(url_for('login'))


@app.route('/')
def dashboard():
    if session['user_logged'] is None:
        return redirect(url_for('login'))

    devices = Device()

    return render_template(
        'dashboard.html',
        devices=devices.find_all(),
        total_devices=devices.total_devices(),
        count_device_scan_last_five_days = devices.count_last_device_scan_last_fine_days()
    )


@app.route('/devices/<id>', methods=['GET'])
def device(id: str):
    if session['user_logged'] is None:
        return redirect(url_for('login'))

    return render_template('device.html', device=Device().find_one(id))


@app.route('/devices/<id>/report', methods=['GET'])
def device_report(id: str):
    if session['user_logged'] is None:
        return redirect(url_for('login'))

    return render_template('report.html', device=Device().find_one(id))


@app.route('/ping', methods=['POST'])
def online():
    from openwnms.tools.utils import ping
    import json  
    
    response = jsonify(request.json).data    
    device = json.loads(response)
    is_online = ping(device['ip'])
    
    response = {
        'host': str(device['ip']),
        'online': is_online,
    }
    
    return jsonify(response)


@app.route('/device_up_down', methods=['POST'])
def device_up_down():
    from openwnms.tools.utils import ping
    
    response = jsonify(request.json).data
    devices = json.loads(response)
    
    device_up_down = {
        'up': 0,
        'down': 0
    }
    
    for device in devices['ips']:
        print(device)
        is_online = ping(device)
        
        print("Status: ", is_online)
    
        if is_online:
            device_up_down['up'] += 1
        else:
            device_up_down['down'] += 1
    
    return jsonify(device_up_down)


@app.route('/rescan', methods=['POST'])
def rescan():
    import main
    
    devices = main.scan()
    
    return jsonify(json.dumps(devices, default=json_util.default))


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=DEBUG)

    device = Device()
    print(device.count_last_device_scan_last_fine_days())