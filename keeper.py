import os
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
    for elements in iteration_files:
        if str(route_root) in str(elements[0]):
            continue
        else:
            road = elements[0], elements[2]
            roads.append(road)
    for road_element in roads:
        for file in road_element[1]:
            file_path = os.path.join(road_element[0], file)

            try:
                file_format_name = magic.from_file(file_path, mime=True).split('/')
                if file_format_name[0] == 'image':
                    files.append(file)
            except IsADirectoryError:
                pass
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


def archives_upload(name, addr='/run/user/1000/gvfs/smb-share:server=freenas.local,share=disk/a'):
    path_exist = os.path.exists(addr)
    if path_exist == True:
        print()


#def uploader(log_name, dir_name='/run/user/1000/gvfs/smb-share:server=freenas.local,share=disk/a'):
#    path_exist = os.path.exists('/run/user/1000/gvfs/smb-share:server=freenas.local,share=disk/a')
#    if path_exist == True:
#        try:
#            dir_name = dir_name
#            files_list = read_log(log_name)
#            for file in files_list:
#                route = file
#                print(file)
#                if route != '':
#                    try:
#                        source = f'/home/pc/project5/photokeeper/{route}'
#                        if os.path.exists(source):
#                            result_path = os.path.join(dir_name, route)
#                            print(result_path)
#                            moving = shutil.move
#                            moving(source, result_path)
#                        else:
#                            print('not')
#                    except OSError:
#                        continue
#                    # except OSError:
#                    # files = []
#                    # files.append(file)
#                    # logging(files, 'Error_log.txt')
#                    # sys.exit("Не має доступу до цільової директорії")
#                    # pass
#                else:
#                    pass
#            if log_name == 'Error_log.txt':
#                os.remove('Error_log.txt')
#        except FileNotFoundError:
#            pass
#    else:
#        print('Upload directory is not found')


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
            continue
        file_type = file_format[0]
        if file_type == 'image':
            images.append(img_name)
    print(dirs)
    return images


def zipping_folder(addr, regime, name):
    dir_route = pathlib.Path(addr).iterdir()
    with zipfile.ZipFile(name, f'{regime}') as archive:
        for file in dir_route:
            try:
                file_format_name = magic.from_file(str(file), mime=True).split('/')
                file_format = file_format_name[0]
                if file_format == 'image':
                    archive.write(file)
                else:
                    pass
            except IsADirectoryError:
                continue


def zipping(data, regime, name='Archive.zip'):
    with zipfile.ZipFile(name, f'{regime}') as archive:
        for file in data:
            file_path = os.path.join('..', file)
            print(file_path)
            archive.write(file_path)


def main():
    global images
    try:
        while True:
            print('loop')
            program_route = pathlib.Path().iterdir()
            images_route = pathlib.Path('..').iterdir()
            time.sleep(sleep_time)
            status = []
            try:
                images, roads = new_seeker()
                for files in program_route:
                    status.append(str(files))
                if log_name not in status:
                    logging(images, log_name)
                    print('log_file not in directory making log file and archive!')
                    for road in roads:
                        folder_path = str(road[0])
                        splited_string = folder_path.split('/')
                        archives_name = (splited_string[-1] + '.zip')
                        print(archives_name)
                        zipping_folder(folder_path, 'w', archives_name)
                elif log_name in status:
                    try:
                        images_log = read_log(log_name)
                        log_number = len(images_log)
                        current_number = len(images)
                        if current_number > log_number or current_number == 1:
                            difference = list(set(images) - set(images_log))
                            file_name = 'difference_log.txt'
                            path_names = []
                            for names in roads:
                                for n in difference:
                                    if n in names[1]:
                                        dir_name_path = names[0]
                                        if dir_name_path not in path_names:
                                            path_names.append(dir_name_path)
                                        else:
                                            pass
                                    else:
                                        pass
                            logging(path_names, 'addres_log.txt')
                            for i in path_names:
                                name = i.split('/')
                                zipping_folder(i, 'w', name=str(name[-1] + '.zip'))
                            if file_name not in status:
                                logging(difference, file_name)
                            else:
                                logging(difference, file_name)
                        elif current_number <= log_number:
                            pass

                    except FileNotFoundError:
                        pass
            except FileNotFoundError:
                pass
            logging(images, log_name)
    except KeyboardInterrupt:
        print("Job ended!")
        logging(images, log_name)


if __name__ == '__main__':
    main()
