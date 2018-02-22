A logger class.

Note, probably you'd want to put a copy of this file in your personal user site
directory (you can get the directory by running 'python -m site --user-site').
That way you can always import it without messing with sys.path.

Features:
    * Logging to file is optional.
    * Autosaving to file is optional.
    * Easy to change or add log levels.
    * Easy to add fields to log (beyond the message itself).

Usage:
    import logger
    log = logger.Logger("logfile.txt")
    log.ok("Something good happend.")
    log.info("Something happend.")
    log.warning("Something bad happend.")
    log.error("Something worse happend.")
    log.debug("Any kind of debugging message.")
    log.save()

For displaying the log, access member 'log' externally and print what you want
in the order you want.

A general suggestion is to have a 'log=logger.Logger()' argument for every
relevant class constructor, and send an existing Logger object as argument
to get the class to log to an already existing log higher up.