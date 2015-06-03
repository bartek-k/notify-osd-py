#!/usr/local/bin/python

import argparse
import sender

parser = argparse.ArgumentParser(
	description='Send message to NotificationService')

parser.add_argument(
	"--timeout", "-t", type=int,
	help="timeout", default=3000)
parser.add_argument(
	"--category", "-c", type=str,
	help="category", default="Generic")
parser.add_argument(
	"--urgency", "-u", type=str,
	help="urgency", default="normal")
parser.add_argument(
	"--icon", "-i", type=str,
	help="icon name", default="")
parser.add_argument("message", nargs="+")

arguments = parser.parse_args()
sender = sender.Sender()
sender.notify(
	timeout=arguments.timeout,
	category=arguments.category,
	urgency=arguments.urgency,
	icon=arguments.icon,
	message=arguments.message
)
