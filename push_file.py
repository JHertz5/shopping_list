from pushbullet import Pushbullet

def _get_pb_authKey():
    key_filename = './.pb'
    with open(key_filename,'r') as authFile:
        authKey = authFile.read()
    return authKey.strip()

def push_file(filename):
    authKey = _get_pb_authKey()
    pb = Pushbullet(authKey) # authenticate

    with open(filename, 'rb') as file_to_push:
        file_data = pb.upload_file(file_to_push, filename)

    push_data = pb.push_file(**file_data)
