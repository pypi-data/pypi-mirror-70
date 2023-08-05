# Logger_tt
Make configuring logging simpler and log even exceptions that you forgot to catch.

## Usage:
**Install**: `pip install logger_tt`

In the most simple case, add the following code into your main python script of your project:

```python
from logger_tt import setup_logging    

setup_logging()
```

Then from any of your modules, you just need to get a `logger` and start logging.

```python
from logging import getLogger

logger = getLogger(__name__)

logger.debug('Module is initialized')
logger.info('Making connection ...')
```


This will provide your project with the following **default** log behavior:

* log file: Assume that your `working directory` is `project_root`,
 log.txt is stored at your `project_root/logs/` folder. 
If the log path doesn't exist, it will be created. 
The log file is time rotated at midnight. A maximum of 15 dates of logs will be kept.
This log file's `level` is `DEBUG`.<br>
The log format is `[%(asctime)s] [%(name)s %(levelname)s] %(message)s` where time is `%Y-%m-%d %H:%M:%S`.<br>
Example: `[2020-05-09 00:31:33] [myproject.mymodule DEBUG] Module is initialized`

* console: log with level `INFO` and above will be printed to `stdout` of the console. <br>
The format for console log is simpler: `[%(asctime)s] %(levelname)s: %(message)s`. <br>
Example: `[2020-05-09 00:31:34] INFO: Making connection ...`

* `urllib3` logger: this ready-made logger is to silent unwanted messages from `requests` library.

* `root` logger: if there is no logger initialized in your module, this logger will be used with the above behaviors.
This logger is also used to log **uncaught exception** in your project. Example:

```python
raise RecursionError
```

```python
# log.txt
2020-05-31 19:16:01 ERROR	[root] Uncaught exception
Traceback (most recent call last):
  File "D:/MyProject/Echelon/eyes.py", line 13, in <module>
    raise RecursionError
RecursionError
```

## Config:
All configs are done through `setup_logging` function:
```python
setup_logging(config_path="", log_path="", capture_print=False, strict=False, guess_level=False)
```


1. You can overwrite the default log path with your own as follows:
    
   ```python
   setup_logging(log_path='new/path/to/your_log.txt')
   ```

2. You can config your own logger and handler by providing either `yaml` or `json` config file as follows:
    
   ```python
   setup_logging(config_path='path/to/.yaml_or_.json')
   ```

   Without providing a config file, the default config file with the above **default** log behavior is used.
   You could copy `log_conf.yaml` or `log_conf.json` shipped with this package to start making your version.

   **Warning**: To process `.yaml` config file, you need to `pyyaml` package: `pip install pyyaml`

3. Capture stdout:

   If you have an old code base with a lot of `print(msg)` or `sys.stdout.write(msg)` and 
   don't have access or time to refactor them into something like `logger.info(msg)`, 
   you can capture these `msg` and log them to file, too.
   
   To capture only `msg` that is printed out by `print(msg)`, simply do as follows: 
    
   ```python
   setup_logging(capture_print=True)
   ```
   
   Example:
   ```python
   print('To be or not to be')
   sys.stdout.write('That is the question')
   ```
   
   ```
   # log.txt
   [2020-05-09 11:42:08] [PrintCapture INFO] To be or not to be
   ```
   
   <hr>
   
   Yes, `That is the question` is not captured. 
   Some libraries may directly use `sys.stdout.write` to draw on the screen (eg. progress bar) or do something quirk.
   This kind of information is usually not useful for users. But when you do need it, you can capture it as follows:
   
   ```python
   setup_logging(capture_print=True, strict=True)
   ```
   
   Example:
   ```python
   sys.stdout.write('The plane VJ-723 has been delayed')
   sys.stdout.write('New departure time has not been scheduled')
   ```
   
   ```
   # log.txt
   [2020-05-09 11:42:08] [PrintCapture INFO] The plane VJ-723 has been delayed
   [2020-05-09 11:42:08] [PrintCapture INFO] New departure time has not been scheduled
   ```
  
   <hr>
   
   As you have seen, the log level of the captured message is `INFO` . 
   What if the code base prints something like `An error has occurred. Abort operation.` and you want to log it as `Error`?
   Just add `guess_level=True` to `setup_logging()`.
   
   ```python
   setup_logging(capture_print=True, guess_level=True)
   ```
   
   Example:
   ```python
   print('An error has occurred. Abort operation.')
   print('A critical error has occurred during making request to database')
   ```
   
   ```
   # log.txt
   [2020-05-09 11:42:08] [PrintCapture ERROR] An error has occurred. Abort operation.
   [2020-05-09 11:42:08] [PrintCapture CRITICAL] A critical error has occurred during making request to database
   ```
   
   
   **Note**: Capturing stdout ignores messages of `blank line`. 
   That means messages like `\n\n` or `  `(spaces) will not appear in the log. 
   But messages that contain blank line(s) and other characters will be fully logged.
   For example, `\nTo day is a beautiful day\n` will be logged as is.  

# Sample config:

1. Yaml format:

   ```yaml
   version: 1
   disable_existing_loggers: False
   formatters:
     simple:
       format: "[%(asctime)s] [%(name)s %(levelname)s] %(message)s"
       datefmt: "%Y-%m-%d %H:%M:%S"
     brief: {
       format: "[%(asctime)s] %(levelname)s: %(message)s"
       datefmt: "%Y-%m-%d %H:%M:%S"
   handlers:
     console:
       class: logging.StreamHandler
       level: INFO
       formatter: simple
       stream: ext://sys.stdout
   
     error_file_handler:
       class: logging.handlers.TimedRotatingFileHandler
       level: DEBUG
       formatter: simple
       filename: logs/log.txt
       backupCount: 15
       encoding: utf8
       when: midnight
   
   loggers:
     urllib3:
       level: WARNING
       handlers: [console, error_file_handler]
       propagate: no
   
   root:
     level: DEBUG
     handlers: [console, error_file_handler]
   ```

<br>
2. Json format:

   ```json
   {
     "version": 1,
     "disable_existing_loggers": false,
     "formatters": {
       "simple": {
         "format": "[%(asctime)s] [%(name)s %(levelname)s] %(message)s",
         "datefmt": "%Y-%m-%d %H:%M:%S"
       },
       "brief": {
         "format": "[%(asctime)s] %(levelname)s: %(message)s",
         "datefmt": "%Y-%m-%d %H:%M:%S"
       }
     },
   
     "handlers": {
       "console": {
         "class": "logging.StreamHandler",
         "level": "INFO",
         "formatter": "brief",
         "stream": "ext://sys.stdout"
       },
   
       "error_file_handler": {
         "class": "logging.handlers.TimedRotatingFileHandler",
         "level": "DEBUG",
         "formatter": "simple",
         "filename": "logs/log.txt",
         "backupCount": 15,
         "encoding": "utf8",
         "when": "midnight"
       }
     },
   
     "loggers": {
       "urllib3": {
         "level": "ERROR",
         "handlers": ["console", "error_file_handler"],
         "propagate": false
       }
     },
   
     "root": {
       "level": "DEBUG",
       "handlers": ["console", "error_file_handler"]
     }
   }
   ```