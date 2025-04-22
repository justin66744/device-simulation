from pathlib import Path
from output import Simulation


def _read_input_file_path() -> Path:
    """Reads the input file path from the standard input"""
    return Path(input())

def file_read(my_path):

    if not my_path.exists():
        print('FILE NOT FOUND')
        return

    length = None
    devices = []
    propagates = {}
    alerts = {}
    cancellations = {}

    with my_path.open('r') as file:
        for line in file:
            line = line.strip()
            if not line:
                continue
            pieces = line.split()
            start = pieces[0]

            if start == 'LENGTH':
                length = int(pieces[1])
            elif start == 'DEVICE':
                devices.append(int(pieces[1]))
            elif start == 'PROPAGATE':
                dev_id = pieces[1]
                propagated = pieces[2]
                delay = pieces[3]
                propagates[dev_id] = (propagated, delay)
            elif start == 'ALERT':
                dev_id = pieces[1]
                description = pieces[2]
                time = pieces[3]
                alerts[dev_id] = (description, time)
            elif start == 'CANCEL':
                dev_id = pieces[1]
                description = pieces[2]
                time = pieces[3]
                cancellations[dev_id] = (description, time)

    return length, devices, propagates, alerts, cancellations





def main() -> None:
    """Runs the simulation program in its entirety"""
    input_file_path = _read_input_file_path()
    lengths, devices, propagates, alerts, cancellations = file_read(input_file_path)
    print(lengths, devices, propagates, alerts, cancellations)
    test = Simulation(lengths, devices, propagates, alerts, cancellations)
    test.run()


if __name__ == '__main__':
    main()
