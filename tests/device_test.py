from openwnms.domain.models import Device


def list_devices():

    devices = Device().find_all()
    for device in devices:
        print(device)


if __name__ == '__main__':
    list_devices()
