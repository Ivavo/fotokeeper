import os
import time
import magic
import zipfile
import pathlib
import shutil
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


def read_log(file_name):
    key = load_key()
    crypto = Fernet(key)
    with open(file_name, 'rb') as log:
        text = log.read()
        #print(text)
        decrypted_data = crypto.decrypt(text)
        decoded_data = decrypted_data.decode('utf-8')
        #print(decoded_data)
        images_log = decoded_data.split(':')
        print(images_log)
        return images_log


def uploader(log_name, dir_name):
    dir_name = dir_name
    files_list = read_log(log_name)
    p = 0
    for file in files_list:
        p += 1
        route = file
        print(file)
        try:
            source = f'/home/pc/project5/photokeeper/{route}'
            if os.path.exists(source):
                result_path = dir_name
                move = shutil.move
                move(source, result_path)
                print(p)
            else:
                print('not')
        except OSError:
            pass


_route = pathlib.Path(__file__).parents[1]
log_name = 'log.txt'
sleep_time = 5


def image_seeker(images_route):
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
    return images


def zipping(data, regime, name='Archive.zip'):
    with zipfile.ZipFile(name, f'{regime}') as archive:
        for file in data:
            file_path = os.path.join('..', file)
            print(file_path)
            archive.write(file_path)


def main():
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
                    print('log_file not in directory making log file and archive!')
                    zipping(images, 'w')
                elif log_name in status:
                    try:
                        images_log = read_log(log_name)
                        log_number = len(images_log)
                        current_number = len(images)
                        if images_log != images:
                            difference = list(set(images) - set(images_log))
                            file_name = 'difference_log.txt'
                            archive_name = 'New.zip'
                            if file_name not in status:
                                logging(difference, file_name)
                                zipping(difference, 'w', archive_name)
                                print('difference_list not found')
                            else:

                                logging(difference, file_name)
                                print('ttt', difference, len(difference), sep='\n')
                                #zipping(difference, 'a', archive_name)
                        else:
                            dif = read_log('difference_log.txt')
                            logging('', 'difference_log.txt')
                            print(len(dif))
                            pass

                    except FileNotFoundError:
                        pass
            except FileNotFoundError:
                pass
            logging(images, log_name)
            print(_route)
    except KeyboardInterrupt:
        print("Job ended!")
        logging(images, log_name)


if __name__ == '__main__':
    main()