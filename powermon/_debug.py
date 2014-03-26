__author__ = 'Ratchasak Ranron <ratchasak.ranron@gmail.com>'

__all__ = ['methodtrace', 'functiontrace']

import logging
from . import _interop as _interop

_enable_tracing = False

def enable_tracing(enable):
    global _enable_tracing
    _enable_tracing = enable

def _trace_function_call(logger, fname, *args, **named_args):
    logger.debug(
                # TODO: check if 'f' is a method or a free function
                fname + '(' + \
                ', '.join((str(val) for val in args)) + \
                ', '.join((name + '=' + str(val) for name, val in named_args.items())) + ')'
            )

# decorator for methods calls tracing
def methodtrace(logger):
    def decorator_logging(f):
        if not _enable_tracing:
            return f
        def do_trace(*args, **named_args):
            # this if is just a optimization to avoid unecessary string formatting
            if logging.DEBUG >= logger.getEffectiveLevel():
                fn = type(args[0]).__name__ + '.' + f.__name__
                _trace_function_call(logger, fn, *args[1:], **named_args)
            return f(*args, **named_args)
        _interop._update_wrapper(do_trace, f)
        return do_trace
    return decorator_logging

# decorator for methods calls tracing
def functiontrace(logger):
    def decorator_logging(f):
        if not _enable_tracing:
            return f
        def do_trace(*args, **named_args):
            # this if is just a optimization to avoid unecessary string formatting
            if logging.DEBUG >= logger.getEffectiveLevel():
                _trace_function_call(logger, f.__name__, *args, **named_args)
            return f(*args, **named_args)
        _interop._update_wrapper(do_trace, f)
        return do_trace
    return decorator_logging