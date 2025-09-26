# main.py


import logging
import logging.config
import sys
from generate_pages import (
    copy_files,
    generate_page_recursive,
)


dir_path_static = "./static"
dir_path_public = "./docs"
dir_path_content = "./content"
template_path = "./template.html"


def setup_logging():
    LOGGING_CONFIG = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'simple': {
                'format': '%(asctime)s %(levelname)s: %(message)s',
            },
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'level': 'INFO', # Only print INFO and above to stdout
                'formatter': 'simple',
                'stream': 'ext://sys.stdout',
            },
            'file': {
                'class': 'logging.FileHandler',
                'level': 'DEBUG', # Print everything to log file
                'formatter': 'simple',
                'filename': 'generate.log',
                'mode': 'w',
            },
        },
        'root': {
            'level': 'DEBUG',
            'handlers': ['console', 'file'],
        },
    }

    logging.config.dictConfig(LOGGING_CONFIG)


def main(): 
    setup_logging()

    if len(sys.argv) == 2:
        basepath = sys.argv[1]
    else:
        basepath = "/"

    copy_files(src=dir_path_static, dst=dir_path_public)
    generate_page_recursive(basepath, dir_path_content, template_path, dir_path_public)


if __name__ == "__main__": 
    main()

