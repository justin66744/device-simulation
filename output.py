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

        self._cancelled_alerts = []

    def prop_alert(self):
        msgs = []
        curr_alert = []
        curr_props = []
        for dev_id, (desc, time) in self._alerts.items():
            curr_alert.append((dev_id, (desc, time)))

        for dev_id, (propped_to, delay) in self._propagates.items():
            curr_props.append((dev_id, (propped_to, delay)))

        for dev_id, (desc, time) in curr_alert:
            self._time = int(time)
            if dev_id in self._propagates.keys():
                delay = self._propagates[dev_id][1]
                new_time = self._time

                while new_time < self._length:
                    for prop in curr_props:
                        new_time += int(prop[1][1])
                        if new_time < self._length:
                            msgs.append(f"@{self._time}: #{prop[0]} SENT ALERT TO #{prop[1][0]}: {desc}")
                            msgs.append(f"@{new_time}: #{prop[1][0]} RECEIVED ALERT FROM #{prop[0]}: {desc}")
                        self._time = new_time
        return msgs



    def prop_cancel(self):
        msgs = []
        curr_cancel = []
        curr_props = []
        for dev_id, (desc, time) in self._cancellations.items():
            curr_cancel.append((dev_id, (desc, time)))

        for dev_id, (propped_to, delay) in self._propagates.items():
            curr_props.append((dev_id, (propped_to, delay)))

        for dev_id, (desc, time) in curr_cancel:
            self._time = int(time)
            if dev_id in self._propagates.keys():
                delay = self._propagates[dev_id][1]
                new_time = self._time

                while new_time < self._length:
                    if len(curr_props) == len(self._cancelled_alerts):
                        break
                    for prop in curr_props:
                        new_time += int(prop[1][1])
                        if new_time < self._length:
                            msgs.append(f"@{self._time}: #{prop[0]} SENT CANCELLATION TO #{prop[1][0]}: {desc}")
                            msgs.append(f"@{new_time}: #{prop[1][0]} RECEIVED CANCELLATION FROM #{prop[0]}: {desc}")
                        self._time = new_time
                        self._cancelled_alerts.append(prop)
        return msgs




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

            raw_msgs = []

            cancelled_msgs = self.prop_cancel()
            raw_msgs.extend(cancelled_msgs)
            self._time = 0
            alert_msgs = self.prop_alert()
            raw_msgs.extend(alert_msgs)

            def timestamp(message):
                return int(message.split('@')[1].split(':')[0])

            raw_msgs.sort(key=timestamp)

            final_msgs = []
            sent_cancellations = {}
            received_cancellations = {}

            for msg in raw_msgs:
                if 'CANCELLATION' in msg:
                    pieces = msg.split()
                    time = timestamp(msg)
                    if 'SENT' in msg:
                        from_dev = pieces[1][1:]
                        to_dev = pieces[5][1:]
                        sent_cancellations[(from_dev, to_dev)] = time
                    elif 'RECEIVED' in msg:
                        to_dev = pieces[1][1:]
                        from_dev = pieces[5][1:]
                        received_cancellations[(to_dev, from_dev)] = time

            for msg in raw_msgs:
                if 'ALERT' in msg:
                    pieces = msg.split()
                    time = timestamp(msg)

                    if 'SENT' in msg:
                        from_dev = pieces[1][1:]
                        to_dev = pieces[5][1:]
                        if (from_dev, to_dev) in sent_cancellations:
                            if time >= sent_cancellations[(from_dev, to_dev)]:
                                continue
                    elif 'RECEIVED' in msg:
                        to_dev = pieces[1][1:]
                        from_dev = pieces[5][1:]
                        if (to_dev, from_dev) in received_cancellations:
                            if time >= received_cancellations[(to_dev, from_dev)]:
                                continue

                final_msgs.append(msg)

            final_msgs.sort(key = timestamp)

            for msg in final_msgs:
                print(msg)

        print(f"@{self._length}: END")
