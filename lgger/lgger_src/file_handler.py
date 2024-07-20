from _io import TextIOWrapper
from typing import Optional
from os import makedirs
from os.path import isdir, isfile

import lgger.lgger_src.misc as misc

FILE_READ = 'r'
FILE_CREATE = 'w'
FILE_APPEND = 'a+'


class FileLogException(Exception):
    def __init__(self, err, reason: Optional[Exception] = None):
        self.__error = err
        self.__reason = reason

    def __stringify_exception(self):
        err_msg = f"Error:'{self.__error}'"
        if self.__reason:
            err_msg += f"\nReason:'{self.__reason}'"
        return err_msg

    def __repr__(self):
        return self.__stringify_exception()

    def __str__(self):
        return self.__stringify_exception()


class FileLog:
    def __init__(self):
        self.__file_mode: Optional[str] = None
        self.__log_fp: Optional[TextIOWrapper] = None
        self.__log_dir: Optional[str] = None
        self.__log_name: Optional[str] = None

    def __del__(self):
        if self.__log_fp:
            self.__log_fp.close()

    def clean_file(self):
        if self.__file_mode != FILE_READ:
            self.__log_fp.seek(0)
            self.__log_fp.truncate()
        else:
            raise FileLogException("Cannot clean file in READ mode.")

    def is_log_open(self):
        if self.__log_fp:
            return True
        return False

    def close_log(self):
        self.__log_fp.close()

    def open_log(self, log_dir: str, log_name: str, access_mode: str = FILE_CREATE, enc: str = 'utf-8'):
        try:
            self.__log_dir = misc.normalize_dir(log_dir)
            try:
                if not isdir(self.__log_dir):
                    makedirs(self.__log_dir)
            except OSError:
                raise FileLogException(f'Cannot create directory: {self.__log_dir}.')

            if access_mode == FILE_CREATE:
                self.__log_name = misc.normalize_filename(self.__log_dir, log_name)
            else:
                if not isfile(self.__log_dir + log_name):
                    raise FileLogException(f'File {self.__log_dir + log_name} not found.')
                self.__log_name = log_name

            if access_mode == FILE_READ and not isfile(self.__log_dir + log_name):
                self.__log_fp = open(self.__log_dir + self.__log_name, 'w')
                self.__log_fp.close()

            self.__log_fp = open(self.__log_dir + self.__log_name, access_mode, encoding=enc)
            self.__file_mode = access_mode
        except FileLogException as fe:
            raise fe
        except Exception as e:
            raise FileLogException(f"Unable to open file.\nDir:{self.__log_dir} File:{self.__log_name}", e)

    def write_file(self, log_msg: str):
        try:
            if not self.is_log_open():
                raise FileLogException("No open file.")
            self.__log_fp.write(log_msg)
        except Exception as e:
            raise FileLogException(f"Unable to write in file.\nDir:{self.__log_dir} File:{self.__log_name}", e)

    def read_file(self):
        try:
            if not self.is_log_open():
                raise FileLogException("No open file.")
            return self.__log_fp.readlines()
        except Exception as e:
            raise FileLogException(f"Unable to read from file.\nDir:{self.__log_dir} File:{self.__log_name}", e)