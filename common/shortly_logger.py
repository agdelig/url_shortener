import logging

logger = logging.getLogger(__name__)


def configure_logger():
    logger.setLevel(logging.DEBUG)

    # Create the Handler for logging data to a file
    logger_handler = logging.FileHandler('shorten.log')
    logger_handler.setLevel(logging.DEBUG)

    # Create a Formatter for formatting the log messages
    logger_formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')

    # Add the Formatter to the Handler
    logger_handler.setFormatter(logger_formatter)

    # Add the Handler to the Logger
    logger.addHandler(logger_handler)
    logger.info('Completed configuring logger()!')


configure_logger()

