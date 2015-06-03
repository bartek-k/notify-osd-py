#!/usr/local/bin/python -tt

import os
import sys
import stat
import atexit
import pickle
import signal
from gi.repository import Notify

import service_base

my_dir = os.path.abspath(os.path.dirname(sys.argv[0]))
sys.path.append(os.path.join(my_dir, ".."))

IS_SIGNALED = False


def sighandler(signum, frame):
	global IS_SIGNALED
	print("SIGN: ", signum, frame)
	IS_SIGNALED = True
	

def is_fifo(path):
	r = False
	try:
		r = stat.S_ISFIFO(os.stat(path or service_base.PATH).st_mode)
	except OSError:
		pass
	return r


@atexit.register
def cleanup():
	notification = Notify.Notification.new(
		"NotifyService", "Notification"
	)
	notification.set_timeout(1000)
	notification.update("NotificationService", "Exiting", "process-stop")
	notification.show()


class Listener(service_base.NotificationService):
	def __init__(self, path=None):
		service_base.NotificationService.__init__(self, path)
		self.create_fifo()

	def create_fifo(self):
		try:
			if os.path.exists(self.path):
				os.unlink(self.path)
			os.mkfifo(self.path)
		except OSError as e:
			print(e)

	def main_loop(self):
		global IS_SIGNALED
		if is_fifo(self.path):
			priv_n = Notify.Notification.new(
				"NotifyService", "Notification"
			)
			priv_n.set_timeout(3000)
			priv_n.update("NotificationService ready", self.path, "system-run")
			priv_n.show()
			notification = Notify.Notification.new(
				"NotifyService", "Notification"
			)
		while not IS_SIGNALED:
			with open(self.path) as fifo:
				data = ""
				try:
					data = fifo.read()
					msg = pickle.loads(data)
					title = msg.message[0]
					text = "\n".join(msg.message[1:])
					notification.set_timeout(msg.timeout)
					notification.set_urgency(self.map_urgency(msg.urgency))
					notification.update(title, text, msg.icon)
				except Exception as e:
					print(e)
					notification.update("Event", data)

				notification.show()


if __name__ == "__main__":
	signal.signal(signal.SIGINT, sighandler)
	signal.signal(signal.SIGTERM, sighandler)
	# signal.signal(signal.CTRL_C_EVENT, sighandler)
	listener = Listener()
	listener.main_loop()

