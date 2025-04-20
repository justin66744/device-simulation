from pathlib import Path


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

        pieces = line.split()
        start = pieces[0]

        if start == 'LENGTH' and len(pieces) == 2:
            length = int(pieces[1])
        elif start == 'DEVICE' and len(pieces) == 2:
            devices.append(int(pieces[1]))
        elif start == 'PROPAGATE' and len(pieces) == 4:
            alerted = pieces[1]
            propagated = pieces[2]
            delay = pieces[3]
            propagates[alerted] = (propagated, delay)
        elif start == 'ALERT' and len(pieces) == 4:
            dev_id = pieces[1]
            description = pieces[2]
            time = pieces[3]
            alerts[dev_id] = (description, time)
        elif start == 'CANCEL' and len(pieces) == 4:
            dev_id = pieces[1]
            description = pieces[2]
            time = pieces[3]
            cancellations[dev_id] = (description, time)

    return length, devices, propagates, alerts, cancellations





def main() -> None:
    """Runs the simulation program in its entirety"""
    input_file_path = _read_input_file_path()


if __name__ == '__main__':
    main()
