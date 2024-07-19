from enum import Enum
from os import getcwd
from datetime import datetime
from time import time
from typing import Optional, Callable

from lgger.logger_src.misc import normalize_dir
from lgger.logger_src.conf import LogConf


class LogLvl(Enum):
    DEBUG = 0
    INFO = 1
    WARNING = 2
    ERROR = 3
    FATAL = 4


class Logger(LogConf):
    def __init__(self, filename=None, filepath=None):
        super().__init__()
        self.default_loglvl = LogLvl(self.get_config('default_log_level', LogLvl.INFO.value))
        if not filename:
            filename = self.get_config('default_filename') + self.get_config('default_file_extension')
        if not filepath:
            filepath = normalize_dir(getcwd()) + self.get_config('default_log_folder', 'logs')
        self.open_log(filepath, filename, enc=self.get_config('log_encoding', 'utf-8'))

    def __log_prefix(self, loglvl: LogLvl = None):
        if not loglvl:
            loglvl = self.default_loglvl
        return f"{datetime.now().strftime(self.get_config('datetimeformat', '%Y/%m/%d %H:%M:%S'))} [{loglvl.name.center(7)}]"

    def __log(self, msg, lvl):
        self.write_file(f"{self.__log_prefix(lvl)} - {msg}\n")

    def log(self, msg, lvl=None):
        if not lvl:
            self.__log(msg, lvl)
        else:
            self.__log(msg, self.default_loglvl)

    def log_debug(self, msg):
        self.__log(msg, LogLvl.DEBUG)

    def log_info(self, msg):
        self.__log(msg, LogLvl.INFO)

    def log_warn(self, msg):
        self.__log(msg, LogLvl.WARNING)

    def log_error(self, msg):
        self.__log(msg, LogLvl.ERROR)

    def log_fatal(self, msg):
        self.__log(msg, LogLvl.FATAL)


default_log: Optional[Logger] = None


def create_log(filename=None, filepath=None):
    global default_log
    log_var = Logger(filename, filepath)
    if not default_log:
        default_log = log_var
    return log_var


def get_global_log():
    return default_log


def log(msg, lvl=None):
    global default_log
    if not default_log:
        default_log = Logger()
    default_log.log(msg, lvl)


def time_performance(func: Callable):
    def time_performance_wrapper(*args, **kwargs):
        before_func = time()
        res = func(*args, **kwargs)
        after_func = time()
        log(f"Function {func.__name__} took {(after_func - before_func):5f} seconds")
        return res

    return time_performance_wrapper


def log_args(func: Callable):
    def log_args_wrapper(*args, **kwargs):
        stringified = "\n*** Args: " + ", ".join([str(x) for x in args])
        stringified += "\n*** Kwargs: " + ", ".join([f"{str(k)} = {str(v)}" for k, v in kwargs.items()])
        log(f"Function {func.__name__} has the following arguments:{stringified}")
        return func(*args, **kwargs)

    return log_args_wrapper
