"""A logger class.

Usage:
    import logger
    log = logger.Logger()
    log.ok("Something good happend.")
    log.info("Something happend.")
    log.warning("Something bad happend.")
    log.error("Something worse happend.")
    log.debug("Any kind of debugging message.")
"""

from datetime import datetime

# Logging levels. These are in text format so that they can be used as CSS
# class names immediately.
OK		= 'ok'
INFO	= 'neutral'
WARNING	= 'warning'
ERROR 	= 'error'
DEBUG	= 'debug'

# Indexes
DATE = 0
TIME = 1
LEVEL = 2
MSG = 3


class Logger(object):
    """For logging of messages."""

    def __init__(self, filename='', autosave=False, separator='|'):
        """Initialize with logfile options."""
        self.filename = filename        # Name of log file (optional).
        self.autosave = autosave        # Write to file automatically?
        self.separator = separator      # Separates log entry fields.
        self.log = list()               # The log!
        self.template = '%s' + self.separator + '%s' + self.separator + \
                        '%s' + self.separator + '%s\n'

    def __iadd__(self, other):
        """Extend self log with another using the += operator."""
        self.log.extend(other.log)
        return self

    def __str__(self):
        text = ''
        for entry in self.log:
            text += self._to_string(entry)
        return text

    def ok(self, msg):
        """Save a message in the log."""
        self._add([OK, msg])

    def info(self, msg):
        """Save a message in the log."""
        self._add([INFO, msg])

    def warning(self, msg):
        """Save a message in the log."""
        self._add([WARNING, msg])

    def error(self, msg):
        """Save a message in the log."""
        self._add([ERROR, msg])

    def debug(self, msg):
        """Save a message in the log."""
        self._add([DEBUG, msg])

    def clear(self):
        """Clear the log from all messages."""
        del self.log[:]

    def save(self, overwrite=False):
        """Save log to file.

        If autosave is on, only the last logged entry will be saved. If off,
        the the entire log will be saved.

        Arguments:
            overwrite:  Overwrite or append to file (boolean, optional)?

        Returns:
            True/False: Whether writing went ok or not (boolean).
        """
        # Determine if to save.
        if not self.filename or not self.log:
            return False

        # Determine what to save.
        source = None
        if self.autosave:
            source = [self.log[-1]]     # The last entry.
        else:
            source = self.log           # Entire log.

        # Determine how to save.
        fobject = None
        if overwrite:
            try:
                fobject = open(self.filename, 'w')
            except IOError:
                self.error('Logger: Could not open logfile "%s" for '
                           'overwriting.' % self.filename)
                return False
        else:
            try:
                fobject = open(self.filename, 'a')
            except IOError:
                self.error('Logger: Could not open logfile "%s" for '
                           'appending.' % self.filename)
                return False

        # Save!
        not_written = 0
        for entry in source:
            line = self._to_string(entry)
            try:
                fobject.write(line)
            except IOError:
                not_written += 1
                self.error('Logger: Could not write to logfile "%s".' %
                           self.filename)
                self.info('Logger: Did not write %s of %s log entries.' %
                          (not_written, len(source)))
                return False
        return True

    #
    # Supporting methods.
    #
    @staticmethod
    def _now():
        """Fetch current date and time.

        Returns:
            Date and time:  As [yyyy-mm-dd, hh:mm:ss].
        """
        return datetime.now().strftime('%Y-%m-%d;%H:%M:%S').split(';')

    def _add(self, entry):
        """Add a log entry to the log. Log file is saved if autosave is on."""
        self.log.append(self._now() + entry)
        self.save()

    def _to_string(self, entry):
        """Build a text string from a log entry.

        Returns:
            Log entry (str).
        """
        return self.template % (entry[DATE], entry[TIME], entry[LEVEL],
                                entry[MSG])
