from flask import Flask, render_template

from openwnms.domain.models import Device
from settings import DEBUG

app = Flask(__name__)


@app.route('/')
def dashboard():
    devices = Device().find_all()

    return render_template('dashboard.html', devices=devices)


@app.route('/devices/<id>', methods=['GET'])
def device(id: str):
    return render_template('device.html', device=Device().find_one(id))


@app.route('/devices/<id>/report', methods=['GET'])
def device_report(id: str):
    return render_template('report.html', device=Device().find_one(id))


if __name__ == '__main__':
    app.run(debug=DEBUG)
