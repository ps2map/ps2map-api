"""Main script for launching the API host.

This script sets up logging, checks for database availability and
launches the API server.

For a list of command line arguments and their purpose, run this script
with the ``--help`` flag set.
"""

import argparse
import asyncio
import logging
import os

import uvicorn

from .database import Database

log = logging.getLogger('api')

# Default database configuration
DEFAULT_DB_HOST = '127.0.0.1'
DEFAULT_DB_PORT = 5432
DEFAULT_DB_NAME = 'PS2Map'
DEFAULT_DB_USER = 'postgres'

# Logging configuration
fmt = logging.Formatter('%(asctime)s [%(levelname)s] %(name)s: %(message)s')
fh_ = logging.FileHandler(filename='api.log', encoding='utf-8', mode='w+')
sh_ = logging.StreamHandler()
fh_.setFormatter(fmt)
sh_.setFormatter(fmt)


async def main(db_host: str, db_port: int, db_user: str, db_pass: str,
               db_name: str) -> None:  # pragma: no cover
    """Asynchronous component of the main listener script.

    This coroutine acts much like the ``if __name__ == '__main__':``
    clause below, but supports asynchronous methods.

    Args:
        db_host (str): Host address of the database server.
        db_port (str): Port of the database server.
        db_user (str): Login user for the database server.
        db_pass (str): Login password for the database server.
        db_name (str): Name of the database to access.

    """
    # Create database connection
    log.info('Connecting to database \'%s\' at %s as user \'%s\'...',
             db_name, db_host, db_user)
    Database().create_pool(db_host, db_port, db_user,  db_pass, db_name)
    log.info('Database connection successful')
    # Starting API server
    log.info('Starting uvicorn server...')

    config = uvicorn.Config(  # type: ignore
        'server.app:app', host='0.0.0.0', port=5000,
        log_level='info', loop='asyncio')
    await uvicorn.Server(config=config).serve()  # type: ignore

if __name__ == '__main__':
    loop_policy: asyncio.AbstractEventLoopPolicy
    if os.name == 'nt':
        loop_policy = asyncio.WindowsSelectorEventLoopPolicy()
    else:
        loop_policy = asyncio.DefaultEventLoopPolicy()
    asyncio.set_event_loop_policy(loop_policy)
    # Get default values from environment
    def_service_id = os.getenv('PS2MAP_SERVICE_ID', 's:example')
    def_db_host = os.getenv('PS2MAP_DB_HOST', DEFAULT_DB_HOST)
    def_db_port = int(os.getenv('PS2MAP_DB_PORT', str(DEFAULT_DB_PORT)))
    def_db_name = os.getenv('PS2MAP_DB_NAME', DEFAULT_DB_NAME)
    def_db_user = os.getenv('PS2MAP_DB_USER', DEFAULT_DB_USER)
    def_db_pass = os.getenv('PS2MAP_DB_PASS')
    # Define command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--db-user', '-U', default=def_db_user,
        help='The user account to use when connecting to the database')
    parser.add_argument(
        '--db-pass', '-P', required=def_db_pass is None, default=def_db_pass,
        help='The password to use when connecting to the database')
    parser.add_argument(
        '--db-host', '-H', default=def_db_host,
        help='The address of the database host')
    parser.add_argument(
        '--db-port', '-T', default=def_db_port,
        help='The port of the database host')
    parser.add_argument(
        '--db-name', '-N', default=def_db_name,
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
    loop = asyncio.new_event_loop()
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
