# copy almost all of pando.__main__ to set the www_root

import os
import logging.config
from wsgiref.simple_server import make_server

from pando import website
from pando.logging import log_dammit


logging_cfg = {
    'version': 1,
    'formatters': {
        'threadinfo': {
            'format':
                "%(asctime)s pid-%(process)d thread-%(thread)d "
                "(%(threadName)s) %(levelname)s: %(message)s",
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'threadinfo',
            'level': 'INFO',
            'stream': 'ext://sys.stderr',
        },
    },
    'root': {
        'handlers': ['console'],
    },
}


if __name__ == '__main__':
    logging.config.dictConfig(logging_cfg)
    port = int(os.environ.get('PORT', '8080'))
    host = os.environ.get('PANDO_HOST', '0.0.0.0')
    log_dammit(
        "Greetings, program! Now serving on http://{0}:{1}/."
        .format(host, port))
    website = website.Website(
        www_root='www',
    )
    make_server(host, port, website).serve_forever()
