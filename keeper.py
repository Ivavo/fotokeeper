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
import ast

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
                'oxps',
                'flac'
                )


def new_seeker():
    route_root = pathlib.Path(__file__).parents[0]
    _route1 = pathlib.Path(__file__).parents[1]
    iteration_files = os.walk(_route1)
    dirs = []
    roads = []
    files = []
    for elements in iteration_files:
        if str(route_root) in str(elements[0]):
            continue
        else:
            images = []
            for i in elements[2]:
                resolution = i.split('.')[-1]
                if resolution in file_formats:
                    images.append(i)
            road = elements[0], images
            roads.append(road)
    for road_element in roads:
        dirs.append(road_element[0])
        for file in road_element[1]:
            file_path = os.path.join(road_element[0], file)
            try:
                file_format_name = magic.from_buffer(file_path, mime=True).split('/')
                file_resolution = file_path.split('.')[-1]
                if file_format_name[0] == 'image' or file_resolution in file_formats:
                    files.append(file)
            except IsADirectoryError:
                pass

    return files, roads, dirs


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


def uploader(archive_name = None, result_path = 'Y:\main'):
    sourse_road = pathlib.Path(__file__).parents[0]
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
sleep_time = 3


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


def archives_check(result_path):
    path_exist = os.path.exists(result_path)
    if path_exist == True:
        size1 = file_size_check()
        size2 = file_size_check(result_path)
        size_difference = set(size1) - set(size2)
        if len(size_difference) != 0:
            for archives in size_difference:
                name = archives[0]
                uploader(name, result_path)
        else:
            for i in size1:
                name = i[0]
                path = os.path.join(pathlib.Path(__file__).parents[0], name)
                os.remove(path)
    else:
        print('Result path not exist, check path')
        exit()


def bin_writer(text, name='settings.bin'):
    with open(name, 'wb')as settings:
        text_b = text.encode('utf-8')
        settings.write(text_b)


def bin_reader(bin_file='settings.bin'):
    with open(bin_file, 'rb')as settings:
        rb_text = settings.read()
        r_text = rb_text.decode('utf-8')
        return r_text


def main(result_path):
    global images
    archives_check(result_path)
    try:
        program_route = pathlib.Path().iterdir()
        status = []
        content = {}
        try:
            images, roads, dirs = new_seeker()
            for i in roads:
                i1 = i[1]
                content.update({i[0]: i1})
            p = str(content)
            for files in program_route:
                status.append(str(files))
            if 'settings.bin' not in status:
                bin_writer(result_path)
            else:
                pass
            r_path = bin_reader()
            if 'log1.bin' not in status or result_path != r_path or log_name not in status:
                bin_writer(result_path)
                bin_writer(str(content), 'log1.bin')
                logging(images, log_name)
                print('log_file not in directory making log file and archives!')
                for road in roads:
                    folder_path = str(road[0])
                    splited_string = folder_path.split(path_separator)
                    archives_name = (splited_string[-1] + '.zip')
                    zipping_folder(folder_path, 'w', archives_name)
                    logging(images, log_name)
                    uploader(result_path=result_path)
            elif log_name in status:
                try:
                    print(content)
                    print(type(content))
                    images_log = ast.literal_eval(bin_reader('log1.bin'))
                    if content != images_log:
                        for key in content:
                            name = key.split('\\')[-1]+'.zip'
                            current_content = content[key]
                            if key not in images_log and len(current_content) != 0:
                                zipping_folder(key, 'w', name)
                                bin_writer(str(content), 'log1.bin')
                            elif key in images_log:
                                log_content = images_log[key]
                                if current_content != log_content and len(current_content) != 0:
                                    #if len(current_content) < len(log_content) and os.environ['Less_archives_make'] == 1:
                                    #    zipping_folder(key, 'w', 'less_'+name)
                                    #    bin_writer(str(content), 'log1.bin')
                                    if len(current_content) < len(log_content):
                                        pass
                                    elif len(current_content) >= len(log_content):
                                        zipping_folder(key, 'w', name)
                                        bin_writer(str(content), 'log1.bin')

                                else:
                                    bin_writer(str(content), 'log1.bin')
                                    pass
                    else:
                        bin_writer(str(content), 'log1.bin')
                        pass
                    #images_log = read_log(log_name)
                    #log_number = len(images_log)
                    #current_number = len(images)
#
                    #if images_log != images:
                    #    difference = list(set(images) - set(images_log))
                    #    file_name = 'difference_log.txt'
                    #    logging(images, log_name)
#
                    #    if current_number > log_number or current_number == 1:
                    #        archive_sort(roads, difference)
#
                    #        if file_name not in status:
                    #            logging(difference, file_name)
                    #        else:
                    #            logging(difference, file_name)
#
                    #    elif current_number == log_number:
                    #        difference = list(set(images) - set(images_log))
                    #        archive_sort(roads, difference)
#
                    #    elif current_number < log_number:
                    #        logging(images, log_name)
                    #        pass
#
                    #else:
                    #    pass
#
                except FileNotFoundError:
                    pass

        except FileNotFoundError:
            pass
            logging(images, log_name)
    except KeyboardInterrupt:
        print("Job ended!")
        logging(images, log_name)


if __name__ == '__main__':
    main('Y:\main')
