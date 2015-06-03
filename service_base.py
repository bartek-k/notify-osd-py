import os
from gi.repository import Notify

PATH = os.path.expanduser("~/tmp/notify_service.fifo")

class Message(object):
	def __init__(self, **kwargs):
		self.timeout = kwargs.pop("timeout", 3000)
		self.urgency = kwargs.pop("urgency", "normal")
		self.message = kwargs.pop("message", "...")
		self.category = kwargs.pop("category", "<Uncategorized>")
		self.icon = kwargs.pop("icon", None)


class NotificationService(object):
	def __init__(self, path = None):
		self.path = (path or PATH)
		self.service_name = "NotificationService"
		Notify.init(self.service_name)

	def map_urgency(self, v):
		vals = {
			"low" : Notify.Urgency.LOW,
			"normal" : Notify.Urgency.NORMAL,
			"critical" : Notify.Urgency.CRITICAL,
		}
		return vals.get(v.lower(), "normal")

