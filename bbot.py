#!/usr/bin/env python
import os
import sys
import argparse
import logging
import logging.handlers
import time

from matrix_client.api import MatrixHttpApi
from bbot.engine import Engine
from bbot.matrix import MatrixConfig
import bbot.sample

from matrix_client.client import MatrixClient
from matrix_client.api import MatrixRequestError
from requests.exceptions import MissingSchema

from plugins.b64 import Base64Plugin
from plugins.time_utils import TimePlugin

log = logging.getLogger(name=__name__)


def load_config(loc):
    try:
	with open(loc, 'r') as f:
            return MatrixConfig.from_file(f)
    except:
	pass


def configure_logging(logfile):
    log_format = "%(asctime)s %(levelname)s: %(message)s"
    logging.basicConfig(
	level=logging.DEBUG,
	format=log_format
    )

    if logfile:
	formatter = logging.Formatter(log_format)
	handler = logging.handlers.RotatingFileHandler(logfile,
                                                maxBytes=(1000 * 1000 * 20),
                                                backupCount=5)
	handler.setFormatter(formatter)
	logging.getLogger('').addHandler(handler)


def on_message(event):
    if event['type'] == "m.room.member":
        if event['membership'] == "join":
            print("{0} joined".format(event['content']['displayname']))
    elif event['type'] == "m.room.message":
        if event['content']['msgtype'] == "m.text":
            print("{0}: {1}".format(event['sender'], event['content']['body']))
    else:
        print(event['type'])


def main(config):
    log.info("Main module init ok ...")
    client = MatrixClient(config.homeserver)
    try:
	token = client.login_with_password(username=config.username, password=config.password)
	base_url = config.homeserver + "/_matrix/client/api/v1"
	matrix = MatrixHttpApi(config.homeserver, token)

    except MatrixRequestError as e:
	print(e)
	if e.code == 403:
            print("Bad username or password.")
            sys.exit(4)
	else:
            print("Check your sever details are correct.")
            sys.exit(2)

    except MissingSchema as e:
	print("Bad URL format.")
	print(e)
	sys.exit(3)

    log.info("User token is: " + str(token))

    # todo: add in config config.default_room
    room = client.join_room("#admins:matrix.bingo-boom.ru")
    # room.send_text("stupid bot is coming ;-)")

    # todo: add in config config.nickname
    user = client.get_user(config.username)
    log.info("Current Display Name: %s" % user.get_display_name())
    user.set_display_name("Matrix")
    # todo: add default bit icon
    # http://www.avatarsdb.com/avatars/matrix_rain.gif
    user.set_avatar_url("http://www.avatarsdb.com/avatars/matrix_rain.gif")

    log.debug("Setting up plugins...")

    plugins = [
        TimePlugin,
        Base64Plugin,
    ]

    engine = Engine(matrix, config)

    for plugin in plugins:
	engine.add_plugin(plugin)
    engine.setup()

#    room.add_listener(on_message)
#    client.start_listener_thread()

    while True:
	try:
            log.info("Listening for incoming events.")
            engine.event_loop()
	except Exception as e:
            log.error("Ruh roh: %s", e)
	time.sleep(5)

#	msg = bbot.sample.get_input()
#	if msg == "/quit":
#	    room.send_text("stupid bot is out :-(")
#	    break
#	else:
#	    room.send_text(msg)


if __name__ == '__main__':
    a = argparse.ArgumentParser("Run Matrix-BB.")

    a.add_argument(
	"-c", "--config", dest="config",
	help="The config to create or read from."
    )

    a.add_argument(
	"-l", "--log-file", dest="log",
	help="Log to this file."
    )

    args = a.parse_args()
    configure_logging(args.log)
    log.info("  ===== BBot initialising ===== ")

    config = None

    if args.config:
	log.info("Loading config from %s", args.config)
	config = load_config(args.config)
	if not config:
            log.info("Config not found.")
            print "Config file could not be loaded."
    else:
	print "You probably want to run 'python bbot.py -c bbot.json'"

    if config:
	main(config)
