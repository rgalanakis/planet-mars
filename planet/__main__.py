#!/usr/bin/env python
"""
The Planet aggregator.

A flexible and easy-to-use aggregator for generating websites.
"""

import argparse
import ConfigParser
import locale
import logging
import socket
import sys
import time

import planet
from planet.constants import REQUIRED_OPTIONS

log = logging.getLogger('planet.runner')


def read_config(config_file):
    """Reads and performs validation of config."""
    config = ConfigParser.ConfigParser()
    config.read(config_file)
    if not config.has_section('Planet'):
        sys.stderr.write('Config must have a [Planet] section. Exiting.\n')
        sys.exit(3)
    for o in REQUIRED_OPTIONS:
        if not config.has_option('Planet', o):
            sys.stderr.write(
                '[Planet] section missing required option %r. '
                'Check example/config.ini for an example. '
                'Exiting.\n' % o)
            sys.exit(4)
    return config


def set_locale(localestr):
    # The user can specify more than one locale (separated by ":") as
    # fallbacks.
    locale_ok = False
    for user_locale in localestr.split(':'):
        user_locale = user_locale.strip()
        try:
            locale.setlocale(locale.LC_ALL, user_locale)
        except locale.Error:
            pass
        else:
            locale_ok = True
            break
    if not locale_ok:
        sys.stderr.write("Unsupported locale setting.\n")
        sys.exit(5)


def main():
    starttime = time.clock()
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='DEBUG level logging during update.')
    parser.add_argument('-o', '--offline', action='store_true',
                        help='Update the Planet from the cache only.')
    parser.add_argument('config_file', help='Path to configuration ini file.')
    opts = parser.parse_args()

    config = read_config(opts.config_file)

    if opts.verbose:
        log_level = "DEBUG"
    elif config.has_option('Planet', 'log_level'):
        log_level = config.get('Planet', 'log_level')
    else:
        log_level = logging.WARN
    logging.basicConfig(level=logging.getLevelName(log_level))

    # Read the [Planet] config section
    planet_options = dict(config.items('Planet'))

    # Define locale
    try:
        localestr = config.get('Planet', 'locale')
    except ConfigParser.NoOptionError:
        pass
    else:
        set_locale(localestr)

    feed_timeout = planet_options['feed_timeout']
    try:
        feed_timeout = float(feed_timeout)
    except Exception:
        sys.stderr.write("Feed timeout set to invalid value '%s', skipping.\n"
                         % feed_timeout)
        sys.exit(6)

    if not opts.offline:
        socket.setdefaulttimeout(feed_timeout)
        log.debug("Socket timeout set to %d seconds", feed_timeout)

    # run the planet
    planet_name = planet_options['name']
    planet_link = planet_options['link']
    template_files = planet.parse_template_files(
        planet_options['template_files'])

    my_planet = planet.Planet(config)
    my_planet.run(planet_name, planet_link, template_files, opts.offline)

    my_planet.generate_all_files(template_files, planet_options)
    duration = time.clock() - starttime
    log.info('Took %ss to generate.', duration)


if __name__ == "__main__":
    main()
