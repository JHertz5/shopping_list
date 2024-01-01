from pushbullet import Pushbullet


def _get_pb_authKey():
    key_filename = './.pb'
    with open(key_filename, 'r') as auth_file:
        auth_key = auth_file.read()
    return auth_key.strip()


def push_file(filename):
    auth_key = _get_pb_authKey()
    pb = Pushbullet(auth_key)  # authenticate

    with open(filename, 'rb') as file_to_push:
        file_data = pb.upload_file(file_to_push, filename)

    push_data = pb.push_file(**file_data)
