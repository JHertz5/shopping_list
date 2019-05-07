from pushbullet import Pushbullet

def get_pb_authKey():
    filename = './.pb'
    with open(filename,'r') as authFile:
        authKey = authFile.read()
    return authKey.strip()

def push_file(filename, authKey):

    pb = Pushbullet(authKey) # authenticate

    with open(filename, 'rb') as file_to_push:
        file_data = pb.upload_file(file_to_push, filename)

    push_data = pb.push_file(**file_data)
