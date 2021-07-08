import os
import sys
import time
import magic
import zipfile
import pathlib
import shutil
from cryptography.fernet import Fernet


##############################################################################################
def new_seeker():
    route_root = pathlib.Path(__file__).parents[0]
    _route1 = pathlib.Path(__file__).parents[1]
    iteration_files = os.walk(_route1)
    roads = []
    files = []
    for i in iteration_files:
        if str(route_root) in str(i[0]):
            continue
        else:
            string = i[0], i[2]
            roads.append(string)
    #print(roads)
    for i in roads:
        for t in i[1]:
            r = os.path.join(i[0], t)
            #print(r)
            try:
                file_format_name = magic.from_file(r, mime=True).split('/')
                #print(file_format_name)
                if file_format_name[0] == 'image':
                    files.append(t)
            except IsADirectoryError:
                pass
    #print(files, len(files), sep='\n')
    return files, roads
###############################################################################################


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
        decrypted_data = crypto.decrypt(text)
        decoded_data = decrypted_data.decode('utf-8')
        images_log = decoded_data.split(':')
        print(images_log)
        return images_log


def uploader(log_name, dir_name='/run/user/1000/gvfs/smb-share:server=freenas.local,share=disk/a'):
    try:
        dir_name = dir_name
        files_list = read_log(log_name)
        for file in files_list:
            route = file
            print(file)
            if route != '':
                try:
                    source = f'/home/pc/project5/photokeeper/{route}'
                    if os.path.exists(source):
                        result_path = os.path.join(dir_name, route)
                        print(result_path)
                        moving = shutil.move
                        moving(source, result_path)
                    else:
                        print('not')
                except OSError:
                    continue
                # except OSError:
                # files = []
                # files.append(file)
                # logging(files, 'Error_log.txt')
                # sys.exit("Не має доступу до цільової директорії")
                # pass
            else:
                pass
        if log_name == 'Error_log.txt':
            os.remove('Error_log.txt')
    except FileNotFoundError:
        pass


_route = pathlib.Path(__file__).parents[1]
log_name = 'log.txt'
sleep_time = 5


def image_check(files_path):
    try:
        file_format_name = magic.from_file(files_path, mime=True).split('/')
        return file_format_name
    except IsADirectoryError:
        pass


def image_seeker(images_route):
    images = []
    status = []
    dirs = []
    for file_names in images_route:
        file = str(file_names).split('/')[1]
        status.append(file)
    for file in status:
        img_name = file
        files_path = os.path.join(_route, img_name)
        root_dir = pathlib.Path(__file__).parents[0]
        is_dir = os.path.isdir(files_path)
        file_format = image_check(files_path)
        if str(files_path) != str(root_dir) and is_dir == True:
            dirs.append(files_path)

        if file_format is None:
            # print(files_path)
            continue
        file_type = file_format[0]
        if file_type == 'image':
            images.append(img_name)
    print(dirs)
    return images


def zipping_folder(addr, regime, name):
    print(addr)
    dir_route = pathlib.Path(addr).iterdir()
    with zipfile.ZipFile(name, f'{regime}') as archive:
        for file in dir_route:
            print(file)
            archive.write(file)


def zipping(data, regime, name='Archive.zip'):
    with zipfile.ZipFile(name, f'{regime}') as archive:
        for file in data:
            file_path = os.path.join('..', file)
            print(file_path)
            archive.write(file_path)


def main():
    uploader('Error_log.txt')
    try:
        while True:
            print('loop')
            program_route = pathlib.Path().iterdir()
            images_route = pathlib.Path('..').iterdir()
            time.sleep(sleep_time)
            status = []
            try:
                images, roads = new_seeker()
                print(roads)
                print(images)
                #print(images)
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
                        #print(images, current_number, log_number)
                        if current_number > log_number or current_number == 1:
                            difference = list(set(images) - set(images_log))
                            file_name = 'difference_log.txt'
                            archive_name = 'New.zip'
                            path_names = []
                            for names in roads:
                                print(names)
                                for n in difference:

                                    if n in names[1]:
                                        dir_name_path = names[0]
                                        if dir_name_path not in path_names:
                                            path_names.append(dir_name_path)
                                        else:
                                            pass
                                    else:
                                        pass
                            print(path_names)
                            logging(path_names, 'addres_log.txt')
                            for i in path_names:
                                print(type(i))
                                name = i.split('/')
                                zipping_folder(i, 'w', name=str(name[-1]+'.zip'))
                            if file_name not in status:
                                logging(difference, file_name)
                                zipping(difference, 'w', archive_name)
                                print('difference_list not found')
                            else:
                                logging(difference, file_name)
                                #print('ttt')
                                # zipping(difference, 'a', archive_name)
                                #uploader('difference_log.txt')
                        elif current_number <= log_number:
                            pass

                    except FileNotFoundError:
                        pass
            except FileNotFoundError:
                pass
            logging(images, log_name)
            #print(_route)
    except KeyboardInterrupt:
        print("Job ended!")
        logging(images, log_name)


if __name__ == '__main__':
    main()
