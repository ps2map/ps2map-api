"""Main script for launching the APL API component.

This script sets up logging, checks for database availability and
launches the API server.

For a list of command line arguments and their purpose, run this script
with the ``--help`` flag set.
"""

import argparse
import asyncio
import logging
import os

from ._server import ApiHost

log = logging.getLogger('api')

# Default database configuration
DEFAULT_DB_HOST = '127.0.0.1'
DEFAULT_DB_NAME = 'postgres'
DEFAULT_DB_USER = 'postgres'

# Logging configuration
fmt = logging.Formatter('%(asctime)s [%(levelname)s] %(name)s: %(message)s')
fh_ = logging.FileHandler(filename='api.log', encoding='utf-8', mode='w+')
sh_ = logging.StreamHandler()
fh_.setFormatter(fmt)
sh_.setFormatter(fmt)


async def main(db_host: str, db_user: str, db_pass: str, db_name: str) -> None:
    """Asynchronous component of the main listener script.

    This coroutine acts much like the ``if __name__ == '__main___':``
    clause below, but supports asynchronous methods.
    """
    os.environ['_DB_NAME'] = db_name
    os.environ['_DB_HOST'] = db_host
    os.environ['_DB_USER'] = db_user
    os.environ['_DB_PASS'] = db_pass
    host = ApiHost()
    log.info('Starting uvicorn server...')
    await host.start()


if __name__ == '__main__':
    # Define command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--db-user', '-U', default=DEFAULT_DB_USER,
        help='The user account to use when connecting to the database')
    parser.add_argument(
        '--db-pass', '-P', required=True,
        help='The password to use when connecting to the database')
    parser.add_argument(
        '--db-host', '-H', default=DEFAULT_DB_HOST,
        help='The address of the database host')
    parser.add_argument(
        '--db-name', '-N', default=DEFAULT_DB_NAME,
        help='The name of the database to access')
    parser.add_argument(
        '--log-level', '-L', default='INFO',
        choices=['DISABLE', 'ERROR', 'WARNING', 'INFO', 'DEBUG'],
        help='The log level to use; for levels greater than "DEBUG", '
             'the logging input from Auraxium will also be included')
    # Parse arguments from sys.argv
    kwargs = vars(parser.parse_args())
    # Optionally set up logging
    if kwargs['log_level'] != 'DISABLE':
        log_level = getattr(logging, kwargs.pop('log_level'))
        log.setLevel(log_level)
        log.addHandler(fh_)
        log.addHandler(sh_)

    # Run utility
    loop = asyncio.get_event_loop()
    loop.create_task(main(**kwargs))
    try:
        loop.run_forever()
    except InterruptedError:
        log.info('The application has been shut down by an external signal')
    except KeyboardInterrupt:
        log.info('The application has been shut down by the user')
    except BaseException as err:
        log.exception('An unhandled exception occurred:')
        raise err from err
