import os
import time
import magic
import json
import zipfile
import pathlib


def logging(data, file_name):
    with open(file_name, 'w') as log:
        json.dump(data, log)


def read_log(file_name):
    with open(file_name, 'r+') as log:
        images_log = json.load(log)
        return images_log


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
            continue
        file_type = file_format[0]
        if file_type == 'image':
            images.append(img_name)
    return images


_route = pathlib.Path(__file__).parents[1]

k = 0
log_name = 'log.json'
while True:
    program_route = pathlib.Path().iterdir()
    images_route = pathlib.Path('..').iterdir()
    time.sleep(3)
    k += 1
    print('---------------------------------', k)

    status = []
    images = image_seeker(images_route)
    print(images)
    for files in program_route:
        status.append(str(files))
    if log_name not in status:
        logging(images, log_name)
    elif log_name in status:
        try:
            images_log = read_log(log_name)
            log_number = len(images_log)
            current_number = len(images)
            if log_number < current_number:
                difference = list(set(images) - set(images_log))
                if 'difference_log.json' not in status:
                    logging(difference, "difference_log.json")
                else:
                    logging(difference, "difference_log.json")
            else:
                continue
        except Exception:
            continue

    logging(images, log_name)
