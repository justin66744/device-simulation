class Simulation:
    def __init__(self, length, devices, propagates, alerts, cancellations):
        self._length = int(length)
        self._devices = devices
        self._propagates = propagates
        self._alerts = alerts
        self._cancellations = cancellations
        self._time = 0

        self._alert_times = []
        for alert in self._alerts.values():
            self._alert_times.append(alert[1])
        self._alert_times.sort()

        self._cancel_times = []
        for cancellation in self._cancellations.values():
            self._cancel_times.append(cancellation[1])
        self._cancel_times.sort()

    def prop_alert(self):
        curr_alert = []
        curr_props = []
        for dev_id, (desc, time) in self._alerts.items():
            if int(time) == self._time:
                curr_alert.append((dev_id, desc))

        for dev_id, (propped_to, delay) in self._propagates.items():
            curr_props.append((dev_id, (propped_to, delay)))

        for dev_id, desc in curr_alert:
            if dev_id in self._propagates.keys():
                delay = self._propagates[dev_id][1]
                new_time = self._time + int(delay)
                self._time = new_time

                if new_time < int(self._length):
                    print(f"@{self._time}: #{dev_id} SENT ALERT TO #{self._propagates[dev_id][0]}: {desc}")
                    print(f"@{new_time}: #{self._propagates[dev_id][0]} RECEIVED ALERT FROM #{dev_id}: {desc}")

                while new_time < int(self._length):
                    for prop in curr_props:
                        new_time += int(prop[1][1])
                        self._time = new_time
                        if new_time < int(self._length):
                            print(f"@{self._time}: #{prop[0]} SENT ALERT TO #{prop[1][0]}: {desc}")
                            print(f"@{new_time}: #{prop[1][0]} RECEIVED ALERT FROM #{prop[0]}: {desc}")




    def prop_cancel(self):
        pass



    def run(self):
        while self._time < self._length:
            curr_alert = None
            curr_cancellation = None
            if len(self._alert_times) > 0:
                curr_alert = self._alert_times[0]
            if len(self._cancel_times) > 0:
                curr_cancellation = self._cancel_times[0]
            if len(self._alert_times) == 0 and len(self._cancel_times) == 0:
                break


            self.prop_alert()

        print(f"@{self._length}")











