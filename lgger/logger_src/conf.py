from os import environ, getcwd
from lgger.logger_src.file_handler import FileLog, FILE_READ, FILE_APPEND
from lgger.logger_src.misc import normalize_dir, valid_number


class LogConf(FileLog):
    def __init__(self):
        super().__init__()
        self.__conf_dir = environ.get('LOGGER_CONF_DIR', environ.get('GLOBAL_CONF_DIR', f"{normalize_dir(getcwd())}/conf"))
        self.__conf_file = environ.get('LOGGER_CONF_FILE', environ.get('GLOBAL_CONF_DIR', 'logger.conf'))
        self.open_log(self.__conf_dir, self.__conf_file, FILE_READ)
        self.data = {conf.split('=')[0].strip(): conf.split('=')[1].strip() for conf in self.read_file()}
        for conf_name, conf_val in self.data.items():
            temp = valid_number(conf_val)
            if temp:
                self.data[conf_name] = temp
        self.has_change = False

    def __del__(self):
        if self.has_change:
            self.close_log()
            self.open_log(self.__conf_dir, self.__conf_file, FILE_APPEND)
            self.clean_file()
            for conf_name, conf_val in self.data.items():
                if valid_number(conf_val):
                    conf_val = valid_number(conf_val)
                self.write_file(f"{conf_name}={conf_val}\n")

    def get_config(self, conf_name, default=None):
        return self.data.get(conf_name, default)

    def set_config(self, conf_name, conf_value):
        self.data[conf_name] = conf_value
        self.has_change = True
