import pickle
import service_base

class Sender(service_base.NotificationService):
	def __init__(self, path = None):
		service_base.NotificationService.__init__(self, path)

	def notify(self, **kwargs):
		data = "Unknown event"
		try:
			msg = service_base.Message(**kwargs)
			data = pickle.dumps(msg)
		except Exception as e:
			print(e)
			data += "\n" + str(kwargs)

		with open(self.path, "w") as fifo:
			try:
				fifo.write(data)
			except:
				pass
