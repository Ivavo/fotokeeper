#-*- coding: utf-8 -*-
import os
import time
import magic
import zipfile
import pathlib
import shutil
from cryptography.fernet import Fernet
from sys import platform
from tqdm import tqdm


path_separator = None
if platform == 'win32':
    path_separator = '\\'
elif platform == 'linux' or platform == 'linux2':
    path_separator = '/'



file_formats = (
                'bmp',
                'dib',
                'rle',
                'gif',
                'iff',
                'lbm',
                'bbm',
                'ilbm',
                'pic',
                'jpeg',
                'jpg',
                'JPEG',
                'jPG',
                'sid',
                'pcx',
                'pcc',
                'png',
                'psd',
                'tif',
                'tiff',
                'jxr',
                'hdp',
                'wdp',
                'webp',
                'xbm',
                'xps',
                'oxps'
                )


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
                file_format_name = magic.from_buffer(file_path, mime=True).split('/')
                file_resolution = file_path.split('.')[-1]
                if file_format_name[0] == 'image' or file_resolution in file_formats:
                    files.append(file)
            except IsADirectoryError:
                pass
    return files, roads


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
        return images_log


def uploader(archive_name = None, result_path ='Z:\dataset1'):
    sourse_road = pathlib.Path(__file__).parents[0]
    result_path = os.path.join('Z:\dataset1')
    if archive_name == None:
        archives = []
        program_route = pathlib.Path(sourse_road).iterdir()
        path_exist = os.path.exists(result_path)
        if path_exist == True:
            for i in program_route:
                if '.zip' in str(i):
                    archives.append(str(i))
            for archive in archives:
                path_to_file = os.path.join(sourse_road, archive)
                shutil.copy(path_to_file, result_path)
        else:
            print('error')
    else:
        path_to_archive = os.path.join(sourse_road, archive_name)
        print(path_to_archive)
        shutil.copy(path_to_archive, result_path)


_route = pathlib.Path(__file__).parents[1]
log_name = 'log.txt'
sleep_time = 5


def file_size_check(addr=pathlib.Path(__file__).parents[0]):
    sizes = []
    program_route = pathlib.Path(addr).iterdir()
    for i in program_route:
        name = os.path.split(i)[-1]
        if '.zip' in str(i):
           file_size_abs = os.path.getsize(i)
           file_size = file_size_abs // 1024
           size = (name, file_size)
           sizes.append(size)
    return sizes


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
        for file in tqdm(dir_route):
            file = str(file)
            try:
                file_res = file.split('.')[-1]
                if file_res in file_formats:
                    archive.write(file)
                    print(file)
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


def archive_sort(roads, difference):
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
        splited_path = i.split(path_separator)
        name = splited_path[-1] + '.zip'
        zipping_folder(i, 'w', name=name)
        uploader(name)
        print(name)



def main():
    global images
    result_path = os.path.join('Z:\dataset1')
    path_exist = os.path.exists(result_path)
    if path_exist == True:
        size1 = file_size_check()
        size2 = file_size_check(result_path)
        size_difference = set(size1) - set(size2)
        if len(size_difference) != 0:
            for archives in size_difference:
                name = archives[0]
                uploader(name)
        else:
            for i in size1:
                name = i[0]
                path = os.path.join(pathlib.Path(__file__).parents[0], name)
                os.remove(path)
                print(path)
    else:
        print('Result path not exist, check path')
        exit()
    try:
        while True:
            print('loop')
            program_route = pathlib.Path().iterdir()
            time.sleep(sleep_time)
            status = []
            try:
                images, roads = new_seeker()
                for files in program_route:
                    status.append(str(files))
                if log_name not in status:
                    logging(images, log_name)
                    print('log_file not in directory making log file and archives!')
                    for road in roads:
                        folder_path = str(road[0])
                        splited_string = folder_path.split(path_separator)
                        archives_name = (splited_string[-1] + '.zip')
                        zipping_folder(folder_path, 'w', archives_name)
                        uploader()
                elif log_name in status:
                    try:
                        images_log = read_log(log_name)
                        log_number = len(images_log)
                        current_number = len(images)
                        if images_log != images:
                            difference = list(set(images) - set(images_log))
                            file_name = 'difference_log.txt'
                            print(difference)
                            if current_number > log_number or current_number == 1:
                                archive_sort(roads, difference)
                                if file_name not in status:
                                    logging(difference, file_name)
                                else:
                                    logging(difference, file_name)
                            elif current_number == log_number:
                                difference = list(set(images) - set(images_log))
                                archive_sort(roads, difference)
                            elif current_number < log_number:
                                pass
                        else:
                            pass
                    except FileNotFoundError:
                        pass
            except FileNotFoundError:
                pass
            logging(images, log_name)
    except KeyboardInterrupt:
        print("Job ended!")
        logging(images, log_name)


#if __name__ == '__main__':
#    start_check()
