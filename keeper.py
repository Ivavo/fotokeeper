# -*- coding: utf-8 -*-
import os
import zipfile
import pathlib
import shutil

from cryptography.fernet import Fernet
from sys import platform
import ast

path_separator = None
if platform == 'win32':
    path_separator = '\\'
elif platform == 'linux' or platform == 'linux2':
    path_separator = '/'

settings_name = 'settings.bin'
adr_log_bin = 'adr_log.bin'
log_name = 'log.bin'
sleep_time = 3
message = None

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
)


def new_seeker(current_route=pathlib.Path(__file__).parents[1]):
    route_root = pathlib.Path(__file__).parents[0]
    dirs = []
    roads = []
    files = []
    iteration_files = os.walk(current_route)
    for elements in iteration_files:
        if str(route_root) in str(elements[0]):
            pass
        else:
            buffer_list = []
            for element in elements[2]:
                resolution = element.split('.')[-1]
                if resolution in file_formats:
                    buffer_list.append(element)
            road = elements[0], buffer_list
            roads.append(road)
    for road_element in roads:
        dirs.append(road_element[0])
        for file in road_element[1]:
            file_path = os.path.join(road_element[0], file)
            try:
                file_resolution = file_path.split('.')[-1]
                if file_resolution in file_formats:
                    files.append(file)
            except IsADirectoryError:
                pass
    return files, roads, dirs


def write_key():
    key = Fernet.generate_key()
    with open('config.bin', 'wb') as key_file:
        key_file.write(key)


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


def read_log(file_name):
    key = load_key()
    crypto = Fernet(key)
    with open(file_name, 'rb') as log:
        text = log.read()
        decrypted_data = crypto.decrypt(text)
        decoded_data = decrypted_data.decode('utf-8')
        images_log = decoded_data.split(':')
        return images_log


def uploader(archive_name=None, result_path='Y:\\main'):
    source_road = pathlib.Path(__file__).parents[0]
    if archive_name is None:
        archives = []
        program_route = pathlib.Path(source_road).iterdir()
        path_exist = os.path.exists(result_path)
        if path_exist is True:
            for i in program_route:
                if '.zip' in str(i):
                    archives.append(str(i))
            for archive in archives:
                path_to_file = os.path.join(source_road, archive)
                os.environ['Size'] = os.path.getsize(path_to_file)
                os.environ['File_Name'] = os.path.join(result_path, archive)
                shutil.copy(path_to_file, result_path)
        else:
            print('Error the required path is not found!')
    else:
        path_to_archive = os.path.join(source_road, archive_name)
        size = os.path.getsize(archive_name)
        os.environ['Size'] = str(size)
        os.environ['File_Name'] = os.path.join(result_path, archive_name)
        shutil.copy(path_to_archive, result_path)


def file_size_check(address=pathlib.Path(__file__).parents[0]):
    sizes = []
    program_route = pathlib.Path(address).iterdir()
    for i in program_route:
        name = os.path.split(i)[-1]
        if '.zip' in str(i):
            file_size_abs = os.path.getsize(i)
            file_size = file_size_abs // 1024
            size = (name, file_size)
            sizes.append(size)
    return sizes


def size_check(name=None):
    file_size_bit = 0
    path_exist = os.path.exists(name)
    if name is None or not path_exist:
        pass
    else:
        file_size_bit = os.path.getsize(name)
    return file_size_bit


def zipping_images_folder(addr, regime, name):
    dir_route = pathlib.Path(addr).iterdir()
    with zipfile.ZipFile(name, f'{regime}') as archive:
        for file in dir_route:
            file = str(file)
            try:
                file_res = file.split('.')[-1]
                if file_res in file_formats:
                    message = str(f'Створюється архів {name}')
                    archive.write(file)
                else:
                    pass
            except IsADirectoryError:
                continue


def make_fine_list(size2):
    names = []
    for items in size2:
        string = str(items[0])
        size = str(items[1] / 1024)
        item = string + ': - ' + size + ' Mb;'
        names.append(item)
    return names

def error_writer(text):
    with open('error.txt', 'w')as errors:
        errors.write(text)


def archives_check(result_path):
    path_exist = os.path.exists(result_path)

    if path_exist is True:
        size1 = file_size_check()
        size2 = file_size_check(result_path)
        names = make_fine_list(size2)
        os.environ['Images'] = '\n'.join(names)
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
        global message
        message = str('Шлях вказано не вірно!')
        error_writer(message)
        raise Exception('Not correct path!')



def bin_writer(text, name='settings.bin'):
    with open(name, 'wb')as settings:
        text_b = text.encode('utf-8')
        settings.write(text_b)


def bin_reader(bin_file='settings.bin'):
    with open(bin_file, 'rb')as settings:
        rb_text = settings.read()
        r_text = rb_text.decode('utf-8')
        return r_text


def event_cach(content, images_log):
    if content != images_log:
        for key in content:
            name = key.split('\\')[-1] + '.zip'
            current_content = content[key]
            if key not in images_log and len(current_content) != 0:
                zipping_images_folder(key, 'w', name)
                bin_writer(str(content), adr_log_bin)
            elif key in images_log:
                log_content = images_log[key]
                if current_content != log_content and len(current_content) != 0:
                    # if len(current_content) < len(log_content) and os.environ['Less_archives_make'] == 1:
                    #    zipping_folder(key, 'w', 'less_'+name)
                    #    bin_writer(str(content), 'log1.bin')
                    if len(current_content) < len(log_content):
                        pass
                    elif len(current_content) >= len(log_content):
                        zipping_images_folder(key, 'w', name)
                        bin_writer(str(content), adr_log_bin)
                else:
                    bin_writer(str(content), adr_log_bin)
                    pass
    else:
        bin_writer(str(content), adr_log_bin)
        pass


def main(result_path):
    archives_check(result_path)
    images = []
    try:
        program_route = pathlib.Path().iterdir()
        status = []
        content = {}
        try:
            images, roads, dirs = new_seeker()
            for road in roads:
                content.update({road[0]: road[1]})
            for files in program_route:
                status.append(str(files))
            if settings_name not in status:
                bin_writer(result_path)
            else:
                pass
            r_path = bin_reader()
            if adr_log_bin not in status or result_path != r_path or log_name not in status:
                bin_writer(result_path)
                bin_writer(str(content), adr_log_bin)
                logging(images, log_name)
                message = 'Log file not in directory making log file and archives!'
                for road in roads:
                    folder_path = str(road[0])
                    splited_string = folder_path.split(path_separator)
                    archives_name = (splited_string[-2] + '-' + splited_string[-1] + '.zip')
                    zipping_images_folder(folder_path, 'w', archives_name)
                    logging(images, log_name)
                    uploader(archives_name, result_path)
            elif log_name in status:
                try:
                    images_log = ast.literal_eval(bin_reader(adr_log_bin))
                    event_cach(content, images_log)
                except FileNotFoundError:
                    pass

        except FileNotFoundError:
            pass
            logging(images, log_name)
    except KeyboardInterrupt:
        logging(images, log_name)


#if __name__ == '__main__':
#    main()
