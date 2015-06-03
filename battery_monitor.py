#!/usr/bin/python

import os
import sys
import time
my_dir = os.path.abspath(os.path.dirname(sys.argv[0]))
sys.path.append(os.path.join(my_dir))
print(sys.path)
from notification_service.sender import Sender

presence_file = "/sys/class/power_supply/BAT0/present"
status_file = "/sys/class/power_supply/BAT0/uevent"
capacity_key = "POWER_SUPPLY_CAPACITY"
critical_power = 5
low_power = 25
data = {}

sender = Sender()

while True:
	with open(presence_file) as pf:
		if int(pf.read().strip()):
			with open(status_file) as sf:
				for line in sf.readlines():
					line = line.strip()
					if line:
						(k, v) = line.split("=")
						data[k] = v
				power = int(data.get(capacity_key, 100))
				if power < critical_power:
					sender.notify(
						timeout = 10000,
						category = "powers",
						urgency = "critical",
						icon = "battery-low",
						message = [
							"Battery critical (%d%%)" % power,
							"Will hibernate"
						],
					)
					os.system("/usr/bin/sudo /usr/sbin/pm-hibernate")
				elif power < low_power:
					sender.notify(
						timeout = 5000,
						category = "power",
						urgency = "critical",
						icon = "battery-caution",
						message = ["Battery low", "Remaining: %d%%" % power]
					)
					pass

				time.sleep(60)
