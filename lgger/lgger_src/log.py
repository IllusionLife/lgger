from enum import Enum
from datetime import datetime
from time import time
from typing import Optional, Callable

from lgger.lgger_src.misc import normalize_dir
from lgger.lgger_src.conf import LogConf


class LogLvl(Enum):
    DEBUG = 0
    INFO = 1
    WARNING = 2
    ERROR = 3
    FATAL = 4


class LggerException(Exception):
    def __init__(self, exc_message):
        super().__init__(exc_message)
        log(exc_message, LogLvl.FATAL)


class Lgger(LogConf):
    def __init__(self, filename=None, filepath=None):
        super().__init__()
        self.default_loglvl = LogLvl(self.get_config('default_log_level', LogLvl.INFO.value))
        if not filename:
            filename = f"{self.get_config('default_filename', '').rstrip('.')}." \
                       f"{self.get_config('default_file_extension', '').lstrip('.')}"
            if not filename:
                raise LggerException("No log name provided and no default found.")
        if not filepath:
            filepath = normalize_dir(self.get_config('default_log_folder', './logs'))
            if not filepath:
                raise LggerException("No log folder provided and no default found.")

        self.open_log(filepath, filename, enc=self.get_config('log_encoding', 'utf-8'))

    def __stringify(self, obj):
        msg_string = obj
        if type(obj).__str__ is object.__str__:
            if type(obj).__repr__ is object.__repr__:
                raise LggerException(f'Type {type(obj)} has no string representation available.')
            msg_string = obj.__repr__()
        return msg_string

    def __log_prefix(self, loglvl: LogLvl):
        if not loglvl:
            loglvl = self.default_loglvl
        return f"{datetime.now().strftime(self.get_config('datetimeformat', '%Y/%m/%d %H:%M:%S'))} [{loglvl.name.center(7)}]"

    def __log(self, msg, lvl, *args):
        msg_string = self.__stringify(msg) + ','.join([self.__stringify(x) for x in args])
        self.write_file(f"{self.__log_prefix(lvl)} - {msg_string}\n")

    def log(self, msg, lvl: Optional[LogLvl] = None, *args):
        if not lvl:
            self.__log(msg, self.default_loglvl, *args)
        else:
            self.__log(msg, lvl, *args)

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


default_log: Optional[Lgger] = None


def create_log(filename=None, filepath=None):
    global default_log
    log_var = Lgger(filename, filepath)
    if not default_log:
        default_log = log_var
    return log_var


def get_global_log():
    return default_log


def log(msg, lvl=None, *args):
    global default_log
    if not default_log:
        default_log = Lgger()
    default_log.log(msg, lvl, *args)


def resolve_template():
    default_log.resolve_template()


def time_performance(func: Callable):
    def time_performance_wrapper(*args, **kwargs):
        before_func = time()
        res = func(*args, **kwargs)
        after_func = time()
        log(f"Function {func.__name__} took {(after_func - before_func):6f} seconds")
        return res

    return time_performance_wrapper


def log_args(func: Callable):
    def log_args_wrapper(*args, **kwargs):
        stringified = "\n*** Args: " + ", ".join([str(x) for x in args])
        stringified += "\n*** Kwargs: " + ", ".join([f"{str(k)} = {str(v)}" for k, v in kwargs.items()])
        log(f"Function {func.__name__} has the following arguments:{stringified}")
        return func(*args, **kwargs)

    return log_args_wrapper

def log_return(func: Callable):
    def log_return_wrapper(*args, **kwargs):
        res = func(*args, **kwargs)
        try:
            log(f"Function {func.__name__} returned:", None, res)
        except LggerException as exc:
            raise LggerException(f"Error during logging of return of function {func.__name__}.")
        return res

    return log_return_wrapper
