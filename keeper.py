import os
import time
import magic
import json
import zipfile
import pathlib
from cryptography.fernet import Fernet


def load_key():
    with open('key.txt', 'rb') as key_file:
        key = key_file.read()
        return key


def logging(data, file_name):
    key = load_key()
    crypto = Fernet(key)
    one_str_data = ':'.join(data)
    bytes_data = bytes(one_str_data, 'utf-8')
    encrypt_data = crypto.encrypt(bytes_data)
    with open(file_name, 'wb') as log:
        log.write(encrypt_data)
        print('logged')


def _logging(data, file_name):
    with open(file_name, 'w') as log:
        json.dump(data, log)
        print('logged')


def read_log(file_name):
    key = load_key()
    crypto = Fernet(key)
    with open(file_name, 'rb') as log:
        text = log.read()
        print(text)
        decrypted_data = crypto.decrypt(text)
        decoded_data = decrypted_data.decode('utf-8')
        print(decoded_data)
        images_log = decoded_data.split(':')
        print(images_log)
        return images_log


def image_seeker(images_route):
    global file_format
    images = []
    status = []
    for file_names in images_route:
        file = str(file_names).split('/')[1]
        status.append(file)
    for file in status:
        img_name = file
        files_path = os.path.join(_route, img_name)
        try:
            file_format = magic.from_file(files_path, mime=True).split('/')
        except IsADirectoryError:
            pass
        file_type = file_format[0]
        if file_type == 'image':
            images.append(img_name)
    kn = tuple(images)
    m = hash(kn)

    print(images, m, sep='\n')
    return images


def zipping(data, regime, name='Archive.7z'):
    with zipfile.ZipFile(name, f'{regime}') as archive:
        for file in data:
            file_path = os.path.join('..', file)
            print(file_path)
            archive.write(file_path)


_route = pathlib.Path(__file__).parents[1]
log_name = 'log.txt'
sleep_time = 10
try:
    while True:
        print('loop')
        program_route = pathlib.Path().iterdir()
        images_route = pathlib.Path('..').iterdir()
        time.sleep(sleep_time)
        status = []
        try:
            images = image_seeker(images_route)
            for files in program_route:
                status.append(str(files))
            if log_name not in status:
                logging(images, log_name)
                print('log_file not in directory making log file and archive! ')
                zipping(images, 'w')
            elif log_name in status:
                try:
                    images_log = read_log(log_name)
                    log_number = len(images_log)
                    current_number = len(images)
                    if images_log != images:
                        difference = list(set(images) - set(images_log))
                        if 'difference_log.txt' not in status:
                            logging(difference, "difference_log.txt")
                            zipping(difference, 'w', 'New.zip')
                            print('difference_list not found')
                        else:
                            logging(difference, "difference_log.txt")
                            print('ttt', difference)
                            zipping(difference, 'a', name='New.zip')

                    else:
                        read_log('difference_log.txt')
                        pass

                except FileNotFoundError:
                    pass
        except FileNotFoundError:
            pass
        logging(images, log_name)

except KeyboardInterrupt:
    print("Job ended!")
    logging(images, log_name)
