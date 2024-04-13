import logging


def read_meminfo_file():
    """Reads the /proc/meminfo file and returns its content as a list of lines."""
    try:
        with open('/proc/meminfo', 'r') as file:
            return file.readlines()
    except FileNotFoundError:
        logging.warning("File not found: /proc/meminfo")
        return []
    except Exception as e:
        logging.error(f"Error reading file /proc/meminfo: {str(e)}")
        return []


def parse_meminfo_line(line):
    """Parses a line from the /proc/meminfo file and returns a key-value pair."""
    k, v = map(str.strip, line.strip().split(':', 1))
    return k, v


def get_host_mem():
    """Returns information about the host's memory."""
    mem = {}
    meminfo_lines = read_meminfo_file()
    for line in meminfo_lines:
        if not line.strip():
            continue

        k, v = parse_meminfo_line(line)

        for a, b in (('MemTotal', 'Total'), ('MemFree', 'Free'), ('MemAvailable', 'Available'), ('Buffers', 'Buffers'), ('Cached', 'Cached')):
            if k == a:
                mem[b] = v

    return mem
