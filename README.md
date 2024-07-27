# Lgger - A simple package for logging

![Lgger background](./lgger/img/lgger_background.png "Lgger background image")

A simple logging package, aimed to help with writing log files. This is the first 
package, that I have ever created and is to be used in future projects of mine.

Any ideas for improvements and criticism is welcomed.

## Setup:
As a lazy person, the setup is one of the more unpleasant parts of each
project. This is why I have made this package to work with minimal setup required.
All that needs to be done is to install the package and import it.

Using pip:
```
pip install git+https://github.com/IllusionLife/lgger.git
```

When used, the package will set temporary enviromental variables, which 
can be overwritten for customization. Those enviromental variables are
intended to create a configuration file by using the [Lgger template] file.

The enviromental variables are being set in the [env file] and here is the list
of what each variable is being used for:

| Env variable           | Config variable         |                      Intended use                       | Changable |           Default value            |
|------------------------|:------------------------|:-------------------------------------------------------:|:---------:|:----------------------------------:|
| LGGER_TMPL             |                         |             Stores to the templates folder              |           |   ${package_dir}/lgger/templates   |
| LGGER_CONF_TMPL        |                         |      Stores the name of Lgger config template file      |           |        lgger.conf.template         |
| LGGER_LOG_NAME         | default_filename        | Default log name if none is being provided in the code. |     Y     |     log_%Y-%m-%d `date format`     |
| LGGER_LOG_EXTN         | default_file_extension  |               Default log file extention.               |     Y     |                .log                |
| LGGER_LOG_DIR          | default_log_folder      |                 Default log directory.                  |     Y     |             ./logging              |
| LGGER_ENC              | log_encoding            |                  Default log encoding.                  |     Y     |               utf-8                |
| LGGER_TIMESTAMP_FORMAT | datetimeformat          |           Log timestamp, used inside the log.           |     Y     | %Y-%b-%d %H:%M:%S:%f `date format` |
| LGGER_CWD              |                         |          Stores the current working directory.          |           |            ${getcwd()}             |

If you need to change the default values, you can either:
* change the `${LGGER_LOG_DIR}/lgger.conf` file directly
  (if the .conf file is created already).
* or change the env variables and create the configuration file
  * After setting the variables, you can delete the old configuration file
    and create a `Lgger()` object or use the `log(msg)` function, which
    will create the conf file automatically.
  * or call `resolve_template()`, which will do the same as above.

## How to use:
After installing and importing the package, you can use the `log(msg)` directly, which
will create a log file according to the configuration file mentioned above.
You can also create a custom log file by creating a `Lgger()` object. I will provide demonstrations
for both here:

### Using `log(msg, lvl=None, *args)`

Too lazy to create, store and handle a `Lgger()` object? Then don't.
By calling log("Your message"), the package will create a log folder
in your pre-configured directory (by default
the current working directory) in a separate folder.
```
import lgger

lgger.log("Hello World!")
```

You can also select a log level/severity and add any additional parameters to
be printed at the end of the log message. For more info on the log severity, please
check the [Log level / Severity] section.
```
import lgger

lgger.log("This is an error!", LogLvl.ERROR)
lgger.log("string", LogLvl.DEBUG, {more: "data"})
```

### Using the `create_log(filename, filepath)` function

If you want to create a `Lgger()` object, that writes in a different
folder or has a different filename, then this is what you should use.

This will create an object, assign it as the default logger for the
current session and run any `log(msg)` from this object. This is the recommended
way to create a `Lgger()` object.

The function takes a number of optional parameters:
  * `filename: str` - Name of the log file *(By default = None, config)*
  * `filepath: str` - Directory path *(By default = None, config)*


### Using a `Lgger(filename, filepath)` object

You can also create the object directly by calling the `Lgger()`. This will
create an object similarly to the `create_log()` function, but will not assign it as a global variable, making the
decorators ignore the current object and creating a new `Lgger()` object
using the default values.

## Log level / Severity:
Just as any other logging library out there, I have added a level/severity
system to the logs. You can add logs as INFO, debug using DEBUG or an error
with ERROR.

All those are saved in the `LogLvl` class and to use it, you just have to
provide the argument in the log function in the following format:
`LogLvl.{level}`.

The levels are as follows:

|   Level   | Value | Example        | Usage                                                                                                               |
|:---------:|:-----:|----------------|---------------------------------------------------------------------------------------------------------------------|
|   DEBUG   |   0   | LogLvl.DEBUG   | Used to track information for developers.                                                                           |
|   INFO    |   1   | LogLvl.INFO    | Used to log general information.                                                                                    |
|  WARNING  |   2   | LogLvl.WARNING | A warning message, pointing to a discrepancy that should not affect the process, but could lead to possible issues. |
|   ERROR   |   3   | LogLvl.ERROR   | This is used for errors or error messages, that doesn't lead to the application to stop.                            |
|   FATAL   |   4   | LogLvl.FATAL   | This is an error log, which if used prior to an application failure due to an exception or something else.          |

Please note that the provided usage is imperative. You can use them as you wish.

## Methods
`Lgger()` has a few methods, that can be used:
  * `log(msg, level)` - used to log a message on a level/severity, provided by
  the user
    * `msg: str`  - (***Required***) Log message to be added to log
    * `lvl: LogLvl` - Log level/severity *(By default = None, config)*
  * `log_debug(msg: str)`, `log_info(msg: str)`
  , `log_warn(msg: str)`, `log_error(msg: str)`, `log_fatal(msg: str)`
  \- used to log a message with a certain level/severity
    * `msg: str`  - (***Required***) Log message to be added to log

### Decorators

Now, this is most probably the most useful part of this whole package.
In order to keep track of what is being provided to the functions, how much time
or whatever needs to be checked/tracked in the future, there are decorators
that will do this. For the time being, I made them work with a global
`Lgger()` object, that is stored in the package. They are also stackable, meaning
you can use more than one decorator to the same function.

* `@time_performance` - This will time the approximate execution time for
the called function. The time is tracked in seconds, with a precision to
the microseconds.
* `@log_args` - This decorator will log the arguments, provided in the
called function. Both *args and **kwargs will be logged.
* `@log_return` - This decorator will log the return value of the
called function.


[Lgger template]: https://github.com/IllusionLife/lgger/tree/main/lgger/templates/lgger.conf.template
[env file]: https://github.com/IllusionLife/lgger/tree/main/lgger/env.py
[Log level / Severity]: https://github.com/IllusionLife/lgger/tree/main#log-level-/-severity