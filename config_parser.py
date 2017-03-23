import configparser
from configparser import RawConfigParser
import os.path
import os
from os.path import expanduser

HOME = expanduser('~')


def read_file(name):
    name = os.path.join(HOME, name)
    config = RawConfigParser()
    config.read(name)
    try:
        save_path = config.get("DIRECTORY",
                               "Download_Path")
    except configparser.NoSectionError:
        print('Could not read configuration file')
    return save_path


def change_to_main_manga_dir(main_dir):
    new_path = os.path.join(HOME, main_dir)
    if not os.path.exists(new_path):
        os.makedirs(new_path)

    os.chdir(new_path)
    return new_path


def change_to_manga_dir(manga_dir, manga_name, chapter):
    new_path = os.path.join(HOME, manga_dir, manga_name)
    if not os.path.exists(new_path):
        os.makedirs(new_path)
    if not os.path.exists(os.path.join(new_path,
                                       manga_name + "-" + chapter)):
        os.makedirs(os.path.join(new_path,
                                 manga_name + "-" + chapter))

    os.chdir(os.path.join(new_path,
                          manga_name + "-" + chapter))
