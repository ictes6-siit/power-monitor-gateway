import logging
import sys, getopt

__author__ = 'Ratchasak Ranron'

version_info = (0, 0, 1, 'b0')
__version__ = '%d.%d.%d%s' % version_info

__all__ = ['powermon', 'serialcomm']

def _setup_log():
    from . import _debug

    logger = logging.getLogger('powermon')
    debug_level = None
    log_filename = None

    opts, args = getopt.getopt(sys.argv[1:],"i:b:l:f", ["port=", "buad=", "loglevel=", "logfile="])
    for o, a in opts:
        if o in ("-l", "--loglevel"):
            debug_level = a
        elif o in ("-f", "--logfile"):
            log_filename = a

    if debug_level is not None:
        _debug.enable_tracing(True)
        filename = log_filename

        LEVELS = {'debug': logging.DEBUG,
                  'info': logging.INFO,
                  'warning': logging.WARNING,
                  'error': logging.ERROR,
                  'critical': logging.CRITICAL}

        level = LEVELS.get(debug_level, logging.CRITICAL + 10)
        logger.setLevel(level = level)

        try:
            handler = logging.FileHandler(filename)
        except:
            handler = logging.StreamHandler()

        fmt = logging.Formatter('%(asctime)s %(levelname)s:%(name)s:%(message)s')
        handler.setFormatter(fmt)
        logger.addHandler(handler)
    else:
        class NullHandler(logging.Handler):
            def emit(self, record):
                pass

        # We set the log level to avoid delegation to the
        # parent log handler (if there is one).
        # Thanks to Chris Clark to pointing this out.
        logger.setLevel(logging.CRITICAL + 10)
        logger.addHandler(NullHandler())


_setup_log()