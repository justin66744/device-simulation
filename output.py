class Simulation:
    def __init__(self, length, devices, propagates, alerts, cancellations):
        self._length = length
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

    def run(self):
        while self._time < self._length:
            continue




