from os import environ, getcwd
from os.path import dirname
from datetime import datetime

from lgger.lgger_src.misc import normalize_dir

# Templates
environ["LGGER_CONF_TMPL"] = "lgger.conf.template"
environ["LGGER_TMPL"] = normalize_dir(f"{dirname(__file__) + '/templates'}")


# Templates - Configuration file creation
environ["LGGER_CWD"] = normalize_dir(getcwd())
environ["LGGER_LOG_NAME"] = environ.get("LGGER_LOG_NAME", f'log_{datetime.now().strftime("%Y-%m-%d")}')
environ["LGGER_LOG_EXTN"] = environ.get("LGGER_LOG_EXTN", ".log")
environ["LGGER_LOG_DIR"] = environ.get("LGGER_LOG_DIR", "./logging")
environ["LGGER_ENC"] = environ.get("LGGER_ENC", "utf-8")
environ["LGGER_TIMESTAMP_FORMAT"] = environ.get("LGGER_TIMESTAMP_FORMAT", "%Y-%b-%d %H:%M:%S:%f")
