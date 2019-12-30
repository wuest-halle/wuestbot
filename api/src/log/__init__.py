import logging
import sys

LOG_LEVELS = {
    "debug": 10,
    "info": 20,
    "warn": 30,
    "warning": 30,
    "error": 40,
}

DEFAULT_LOG_LEVEL = "info"

def set_level(log, level):
    """Sets the log level.

    Will default to 'info'.

    Args:
        log: A Python Logging object
        level: The log level to set. Must be part auf LOG_LEVELS.
    """

    if level not in LOG_LEVELS:
        print(f"Unable to parse '{level}', defaulting to '{DEFAULT_LOG_LEVEL}'")
        level = LOG_LEVELS[DEFAULT_LOG_LEVEL]
    else:
        level = LOG_LEVELS[level]

    log.setLevel(level)

def get_logger(name="root"):
    """Returns a Logger object with handlers configured.

    Will use the Logger.LOG_LEVEL attribute for the log level. If you want
    to adjust the log level, change it beforehand.

    Args:
        level (string): The log level to set.

    Returns:
        A Python logger object.
    """

    log = logging.getLogger(name)
    set_level(log, Logger.LOG_LEVEL)

    # If we instantiate multiple loggers with the same name,
    # we would add duplicate handlers.
    if not log.handlers:
        sh = logging.StreamHandler(sys.stdout)
        fmt = logging.Formatter("%(asctime)s|%(name)s|%(levelname)s|%(message)s'")
        sh.setFormatter(fmt)
        log.addHandler(sh)

    return log

class Singleton(type):
    """Metaclass to implement the Singleton pattern.
    This Metaclass implements the Singleton pattern. This should only be used
    logging purposes to avoid introducing mutable global state into the
    application.
    Metaclasses are classes that instantiate other classes. Everytime a new
    class (any class in Python) is instantiated, it checks what the Metaclass
    of that specific class is, then executes it with certain parameters.
    In our case, the metaclass holds a dictionary that keeps track of all the
    instances that have been created by the Singleton Metaclass. Everytime we
    instantiate or call :class:`log.Logger`, whose
    Metaclass is the Singleton class, we check if we already have such an
    instance. If yes, that one is returned. If not, we create such an instance,
    add it to the ``_instances`` dict and then return it. Subsequent calls will
    then only return one instance, which is always the same object with the same ID.
    For more information about the pattern, see `Eli's Post
    <https://eli.thegreenplace.net/2011/08/14/python-metaclasses-by-example/>`_
    and `Stack Overflow  <https://stackoverflow.com/a/6798042>`_.
    Example:
        >>> log1 = Logger(__name__)
        >>> log2 = Logger(__name__)
        >>> log1.info("hello")
        hello
        >>> log2.info("world")
        world
        >>> log3 = Logger("test")
        >>> id(log1) == id(log2) == id(log3)
        True
    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        else:
            cls._instances[cls].__init__(*args, **kwargs)

        return cls._instances[cls]

class Logger(metaclass=Singleton):
    """Provides logging capabilities.

    This class is a singleton that returns a proxy instance of
    ``logging.Logger``.

    The default log level is set to 'info'. Change it by assigning it
    to the Logger class. Note that since the Logger is a singleton, the
    log level is shared between instances.

    Example:
        >>> Logger.LOG_LEVEL = "info"
        >>> info_logger = Logger("info_logger")
        >>> info_logger.info("Hello")
        Hello
        >>> Logger.LOG_LEVEL = "error"
        >>> error_logger = Logger("error")
        error
        >>> info_logger.info("Hello again")
        >>> # no output from info_logger

    All functions support ``f``-, ``%``-, and ``format``-Style formatting.
    Example:
        >>> log = Logger(__name__)
        >>> log.info("hello world")
        hello world
        >>> log.info("%s %s", "hello", "world")
        hello world
        >>> a, b = "hello", "world"
        >>> log.info(f"{a} {b}")
        hello world
        >>> log.info("{} {}".format(b, a))
        world hello

    Attributes:
        LOG_LEVEL (int): The log level to be used across the application.
    Args:
        name (str): The name of the logger.
    """

    LOG_LEVEL = 'info'

    def __init__(self, name="root"):
        self.logger = get_logger(name)

    @property
    def level(self):
        """Returns the Python log level equivalent.
        Returns:
            The Python loglevel equivalent or None if logger not instantiated.
        """
        if not self.logger:
            return None

        if self.logger.disabled:
            return 0

        return self.logger.level

    def error(self, msg, *args, **kwargs):
        """Logs a message on error level.

        Args:
            msg (str): The message to be logged.
        """

        self.logger.error(msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        """Logs a message on warning level.

        Args:
            msg (str): The message to be logged.
        """

        self.logger.warning(msg, *args, **kwargs)

    def info(self, msg, *args, **kwargs):
        """Logs a message on info level.

        Args:
            msg (str): The message to be logged.
        """

        self.logger.info(msg, *args, **kwargs)

    def debug(self, msg, *args, **kwargs):
        """Logs a message on debug level.

        Args:
            msg (str): The message to be logged.
        """

        self.logger.debug(msg, *args, **kwargs)