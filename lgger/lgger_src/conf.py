from os import environ, getcwd, mkdir
from os.path import isdir, isfile, dirname
from re import findall

from lgger.lgger_src.file_handler import FileLog, FILE_READ, FILE_APPEND
from lgger.lgger_src.misc import normalize_dir, valid_number


class LogConf(FileLog):
    def __init__(self):
        super().__init__()
        self.__conf_dir = f"{environ.get('LGGER_CWD', getcwd())}/config"
        if not isdir(self.__conf_dir):
            self.__conf_dir = environ.get('LGGER_CONF_DIR')
        self.__conf_file = environ.get('LGGER_CONF_FILE', 'lgger.conf')
        if not isfile(normalize_dir(self.__conf_dir) + self.__conf_file) \
                and not isfile(normalize_dir(environ.get('LGGER_CONF_DIR')) + self.__conf_file):
            print("Configuration file not found. Creating new configuration file based on template.")
            self.__conf_dir = normalize_dir(f"{environ.get('LGGER_CWD', getcwd())}/config")
            if not isdir(self.__conf_dir):
                mkdir(self.__conf_dir)
            self.resolve_template()
        self.open_log(self.__conf_dir, self.__conf_file, FILE_READ)
        self.data = {conf.split('=')[0].strip(): conf.split('=')[1].strip() for conf in self.read_file()}
        for conf_name, conf_val in self.data.items():

            temp = valid_number(conf_val)
            if temp:
                self.data[conf_name] = temp
            elif isdir(conf_val):
                self.data[conf_name] = normalize_dir(conf_val)
        self.has_change = False

    def __del__(self):
        if self.has_change:
            self.close_log()
            self.open_log(self.__conf_dir, self.__conf_file, FILE_APPEND)
            self.clean_file()
            for conf_name, conf_val in self.data.items():
                self.write_file(f"{conf_name}={conf_val}\n")

    def get_config(self, conf_name, default=None):
        return self.data.get(conf_name, default)

    def set_config(self, conf_name, conf_value):
        self.data[conf_name] = conf_value
        self.has_change = True

    def resolve_template(self):
        conf_tmpl_dir = environ["LGGER_TMPL"]
        conf_tmpl_file = environ['LGGER_CONF_TMPL']
        if not isfile(conf_tmpl_dir + conf_tmpl_file):
            print(conf_tmpl_dir + conf_tmpl_file)
            raise Exception("Configuration template file not found. Cannot create log file/")
        self.open_log(self.__conf_dir, self.__conf_file)
        read_tmpl = FileLog()
        read_tmpl.open_log(conf_tmpl_dir
                           , conf_tmpl_file
                           , FILE_READ)
        pass

        for line in read_tmpl.read_file():
            env_var_name = findall("(?<=\$\{).+?(?=\})", line)[0]
            self.write_file(line.replace(f"${{{env_var_name}}}", environ.get(env_var_name, '')))
        read_tmpl.close_log()
        self.close_log()