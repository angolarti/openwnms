from flask import Flask, render_template

from openwnms.domain.models import Device
from settings import DEBUG

app = Flask(__name__)


@app.route('/')
def dashboard():
    devices = Device()

    return render_template(
        'dashboard.html',
        devices=devices.find_all(),
        total_devices=devices.total_devices(),
        count_device_scan_last_five_days = devices.count_last_device_scan_last_fine_days(),
        device_link_status=devices.link_status,
        device_is_up_and_down=devices.device_is_up_and_down()
    )


@app.route('/devices/<id>', methods=['GET'])
def device(id: str):
    return render_template('device.html', device=Device().find_one(id))


@app.route('/devices/<id>/report', methods=['GET'])
def device_report(id: str):
    return render_template('report.html', device=Device().find_one(id))


if __name__ == '__main__':
    device = Device()
    print(device.count_last_device_scan_last_fine_days())
    print(device.device_is_up_and_down())

    app.run(host='0.0.0.0', debug=DEBUG)
